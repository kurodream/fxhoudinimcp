# Portable Read-only Houdini MCP Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Make the read-only Houdini MCP reproducible from the fork on a new Windows computer.

**Architecture:** Keep source, policy, entry point, and documentation in Git. Generate a project-local `.venv` and append a path-resolved Codex stdio server entry through a PowerShell bootstrap script.

**Tech Stack:** Python 3.10+, MCP SDK, PowerShell, Codex `config.toml`, pytest and ruff.

**Spec:** `docs/superpowers/specs/2026-10-29-portable-readonly-mcp-design.md`

## Global Constraints

- Read-only mode must hide arbitrary code execution and mutation tools.
- Do not commit `.venv`, `site-packages`, Python executables, or user-specific Codex configuration.
- Do not overwrite an existing `fxhoudini` Codex entry.
- Keep the upstream full-authoring entry point unchanged.

## Review Focus

- Existing Codex config: bootstrap backs it up and refuses duplicate server names; covered by script behavior review.
- Repository paths containing spaces: use absolute quoted TOML paths; covered by path construction review.
- Python launcher differences: `-Python` override; covered by setup script branch.
- Houdini not running: documentation states the client starts but inspection calls require the Houdini plugin session.
- Read-only regression: policy, registration count, and forbidden tool tests cover the server surface.

### Task 1: Portable bootstrap and documentation

**Files:**
- Create: `setup-readonly-mcp.ps1`
- Create: `config.codex.toml.example`
- Create: `docs/readonly-mcp-setup.md`
- Create: `docs/superpowers/specs/2026-10-29-portable-readonly-mcp-design.md`
- Modify: `README.md`

- [ ] Run the read-only policy and registration tests.
- [ ] Run ruff, compile checks, and `git diff --check`.
- [ ] Commit the portable read-only implementation on `portable-readonly-mcp`.
