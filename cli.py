# ===== File: codegen/cli.py =====
import argparse
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any


def build_report() -> Dict[str, Any]:
    """Create a minimal report. No external params required."""
    return {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "message": "Minimal CodeGen report",
        "items": [
            {"id": "item1", "note": "example"},
        ],
    }


def main(argv=None):
    """
    Minimal CodeGen CLI entrypoint.
    - If called without args, writes to ./output/codegen_report.json by default.
    - If called programmatically, you may pass argv list like:
        main(["--output_path", "/tmp/out.json"])
    Exits with SystemExit(0) on success, SystemExit(1) on failure.
    """
    parser = argparse.ArgumentParser(prog="codegen")
    parser.add_argument(
        "--output_path",
        required=False,
        default=str(Path.cwd() / "output" / "codegen_report.json"),
        help="Path to write JSON output (default: ./output/codegen_report.json)",
    )
    args = parser.parse_args(argv)

    out_path = Path(args.output_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    report = build_report()

    try:
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"❌ Failed to write output: {e}", file=sys.stderr)
        raise SystemExit(1)

    # stdout message is optional; keep for debug
    print(f"✅ CodeGen wrote report to {out_path}", file=sys.stdout)
    raise SystemExit(0)
