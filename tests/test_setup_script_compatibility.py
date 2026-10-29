from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "setup-readonly-mcp.ps1"


def test_setup_script_uses_windows_powershell_compatible_utf8_encoding():
    text = SCRIPT.read_text(encoding="utf-8-sig")

    assert "-Encoding utf8NoBOM" not in text
    assert "Add-Content -LiteralPath $codexConfig -Value $snippet -Encoding UTF8" in text
