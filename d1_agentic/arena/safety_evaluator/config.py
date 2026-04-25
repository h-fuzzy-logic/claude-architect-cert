"""Configuration dataclasses for the safety evaluator experiment."""

from dataclasses import dataclass, field

from shared.api.models import DEFAULT_MODEL, JUDGMENT_MODEL


@dataclass
class SubagentConfig:
    """Config for each dimension-evaluating subagent."""

    model: str = DEFAULT_MODEL
    max_tokens: int = 1024


@dataclass
class CoordinatorConfig:
    """Config for the coordinator that dispatches subagents."""

    model: str = JUDGMENT_MODEL
    max_tokens: int = 2048


@dataclass
class SafetyDimensions:
    """Flags controlling which safety dimensions are evaluated."""

    harm: bool = True
    honesty: bool = True
    helpfulness: bool = True
    instruction_following: bool = True

    def active(self) -> list[str]:
        """Return the list of enabled dimension names."""
        return [name for name, enabled in vars(self).items() if enabled]


@dataclass
class OutputConfig:
    """Controls where results are written."""

    results_dir: str = "data/results"
    domain: str = "d1"
    experiment: str = "safety_evaluator"


@dataclass
class EvaluatorConfig:
    """Top-level config — compose sub-configs here, not magic numbers in run.py."""

    subagent: SubagentConfig = field(default_factory=SubagentConfig)
    coordinator: CoordinatorConfig = field(default_factory=CoordinatorConfig)
    dimensions: SafetyDimensions = field(default_factory=SafetyDimensions)
    output: OutputConfig = field(default_factory=OutputConfig)
