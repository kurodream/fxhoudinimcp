# Portable read-only Houdini MCP design

## Intent

Make the fork reproducible on another Windows computer without committing a
Python runtime or user-specific Codex state.

## Goals

- Keep the read-only tool allowlist and dedicated entry point in the fork.
- Create a project-local `.venv` from the repository's declared dependencies.
- Generate a Codex config entry with absolute paths and a safe backup.
- Document Houdini, Codex, restart, and verification steps.

## Non-goals

- Shipping Houdini or its license/runtime.
- Committing `.venv`, `site-packages`, or machine-specific configuration.
- Changing the upstream full-authoring entry point.

## Decision

Use a PowerShell bootstrap script plus `python -m fxhoudinimcp.readonly`.
Absolute paths are generated locally because Python and the checkout location
can differ between computers. Existing Codex entries are never overwritten.

