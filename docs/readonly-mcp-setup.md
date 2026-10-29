# Portable read-only Houdini MCP

This checkout provides a read-only MCP entry point for inspecting a running
Houdini session. The repository is the source of truth; the virtual
environment and Codex registration are generated locally on each computer.

## Requirements

- Windows PowerShell
- Python 3.10 or newer
- Houdini 20.5 or newer with the FXHoudini plugin installed
- Codex Desktop or Codex CLI

Do not commit `.venv`, `site-packages`, Python executables, or user-specific
Codex configuration. They are machine-specific and are ignored/generated.

## One-time setup on a new computer

From the repository root:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\setup-readonly-mcp.ps1 -ConfigureCodex
```

Run this from a normal PowerShell after fully closing Codex Desktop. Codex's
own sandbox may prevent the script from creating `venv` files or backing up
`%USERPROFILE%\.codex\config.toml`.

The script creates `.venv`, installs this checkout in editable mode, and adds
an absolute-path `[mcp_servers.fxhoudini]` entry to
`%USERPROFILE%\.codex\config.toml`. If a server with that name already exists,
the script stops rather than overwriting it. Existing config is backed up as
`config.toml.bak` before a new entry is appended.

The script checks `py`, then `python`, then `python.exe`. If Python is installed
at a known absolute path, pass it explicitly:

```powershell
.\setup-readonly-mcp.ps1 -Python D:\App\Python312\python.exe -ConfigureCodex
```

## Houdini side

Install the Houdini package from this checkout using the upstream installer,
or point a Houdini package file at the repository's `houdini/` directory. The
MCP client does not load Houdini itself; Houdini must already be running and
serving the plugin before inspection calls can return scene data.

## Verify

Restart Codex completely and create a new chat. The MCP server should appear as
`fxhoudini`. Its tool list must contain inspection tools such as
`get_scene_info`, `get_node_info`, `get_geometry_info`, and `get_hda_info`, and
must not contain `execute_python`, `execute_hscript`, `create_node`, or
`set_parameter`.

The portable entry point is:

```powershell
.\.venv\Scripts\python.exe -m fxhoudinimcp.readonly
```

The normal `fxhoudinimcp` entry point remains available for the upstream
full-authoring surface, but it is intentionally not used by this setup guide.

