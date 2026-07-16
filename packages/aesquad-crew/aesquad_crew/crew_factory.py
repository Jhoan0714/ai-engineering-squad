"""Assemble a CrewAI Crew from a pipeline + discovered role packs."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from aesquad_crew.pipeline import Pipeline, PipelineStep
from aesquad_crew.role_loader import RoleSpec, load_role
from aesquad_crew.task_builder import build_expected_output, build_task_description


@dataclass
class BuiltCrew:
    crew: Any
    steps: tuple[PipelineStep, ...]
    roles: dict[str, RoleSpec]
    tasks_by_step: dict[str, Any]


def build_crew(
    pipeline: Pipeline,
    *,
    kit_root: Path,
    change_id: str,
    idea: str,
    verbose: bool = True,
) -> BuiltCrew:
    try:
        from crewai import Agent, Crew, Process, Task
    except ImportError as exc:
        raise ImportError(
            "crewai is required to run the squad. "
            "Install with: pip install -r packages/aesquad-crew/requirements.txt"
        ) from exc

    roles_root = kit_root / "roles"
    skills_root = kit_root / "skills"
    schemas_root = kit_root / "contracts" / "schemas"

    roles: dict[str, RoleSpec] = {}
    agents: dict[str, Any] = {}

    for step in pipeline.steps:
        if step.role not in roles:
            roles[step.role] = load_role(
                roles_root, step.role, skills_root=skills_root
            )
        role = roles[step.role]
        if step.role not in agents:
            agents[step.role] = Agent(
                role=role.title,
                goal=role.goal,
                backstory=role.backstory,
                verbose=verbose,
                allow_delegation=False,
            )

    tasks_by_step: dict[str, Any] = {}
    ordered_tasks: list[Any] = []

    for step in pipeline.steps:
        role = roles[step.role]
        context_tasks = [tasks_by_step[ref] for ref in step.context_from]
        task = Task(
            description=build_task_description(
                step=step,
                role=role,
                change_id=change_id,
                idea=idea,
                schemas_root=schemas_root,
            ),
            expected_output=build_expected_output(step),
            agent=agents[step.role],
            context=context_tasks or None,
        )
        tasks_by_step[step.id] = task
        ordered_tasks.append(task)

    ordered_agents: list[Any] = []
    seen_roles: set[str] = set()
    for step in pipeline.steps:
        if step.role not in seen_roles:
            ordered_agents.append(agents[step.role])
            seen_roles.add(step.role)

    crew = Crew(
        agents=ordered_agents,
        tasks=ordered_tasks,
        process=Process.sequential,
        verbose=verbose,
    )
    return BuiltCrew(
        crew=crew,
        steps=pipeline.steps,
        roles=roles,
        tasks_by_step=tasks_by_step,
    )
