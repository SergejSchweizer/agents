import importlib.util


def test_install_agents_module_loads() -> None:
    spec = importlib.util.spec_from_file_location("install_agents", "install_agents.py")
    assert spec is not None
    assert spec.loader is not None
