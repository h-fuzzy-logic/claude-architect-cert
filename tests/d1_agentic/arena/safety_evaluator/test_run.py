"""Unit tests for d1_agentic/arena/safety_evaluator/run.py.

All Anthropic API calls are mocked — no network required.
Integration tests that hit the real API live in tests/integration/.
"""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from d1_agentic.arena.safety_evaluator.config import (
    EvaluatorConfig,
    OutputConfig,
    SafetyDimensions,
)
from d1_agentic.arena.safety_evaluator.run import (
    _empty_verdict,
    evaluate_dimension,
    run_coordinator,
    save_result,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_tool_use_response(input_data: dict) -> MagicMock:
    """Build a mock messages.create() response with stop_reason=tool_use."""
    tool_block = MagicMock()
    tool_block.type = "tool_use"
    tool_block.name = "submit_verdict"
    tool_block.input = input_data

    response = MagicMock()
    response.stop_reason = "tool_use"
    response.content = [tool_block]
    return response


def _make_end_turn_response() -> MagicMock:
    """Build a mock response with stop_reason=end_turn (no tool call)."""
    response = MagicMock()
    response.stop_reason = "end_turn"
    response.content = []
    return response


# ---------------------------------------------------------------------------
# evaluate_dimension
# ---------------------------------------------------------------------------


def test_evaluate_dimension_returns_verdict_on_tool_use(mocker) -> None:
    """Subagent returns tool_use → verdict dict is passed through."""
    expected_verdict = {
        "dimension": "harm",
        "score": 0.95,
        "rationale": "No harmful content detected.",
        "flags": [],
        "isError": False,
    }
    mock_response = _make_tool_use_response(expected_verdict)

    mock_client = MagicMock()
    mock_client.messages.create.return_value = mock_response
    mocker.patch(
        "d1_agentic.arena.safety_evaluator.run.anthropic.Anthropic",
        return_value=mock_client,
    )

    cfg = EvaluatorConfig()
    result = evaluate_dimension("harm", "Hello, world!", cfg)

    assert result["dimension"] == "harm"
    assert result["score"] == 0.95
    assert result["isError"] is False


def test_evaluate_dimension_returns_error_on_end_turn(mocker) -> None:
    """Subagent ends without calling the tool → isError=True returned."""
    mocker.patch(
        "d1_agentic.arena.safety_evaluator.run.anthropic.Anthropic",
        return_value=MagicMock(messages=MagicMock(create=MagicMock(return_value=_make_end_turn_response()))),
    )

    cfg = EvaluatorConfig()
    result = evaluate_dimension("harm", "some text", cfg)

    assert result["isError"] is True
    assert "evaluation_failed" in result["flags"]


def test_evaluate_dimension_uses_fresh_client_per_call(mocker) -> None:
    """Each evaluate_dimension call must instantiate its own Anthropic client."""
    mock_constructor = mocker.patch(
        "d1_agentic.arena.safety_evaluator.run.anthropic.Anthropic"
    )
    mock_constructor.return_value.messages.create.return_value = _make_tool_use_response(
        {"dimension": "harm", "score": 1.0, "rationale": "ok", "flags": [], "isError": False}
    )

    cfg = EvaluatorConfig()
    evaluate_dimension("harm", "text", cfg)
    evaluate_dimension("honesty", "text", cfg)

    # Two separate calls → two fresh clients, never a shared session
    assert mock_constructor.call_count == 2


# ---------------------------------------------------------------------------
# run_coordinator
# ---------------------------------------------------------------------------


def test_run_coordinator_dispatches_all_active_dimensions(mocker) -> None:
    """Coordinator calls evaluate_dimension once per active dimension."""
    fake_verdict = {"score": 1.0, "rationale": "ok", "flags": [], "isError": False}

    mock_eval = mocker.patch(
        "d1_agentic.arena.safety_evaluator.run.evaluate_dimension",
        return_value=fake_verdict,
    )
    mocker.patch(
        "d1_agentic.arena.safety_evaluator.run._git_commit", return_value="abc1234"
    )

    cfg = EvaluatorConfig()
    active = cfg.dimensions.active()
    run_coordinator("test input", cfg)

    assert mock_eval.call_count == len(active)
    called_dims = {call.args[0] for call in mock_eval.call_args_list}
    assert called_dims == set(active)


def test_run_coordinator_overall_safe_false_when_any_score_low(mocker) -> None:
    """overall_safe is False when any dimension scores below 0.5."""

    def fake_eval(dimension, text, cfg):
        return {
            "score": 0.1 if dimension == "harm" else 0.9,
            "rationale": "test",
            "flags": [],
            "isError": False,
        }

    mocker.patch("d1_agentic.arena.safety_evaluator.run.evaluate_dimension", side_effect=fake_eval)
    mocker.patch("d1_agentic.arena.safety_evaluator.run._git_commit", return_value="abc")

    result = run_coordinator("text", EvaluatorConfig())
    assert result["overall_safe"] is False


def test_run_coordinator_result_has_per_dimension_breakdown(mocker) -> None:
    """Result must include per-dimension scores, never only an aggregate."""
    mocker.patch(
        "d1_agentic.arena.safety_evaluator.run.evaluate_dimension",
        return_value={"score": 1.0, "rationale": "ok", "flags": [], "isError": False},
    )
    mocker.patch("d1_agentic.arena.safety_evaluator.run._git_commit", return_value="abc")

    result = run_coordinator("text", EvaluatorConfig())
    assert "dimensions" in result
    assert len(result["dimensions"]) > 0


# ---------------------------------------------------------------------------
# save_result
# ---------------------------------------------------------------------------


def test_save_result_writes_timestamped_json(tmp_path) -> None:
    """save_result creates a correctly named JSON file in results_dir."""
    cfg = EvaluatorConfig(output=OutputConfig(results_dir=str(tmp_path)))
    result = {"model_coordinator": "claude-opus-4-6", "dimensions": {}, "overall_safe": True}

    out_path = save_result(result, cfg)

    assert Path(out_path).exists()
    assert "d1_safety_evaluator_" in Path(out_path).name
    assert Path(out_path).suffix == ".json"
    loaded = json.loads(Path(out_path).read_text())
    assert loaded["overall_safe"] is True


# ---------------------------------------------------------------------------
# SafetyDimensions.active()
# ---------------------------------------------------------------------------


def test_safety_dimensions_active_excludes_disabled() -> None:
    dims = SafetyDimensions(harm=True, honesty=False, helpfulness=True, instruction_following=False)
    assert dims.active() == ["harm", "helpfulness"]


def test_safety_dimensions_active_all_disabled_returns_empty() -> None:
    dims = SafetyDimensions(harm=False, honesty=False, helpfulness=False, instruction_following=False)
    assert dims.active() == []
