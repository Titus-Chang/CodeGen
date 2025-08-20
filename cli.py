# ===== File: codegen/cli.py =====
import argparse
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any


def build_report_dict(args: argparse.Namespace) -> Dict[str, Any]:
    return {
        "project_url": args.project_url,
        "project_name": args.project_name,
        "username": args.username,
        "severity_level": args.severity_level,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "summary": {
            "files_scanned": 2,
            "issues_found": 1,
            "top_issues": [
                {"id": "CG001", "severity": "Medium", "message": "Sample codegen issue"}
            ],
        },
    }


def main(argv=None):
    """
    Minimal CodeGen CLI main.
    Can be called as a CLI or imported and called programmatically.
    Exits with SystemExit(0) on success, SystemExit(1) on failure.
    """
    parser = argparse.ArgumentParser(prog="codegen")
    parser.add_argument("--project_url", default="", help="Project base URL")
    parser.add_argument("--project_name", default="", help="Project name")
    parser.add_argument("--username", default="", help="Username")
    parser.add_argument("--password", default="", help="Password (unused)")
    parser.add_argument("--severity_level", default=5, type=int, help="Severity threshold")
    parser.add_argument("--output_path", required=True, help="Path to write JSON output")

    args = parser.parse_args(argv)

    out_path = Path(args.output_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    report = build_report_dict(args)

    try:
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"❌ Failed to write output: {e}", file=sys.stderr)
        raise SystemExit(1)

    print(f"✅ CodeGen wrote report to {out_path}")
    raise SystemExit(0)
