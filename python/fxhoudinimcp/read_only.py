"""The explicitly supported read-only MCP tool surface.

The allowlist is deliberately conservative.  A tool is not exposed in
read-only mode unless its implementation is known to inspect Houdini state
without changing the scene, writing files, launching work, or executing
caller-supplied code.
"""

from __future__ import annotations

from os import environ

READ_ONLY_TOOLS = frozenset(
    {
        # Connection and scene inspection.
        "get_houdini_connection_status",
        "get_scene_info",
        "get_context_info",
        # Nodes and graph.
        "get_node_info",
        "list_children",
        "find_nodes",
        "list_node_types",
        "verify_network",
        "get_node_card",
        "find_expensive_nodes",
        "get_cook_status",
        # Parameters and expressions (read-only variants).
        "get_parameter",
        "get_parameter_schema",
        "get_parm_references",
        "get_parm_template_tree",
        "get_expression",
        "get_parameters",
        # SOP geometry inspection.
        "get_geometry_info",
        "get_points",
        "get_prims",
        "get_attrib_values",
        "get_groups",
        "get_group_members",
        "get_bounding_box",
        "get_attribute_info",
        "sample_geometry",
        "get_prim_intrinsics",
        "find_nearest_point",
        "get_attrib_stats",
        "get_volume_info",
        "sample_volume",
        "compare_volumes",
        # HDA inspection.
        "list_installed_hdas",
        "get_hda_info",
        "get_hda_sections",
        "get_hda_section_content",
        "list_hda_versions",
        # USD / Solaris inspection.
        "get_stage_info",
        "list_usd_prims",
        "get_usd_prim",
        "get_usd_attribute",
        "get_usd_attributes",
        "get_usd_world_transform",
        "get_usd_layers",
        "get_usd_prim_stats",
        "get_last_modified_prims",
        "get_usd_bound_material",
        "get_usd_materials",
        "find_usd_prims",
        "get_usd_composition",
        "get_usd_variants",
        "inspect_usd_layer",
        "list_lights",
        # Materials, dynamics, PDG, COPs, CHOPs.
        "list_materials",
        "get_material_info",
        "list_material_types",
        "get_simulation_info",
        "list_dop_objects",
        "get_dop_object",
        "get_dop_field",
        "get_dop_relationships",
        "get_sim_memory_usage",
        "get_top_network_info",
        "get_work_item_states",
        "get_work_item_info",
        "get_pdg_graph",
        "get_top_scheduler_info",
        "get_failed_work_items",
        "get_top_logs",
        "get_cop_info",
        "get_cop_geometry",
        "get_cop_layer",
        "list_cop_node_types",
        "get_cop_vdb",
        "get_chop_data",
        "list_chop_channels",
        # VEX, cache, animation, rendering and viewport inspection.
        "validate_vex",
        "get_wrangle_code",
        "list_caches",
        "get_cache_status",
        "get_frame",
        "get_keyframes",
        "list_render_nodes",
        "get_render_settings",
        "get_render_progress",
        "list_panes",
        "get_viewport_info",
        "find_error_nodes",
        "log_status",
        # Documentation and file-reference inspection.
        "search_help",
        "get_help_page",
        "get_workflow_guide",
        "get_env_variable",
        "get_file_references",
        "list_shelf_tools",
        "get_shelf_tool_script",
        "list_takes",
        "get_current_take",
    }
)


def read_only_mode_enabled() -> bool:
    """Return whether the MCP server should expose only the allowlist."""

    return environ.get("FXHOUDINIMCP_READ_ONLY", "").strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


def is_read_only_tool(name: str) -> bool:
    """Return whether *name* is safe to register in read-only mode."""

    return name in READ_ONLY_TOOLS

