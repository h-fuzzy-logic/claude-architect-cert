"""Tests for shared/api/models.py — one test per public constant."""

from shared.api.models import DEFAULT_MODEL, EVAL_MODEL, JUDGMENT_MODEL


def test_model_constants_are_non_empty_strings() -> None:
    for name, value in [
        ("DEFAULT_MODEL", DEFAULT_MODEL),
        ("EVAL_MODEL", EVAL_MODEL),
        ("JUDGMENT_MODEL", JUDGMENT_MODEL),
    ]:
        assert isinstance(value, str) and value, f"{name} must be a non-empty string"


def test_model_constants_follow_claude_naming() -> None:
    for value in [DEFAULT_MODEL, EVAL_MODEL, JUDGMENT_MODEL]:
        assert value.startswith("claude-"), f"Expected claude-* model, got: {value}"
