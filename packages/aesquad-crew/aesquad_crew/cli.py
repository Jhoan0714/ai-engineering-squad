"""CLI entrypoints for aesquad-crew."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from aesquad_crew.kit import default_pipeline_path, find_kit_root
from aesquad_crew.llm import resolve_llm_config
from aesquad_crew.persist import collect_task_outputs, persist_handoffs
from aesquad_crew.pipeline import load_pipeline
from aesquad_crew.role_loader import discover_role_ids, load_role
from aesquad_crew.validate_runner import maybe_validate


def _cmd_list(args: argparse.Namespace) -> int:
    kit_root = Path(args.kit_root).resolve() if args.kit_root else find_kit_root()
    pipeline_path = (
        Path(args.pipeline).resolve()
        if args.pipeline
        else default_pipeline_path(kit_root)
    )
    pipeline = load_pipeline(pipeline_path)
    available = discover_role_ids(kit_root / "roles")
    llm_config = resolve_llm_config(
        model=getattr(args, "llm", None),
        base_url=getattr(args, "llm_base_url", None),
    )

    print(f"Kit root:     {kit_root}")
    print(f"Pipeline:     {pipeline_path}")
    print(f"Pipeline id:  {pipeline.id} ({pipeline.title})")
    print(f"Process:      {pipeline.process}")
    print(f"Roles on disk:{', '.join(available) or '(none)'}")
    if llm_config:
        print(f"LLM:          {llm_config.display}")
    else:
        print("LLM:          (CrewAI default — set --llm or AESQUAD_LLM for Ollama)")
    print()
    print("Steps (dynamic agents/tasks):")
    for i, step in enumerate(pipeline.steps, start=1):
        role = load_role(kit_root / "roles", step.role, skills_root=kit_root / "skills")
        skills = ", ".join(role.skills) or "(none listed)"
        print(f"  {i}. [{step.id}]")
        print(f"     role title : {role.title}")
        print(f"     role id    : {role.id}")
        print(f"     goal       : {role.goal}")
        print(f"     skills     : {skills}")
        print(f"     handoff    : {step.handoff} → {step.artifact}")
        print(f"     contextFrom: {', '.join(step.context_from) or '(none)'}")
    print()
    print(
        f"Human gate (not automated): {pipeline.human.handoff} → {pipeline.human.artifact}"
    )
    return 0


def _cmd_run(args: argparse.Namespace) -> int:
    from aesquad_crew.crew_factory import build_crew

    kit_root = Path(args.kit_root).resolve() if args.kit_root else find_kit_root()
    pipeline_path = (
        Path(args.pipeline).resolve()
        if args.pipeline
        else default_pipeline_path(kit_root)
    )
    out_root = Path(args.out_dir).resolve() if args.out_dir else Path.cwd()
    pipeline = load_pipeline(pipeline_path)
    llm_config = resolve_llm_config(
        model=args.llm,
        base_url=args.llm_base_url,
        api_key=args.llm_api_key,
        temperature=args.temperature,
    )

    if llm_config:
        print(f"Using LLM: {llm_config.display}")
    else:
        print(
            "Using CrewAI default LLM (usually OpenAI). "
            "For Ollama: --llm llama3.1:latest"
        )

    built = build_crew(
        pipeline,
        kit_root=kit_root,
        change_id=args.change_id,
        idea=args.idea,
        verbose=not args.quiet,
        llm_config=llm_config,
    )

    print(
        f"Running pipeline `{pipeline.id}` with {len(pipeline.steps)} dynamic steps…"
    )
    result = built.crew.kickoff()
    task_outputs = collect_task_outputs(result)

    handoff_dir = out_root / "handoffs" / args.change_id
    persist_handoffs(
        pipeline=pipeline,
        steps=built.steps,
        task_outputs=task_outputs,
        handoff_dir=handoff_dir,
        out_root=out_root,
        change_id=args.change_id,
        idea=args.idea,
    )

    if not args.skip_validate and (handoff_dir / pipeline.steps[0].artifact).exists():
        code = maybe_validate(kit_root, handoff_dir)
        if code != 0:
            return code
    return 0


def _add_llm_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--llm",
        help=(
            "Model id (e.g. llama3.1:latest, ollama/llama3.1:latest, gpt-4o-mini). "
            "Also: AESQUAD_LLM"
        ),
    )
    parser.add_argument(
        "--llm-base-url",
        help="LLM base URL (default for ollama/: http://localhost:11434). Also: AESQUAD_LLM_BASE_URL",
    )
    parser.add_argument(
        "--llm-api-key",
        help="Optional API key. Also: AESQUAD_LLM_API_KEY",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=None,
        help="Sampling temperature (default 0.2 when --llm is set)",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="aesquad-crew",
        description=(
            "Run AI Engineering Squad as a dynamic CrewAI pipeline "
            "(roles/skills/workflows driven — not a hard-coded roster)."
        ),
    )
    parser.add_argument(
        "--kit-root",
        help="Path to ai-engineering-squad root (auto-detected if omitted)",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    list_p = sub.add_parser(
        "list",
        help="Show pipeline steps with goals/roles loaded from AGENT.md",
    )
    list_p.add_argument(
        "--pipeline",
        help="Pipeline YAML (default: workflows/feature-delivery.pipeline.yaml)",
    )
    _add_llm_args(list_p)
    list_p.set_defaults(func=_cmd_list)

    run_p = sub.add_parser("run", help="Execute the sequential crew for a change")
    run_p.add_argument("--change-id", required=True)
    run_p.add_argument("--idea", required=True)
    run_p.add_argument(
        "--pipeline",
        help="Pipeline YAML (default: workflows/feature-delivery.pipeline.yaml)",
    )
    run_p.add_argument(
        "--out-dir",
        help="Directory for handoffs/ and openspec/ (default: cwd)",
    )
    run_p.add_argument(
        "--skip-validate",
        action="store_true",
        help="Do not run aesquad validate after writing handoffs",
    )
    run_p.add_argument(
        "--quiet",
        action="store_true",
        help="Less CrewAI verbose logging",
    )
    _add_llm_args(run_p)
    run_p.set_defaults(func=_cmd_run)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except (FileNotFoundError, ValueError, KeyError, ImportError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
