from src.bootstrap import bootstrap

def test_bootstrap_standalone():
    assert bootstrap()["status"] == "ready"

def test_bootstrap_failure_isolated():
    def bad():
        raise RuntimeError("boom")
    result = bootstrap(bad)
    assert result["status"] == "failed"
    assert "boom" in result["error"]
