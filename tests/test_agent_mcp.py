from src.ai.agent import AgentExecutor, AgentPlanner, AgentReviewer, AgentStep
from src.mcp.tools import ToolRegistry, ToolSpec

def test_agent_runs_tools_and_reviews():
    planner = AgentPlanner()
    plan = planner.plan("inspect", [AgentStep("echo", {"value": 3})])
    run = AgentExecutor({"echo": lambda value: value * 2}).run(plan)
    assert run.ok
    assert run.steps[0]["result"] == 6
    assert AgentReviewer().review(run)["ok"]

def test_agent_required_failure_isolated():
    plan = AgentPlanner().plan("broken", [AgentStep("missing", required=True)])
    run = AgentExecutor().run(plan)
    assert not run.ok
    assert "not registered" in run.error.lower()

def test_agent_optional_failure_continues():
    plan = AgentPlanner().plan(
        "mixed",
        [AgentStep("bad", required=False), AgentStep("good", {"value": 4})],
    )
    run = AgentExecutor({"bad": lambda: (_ for _ in ()).throw(RuntimeError("boom")),
                         "good": lambda value: value + 1}).run(plan)
    assert run.ok
    assert run.steps[1]["result"] == 5

def test_mcp_tool_registry_is_structured_and_safe():
    registry = ToolRegistry([
        ToolSpec("echo", "Echo a value", lambda value: value, {"type": "object"})
    ])
    assert registry.names() == ["echo"]
    assert registry.describe()[0]["name"] == "echo"
    assert registry.call("echo", value=7)["result"] == 7
    assert registry.call("missing")["ok"] is False

def test_mcp_tool_handler_failure_isolated():
    registry = ToolRegistry([
        ToolSpec("bad", "Broken tool", lambda: (_ for _ in ()).throw(RuntimeError("boom")))
    ])
    result = registry.call("bad")
    assert not result["ok"]
    assert "boom" in result["error"]
