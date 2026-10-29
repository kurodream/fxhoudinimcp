"""Contract tests for the opt-in read-only MCP surface."""

from __future__ import annotations

from fxhoudinimcp.read_only import is_read_only_tool, read_only_mode_enabled


def test_read_only_surface_contains_the_inspection_tools():
    for name in (
        "get_houdini_connection_status",
        "get_scene_info",
        "get_node_info",
        "list_children",
        "get_geometry_info",
        "sample_geometry",
        "get_hda_info",
        "get_parameters",
        "get_expression",
        "verify_network",
    ):
        assert is_read_only_tool(name), name


def test_read_only_surface_rejects_code_execution_and_mutation():
    for name in (
        "execute_python",
        "execute_hscript",
        "new_scene",
        "save_scene",
        "load_scene",
        "create_node",
        "set_parameter",
        "create_hda",
        "write_cache",
        "start_render",
        "run_shelf_tool",
    ):
        assert not is_read_only_tool(name), name


def test_unknown_tools_are_not_read_only_by_default():
    assert not is_read_only_tool("some_future_tool")


def test_read_only_mode_accepts_common_boolean_environment_values(monkeypatch):
    for value in ("1", "true", "TRUE", "yes", "on"):
        monkeypatch.setenv("FXHOUDINIMCP_READ_ONLY", value)
        assert read_only_mode_enabled()

    monkeypatch.setenv("FXHOUDINIMCP_READ_ONLY", "0")
    assert not read_only_mode_enabled()


def test_read_only_entrypoint_sets_the_mode_before_starting(monkeypatch):
    import fxhoudinimcp.__main__ as normal_entrypoint
    import fxhoudinimcp.readonly as readonly_entrypoint

    monkeypatch.delenv("FXHOUDINIMCP_READ_ONLY", raising=False)
    called = []
    monkeypatch.setattr(normal_entrypoint, "main", lambda: called.append(True))

    readonly_entrypoint.main()

    assert called == [True]
    assert read_only_mode_enabled()
