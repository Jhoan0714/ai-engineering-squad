"""Sequential pipeline runner with schema validate + retry."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from aesquad_crew.llm import LlmConfig, build_llm
from aesquad_crew.persist import extract_json_block, write_json
from aesquad_crew.pipeline import Pipeline, PipelineStep
from aesquad_crew.role_loader import RoleSpec, load_role
from aesquad_crew.schema_validate import validate_handoff_data
from aesquad_crew.task_builder import build_expected_output, build_task_description


def _execute_task(agent: Any, task: Any, *, verbose: bool) -> str:
    from crewai import Crew, Process

    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        verbose=verbose,
    )
    result = crew.kickoff()
    if hasattr(result, "raw") and result.raw:
        return str(result.raw)
    if hasattr(result, "tasks_output") and result.tasks_output:
        first = result.tasks_output[0]
        return str(first.raw if hasattr(first, "raw") else first)
    return str(result)


def _make_agent(
    role: RoleSpec,
    *,
    llm: Any,
    verbose: bool,
) -> Any:
    from crewai import Agent

    kwargs: dict[str, Any] = {
        "role": role.title,
        "goal": role.goal,
        "backstory": role.backstory,
        "verbose": verbose,
        "allow_delegation": False,
    }
    if llm is not None:
        kwargs["llm"] = llm
    return Agent(**kwargs)


def _maybe_write_openspec(
    step: PipelineStep,
    data: dict,
    *,
    out_root: Path,
    change_id: str,
    idea: str,
) -> None:
    if not step.openspec_path_template:
        return
    rel = step.openspec_path_template.format(changeId=change_id)
    proposal = out_root / rel
    proposal.parent.mkdir(parents=True, exist_ok=True)
    summary = None
    open_spec = data.get("openSpec")
    if isinstance(open_spec, dict):
        summary = open_spec.get("summary")
    proposal.write_text(
        f"# {change_id}\n\n## Context\n\n{idea}\n\n"
        f"## Proposal\n\n{summary or 'See implementation-handoff.json'}\n",
        encoding="utf-8",
    )
    print(f"Wrote OpenSpec stub to {proposal}")


def run_pipeline(
    pipeline: Pipeline,
    *,
    kit_root: Path,
    change_id: str,
    idea: str,
    out_root: Path,
    llm_config: LlmConfig | None = None,
    verbose: bool = True,
    max_attempts: int = 3,
) -> Path:
    """
    Run each pipeline step sequentially.

    After each step: parse JSON → validate schema → retry with errors if needed.
    """
    try:
        from crewai import Task
    except ImportError as exc:
        raise ImportError(
            "crewai is required to run the squad. "
            "Install with: pip install -r packages/aesquad-crew/requirements.txt"
        ) from exc

    llm = build_llm(llm_config) if llm_config else None
    roles_root = kit_root / "roles"
    skills_root = kit_root / "skills"
    schemas_root = kit_root / "contracts" / "schemas"
    examples_root = kit_root / "contracts" / "examples"

    handoff_dir = out_root / "handoffs" / change_id
    handoff_dir.mkdir(parents=True, exist_ok=True)

    agents: dict[str, Any] = {}
    roles: dict[str, RoleSpec] = {}
    prior: dict[str, dict] = {}

    for index, step in enumerate(pipeline.steps, start=1):
        if step.role not in roles:
            roles[step.role] = load_role(
                roles_root, step.role, skills_root=skills_root
            )
        if step.role not in agents:
            agents[step.role] = _make_agent(
                roles[step.role], llm=llm, verbose=verbose
            )

        role = roles[step.role]
        agent = agents[step.role]
        print(f"\n=== Step {index}/{len(pipeline.steps)}: {step.id} ({step.handoff}) ===")

        last_errors: list[str] = []
        last_attempt: dict | None = None
        success_data: dict | None = None

        for attempt in range(1, max_attempts + 1):
            description = build_task_description(
                step=step,
                role=role,
                change_id=change_id,
                idea=idea,
                schemas_root=schemas_root,
                examples_root=examples_root,
                prior_handoffs=prior or None,
                repair_errors=last_errors or None,
                previous_attempt=last_attempt,
            )
            task = Task(
                description=description,
                expected_output=build_expected_output(step),
                agent=agent,
            )
            print(f"Attempt {attempt}/{max_attempts}…")
            raw = _execute_task(agent, task, verbose=verbose)

            try:
                data = extract_json_block(raw)
            except (ValueError, TypeError) as exc:
                last_errors = [f"Could not parse JSON object: {exc}"]
                last_attempt = None
                print(f"Parse failed: {exc}", file=sys.stderr)
                continue

            result = validate_handoff_data(
                data, handoff=step.handoff, schemas_root=schemas_root
            )
            if result.ok:
                success_data = data
                print(f"OK  {step.artifact} (schema valid)")
                break

            last_errors = result.error_lines
            last_attempt = data
            print(f"FAIL {step.artifact} — {len(last_errors)} schema error(s):", file=sys.stderr)
            for line in last_errors[:12]:
                print(f"  - {line}", file=sys.stderr)

        if success_data is None:
            # Persist last attempt for debugging
            if last_attempt is not None:
                debug_path = handoff_dir / f"{step.artifact}.invalid.json"
                write_json(debug_path, last_attempt)
                print(f"Wrote invalid attempt to {debug_path}", file=sys.stderr)
            raise ValueError(
                f"Step '{step.id}' failed schema validation after {max_attempts} attempts. "
                f"Last errors: {'; '.join(last_errors[:5])}"
            )

        out_path = handoff_dir / step.artifact
        write_json(out_path, success_data)
        prior[step.artifact] = success_data
        _maybe_write_openspec(
            step,
            success_data,
            out_root=out_root,
            change_id=change_id,
            idea=idea,
        )

    print(f"\nWrote handoffs to {handoff_dir}")
    print(
        f"Human next: write {pipeline.human.artifact} after review "
        f"(handoff kind `{pipeline.human.handoff}`)."
    )
    return handoff_dir
