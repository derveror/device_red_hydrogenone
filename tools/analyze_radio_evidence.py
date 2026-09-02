#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Iterable

RADIO_KEY_RE = re.compile(r"(?:radio|ril|ims|multisim|dsds|dsda|phone_count|sim_count|telephony)", re.I)
RADIO_INIT_RE = re.compile(r"(?:qcril|rild|ril-daemon|radio|ims)", re.I)
PROPERTY_NAMES = {"build.prop", "default.prop", "vendor.prop"}
ACTIVATION_VERBS = {"start", "enable", "restart", "ctl.start"}


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _property_rows(path: Path, display_path: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    try:
        text = _read_text(path)
    except (OSError, UnicodeError):
        return rows
    for line_no, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if RADIO_KEY_RE.search(key):
            rows.append({"path": display_path, "line": line_no, "key": key, "value": value})
    return rows


def scan_property_files(root: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not root.exists():
        return rows
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix != ".prop" and path.name not in PROPERTY_NAMES:
            continue
        rows.extend(_property_rows(path, path.relative_to(root).as_posix()))
    return rows


def scan_extra_property_files(paths: Iterable[Path]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in paths:
        if path.is_file():
            rows.extend(_property_rows(path, f"extra:{path.name}"))
    return rows


def scan_init_files(root: Path) -> dict[str, list[dict[str, Any]]]:
    services: list[dict[str, Any]] = []
    starts: list[dict[str, Any]] = []
    stops: list[dict[str, Any]] = []
    controls: list[dict[str, Any]] = []
    imports: list[dict[str, Any]] = []
    if not root.exists():
        return {"services": services, "starts": starts, "stops": stops, "controls": controls, "imports": imports}

    for path in sorted(root.rglob("*.rc")):
        rel = path.relative_to(root).as_posix()
        try:
            lines = _read_text(path).splitlines()
        except (OSError, UnicodeError):
            continue

        current_service: dict[str, Any] | None = None
        current_trigger = "<top-level>"

        def finish_service() -> None:
            nonlocal current_service
            if current_service is None:
                return
            if RADIO_INIT_RE.search(current_service["name"]) or RADIO_INIT_RE.search(current_service["executable"]):
                services.append(current_service)
            current_service = None

        for line_no, raw in enumerate(lines, 1):
            stripped = raw.strip()
            if not stripped or stripped.startswith("#"):
                continue
            top_level = not raw[:1].isspace()

            if top_level and stripped.startswith("service "):
                finish_service()
                parts = stripped.split(None, 2)
                if len(parts) >= 3:
                    current_service = {
                        "name": parts[1],
                        "executable": parts[2],
                        "disabled": False,
                        "path": rel,
                        "line": line_no,
                    }
                current_trigger = "<service>"
                continue

            if top_level:
                finish_service()
                if stripped.startswith("on "):
                    current_trigger = stripped[3:].strip()
                elif stripped.startswith("import "):
                    imports.append({"path": rel, "line": line_no, "target": stripped[7:].strip()})
                    current_trigger = "<top-level>"
                else:
                    current_trigger = "<top-level>"

            if current_service is not None and stripped == "disabled":
                current_service["disabled"] = True
                continue

            for prefix, bucket, verb in (("start ", starts, "start"), ("stop ", stops, "stop")):
                if stripped.startswith(prefix):
                    target = stripped[len(prefix) :].strip().split()[0]
                    if RADIO_INIT_RE.search(target):
                        row = {"path": rel, "line": line_no, "trigger": current_trigger, "target": target}
                        bucket.append(row)
                        controls.append({**row, "verb": verb})

            for prefix, verb in (("enable ", "enable"), ("restart ", "restart")):
                if stripped.startswith(prefix):
                    target = stripped[len(prefix) :].strip().split()[0]
                    if RADIO_INIT_RE.search(target):
                        controls.append(
                            {"path": rel, "line": line_no, "trigger": current_trigger, "target": target, "verb": verb}
                        )

            if stripped.startswith("setprop ctl.start ") or stripped.startswith("setprop ctl.stop "):
                parts = stripped.split()
                if len(parts) >= 3:
                    prop = parts[1]
                    target = parts[2]
                    if RADIO_INIT_RE.search(target):
                        controls.append(
                            {"path": rel, "line": line_no, "trigger": current_trigger, "target": target, "verb": prop}
                        )

        finish_service()

    services.sort(key=lambda row: (row["name"], row["path"], row["line"]))
    starts.sort(key=lambda row: (row["target"], row["path"], row["line"]))
    stops.sort(key=lambda row: (row["target"], row["path"], row["line"]))
    controls.sort(key=lambda row: (row["target"], row["verb"], row["path"], row["line"]))
    imports.sort(key=lambda row: (row["path"], row["line"]))
    return {"services": services, "starts": starts, "stops": stops, "controls": controls, "imports": imports}


def scan_shell_files(root: Path, context_lines: int = 8) -> list[dict[str, Any]]:
    """Record radio service controls in stock shell scripts without interpreting shell conditions."""
    rows: list[dict[str, Any]] = []
    if not root.exists():
        return rows

    for path in sorted(root.rglob("*.sh")):
        rel = path.relative_to(root).as_posix()
        try:
            lines = _read_text(path).splitlines()
        except (OSError, UnicodeError):
            continue
        history: list[str] = []
        for line_no, raw in enumerate(lines, 1):
            stripped = raw.strip()
            if not stripped or stripped.startswith("#"):
                continue

            verb: str | None = None
            target: str | None = None
            for prefix, parsed_verb in (("start ", "start"), ("stop ", "stop"), ("restart ", "restart")):
                if stripped.startswith(prefix):
                    parts = stripped[len(prefix) :].strip().split()
                    if parts:
                        verb = parsed_verb
                        target = parts[0]
                    break
            if stripped.startswith("setprop ctl.start ") or stripped.startswith("setprop ctl.stop "):
                parts = stripped.split()
                if len(parts) >= 3:
                    verb = parts[1]
                    target = parts[2]

            if verb and target and RADIO_INIT_RE.search(target):
                rows.append(
                    {
                        "path": rel,
                        "line": line_no,
                        "verb": verb,
                        "target": target,
                        "context": history[-context_lines:],
                    }
                )
            history.append(stripped)

    rows.sort(key=lambda row: (row["target"], row["verb"], row["path"], row["line"]))
    return rows


def derive_summary(evidence: dict[str, Any]) -> dict[str, Any]:
    properties = evidence.get("properties", [])
    init = evidence.get("init", {})
    services = init.get("services", [])
    starts = init.get("starts", [])
    controls = init.get("controls", [])

    multisim_values = sorted(
        {
            row.get("value", "")
            for row in properties
            if "multisim" in row.get("key", "").lower() and row.get("value", "")
        }
    )
    qcrild_services = sorted({row["name"] for row in services if "qcril" in row.get("name", "").lower()})
    explicit_qcrild_start_targets = sorted(
        {row["target"] for row in starts if "qcril" in row.get("target", "").lower()}
    )
    qcrild_activation_targets = sorted(
        {
            row["target"]
            for row in controls
            if row.get("verb") in ACTIVATION_VERBS and "qcril" in row.get("target", "").lower()
        }
        | set(explicit_qcrild_start_targets)
    )
    unstarted = sorted(set(qcrild_services) - set(qcrild_activation_targets))

    return {
        "multisim_values": multisim_values,
        "defined_qcrild_services": qcrild_services,
        "explicit_qcrild_start_targets": explicit_qcrild_start_targets,
        "qcrild_activation_targets": qcrild_activation_targets,
        "unstarted_defined_qcrild_services": unstarted,
        "recommended_runtime_instances_from_evidence": qcrild_activation_targets,
        "note": "Runtime recommendation is limited to stock init activation evidence (start/enable/restart/ctl.start); service definitions alone do not prove an instance should be started.",
    }


def render_markdown(evidence: dict[str, Any]) -> str:
    summary = evidence["summary"]
    lines = [
        "# RED Hydrogen One .118 radio init evidence",
        "",
        "This is a diagnostic evidence record, not a donor-derived radio configuration.",
        "",
        f"Stock archive SHA-256: `{evidence['authority']['stock_archive_sha256']}`",
        "",
        "## Summary",
        "",
        f"- Multi-SIM property values observed: `{summary['multisim_values']}`",
        f"- qcrild services defined by stock init: `{summary['defined_qcrild_services']}`",
        f"- qcrild instances explicitly started by stock init: `{summary['explicit_qcrild_start_targets']}`",
        f"- qcrild instances activated by stock init controls: `{summary['qcrild_activation_targets']}`",
        f"- Defined but not activated: `{summary['unstarted_defined_qcrild_services']}`",
        "",
        summary["note"],
        "",
        "## Relevant properties",
        "",
    ]
    for row in evidence["properties"]:
        lines.append(f"- `{row['path']}:{row['line']}` — `{row['key']}={row['value']}`")
    if not evidence["properties"]:
        lines.append("- None found.")

    lines.extend(["", "## Radio/IMS service definitions", ""])
    for row in evidence["init"]["services"]:
        lines.append(
            f"- `{row['path']}:{row['line']}` — `{row['name']}` -> `{row['executable']}`; disabled=`{row['disabled']}`"
        )
    if not evidence["init"]["services"]:
        lines.append("- None found.")

    lines.extend(["", "## Radio/IMS controls", ""])
    for row in evidence["init"].get("controls", []):
        lines.append(
            f"- `{row['path']}:{row['line']}` under `{row['trigger']}` — `{row['verb']} {row['target']}`"
        )
    if not evidence["init"].get("controls", []):
        lines.append("- None found.")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract RED .118 radio/RIL init evidence")
    parser.add_argument("--vendor-root", type=Path, required=True)
    parser.add_argument("--extra-property-file", type=Path, action="append", default=[])
    parser.add_argument("--stock-sha256", required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    properties = scan_property_files(args.vendor_root)
    properties.extend(scan_extra_property_files(args.extra_property_file))
    properties.sort(key=lambda row: (row["key"], row["path"], row["line"]))

    evidence: dict[str, Any] = {
        "schema_version": 2,
        "authority": {
            "stock_build": "H1A1000.082ho.01.00.10r.118",
            "stock_archive_sha256": args.stock_sha256,
            "source": "verified RED .118 stock vendor image plus explicitly supplied stock property files",
        },
        "properties": properties,
        "init": scan_init_files(args.vendor_root),
    }
    evidence["summary"] = derive_summary(evidence)

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    args.output_md.write_text(render_markdown(evidence), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
