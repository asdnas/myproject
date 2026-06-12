"""导出 traditional TPS 的论文用 A-H 开通/关断电流总表。"""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

import sympy as sp

from .current_solver import derive_all_mode_currents
from .switch_event_mapping import compare_dg_confirmed_currents_to_paper
from .switching_current_extractor import build_switching_current_rows
from .symbols import D1, D2, L, V1, V2, fs, n, phi


BASE = Path(__file__).resolve().parent
DOCS = BASE / "docs"
OUTPUTS = BASE / "outputs"
SYMPY_LOCALS = {
    symbol.name: symbol
    for symbol in (D1, D2, phi, V1, V2, n, L, fs)
}


def build_paper_rows() -> tuple[list[dict], list[dict]]:
    on_all, off_all, _ = build_switching_current_rows()
    on_rows = []
    for row in on_all:
        if row["mapping_confidence"] != "confirmed":
            continue
        expr = _parse(row["current_expr"])
        on_rows.append({
            "mode": row["mode"],
            "switch_event": row["switch_event"],
            "switch_name": row["switch_name"],
            "edge_index": row["edge_index"],
            "edge_current_name": row["edge_current_name"],
            "current_expr": str(expr),
            "current_latex": sp.latex(expr),
            "confidence": "confirmed_from_fig3_mapping",
            "note": "来自已推导 VoltageEdge 边界电流；图3关键开通事件映射确认。",
        })
    off_rows = []
    for row in off_all:
        expr = _parse(row["current_expr"])
        off_rows.append({
            "mode": row["mode"],
            "candidate_switch_event": row["candidate_switch_event"],
            "switch_name": row["switch_name"],
            "edge_index": row["edge_index"],
            "edge_current_name": row["edge_current_name"],
            "current_expr": str(expr),
            "current_latex": sp.latex(expr),
            "turn_off_index_expr": str(sp.Abs(expr)),
            "mapping_confidence": "inferred",
            "note": "ideal boundary current；忽略 dead time；由 H 桥互补规则推得。",
        })
    return on_rows, off_rows


def build_table1_rows(on_rows: list[dict]) -> list[dict]:
    """复用现有论文表1对照逻辑，输出有量纲表达式。"""

    M = sp.symbols("M", real=True)
    current_base = V1 / (4 * fs * L)
    normalized = {
        "D": {
            "tS1": D1 * (M - 1) - 2 * M * phi,
            "tS4": -(D1 * (M + 1) + 2 * M * phi - 2 * M),
            "tQ1": D2 * (M + 1) + 2 * phi - 2,
            "tQ4": D2 * (M - 1) + 2 * phi,
        },
        "G": {
            "tS1": -(D1 - M * D2),
            "tS4": -(D1 - M * D2),
            "tQ1": D2 * (M - 1) - 2 * phi,
            "tQ4": D2 * (M - 1) + 2 * phi,
        },
    }
    existing_diffs = compare_dg_confirmed_currents_to_paper()
    indexed = {(row["mode"], row["switch_event"]): row for row in on_rows}
    rows = []
    for mode in ("D", "G"):
        for event in ("tS1", "tS4", "tQ1", "tQ4"):
            generated = _parse(indexed[(mode, event)]["current_expr"])
            paper = sp.simplify(
                current_base * normalized[mode][event].subs(M, n * V2 / V1)
            )
            diff = sp.simplify(generated - paper)
            rows.append({
                "mode": mode,
                "event": event,
                "generated_expr": str(generated),
                "paper_expr": str(paper),
                "diff_expr": str(diff),
                "match_status": "PASS" if diff == 0 and existing_diffs[mode][event] == 0 else "FAIL",
                "note": "论文表1表达式按 M=nV2/V1、基值 V1/(4fsL) 恢复为有量纲形式。",
            })
    return rows


def validate_sources(on_rows: list[dict], off_rows: list[dict]) -> list[dict]:
    csv_currents = _read_csv(OUTPUTS / "mode_currents_symbolic.csv")
    available = {
        (row["mode"], row["current_name"]): _parse(row["current_expr"])
        for row in csv_currents
    }
    checks = []
    for kind, rows in (("turn_on", on_rows), ("turn_off", off_rows)):
        for row in rows:
            key = (row["mode"], row["edge_current_name"])
            diff = sp.simplify(_parse(row["current_expr"]) - available[key])
            checks.append({
                "kind": kind, "mode": row["mode"],
                "event": row.get("switch_event", row.get("candidate_switch_event")),
                "edge_current_name": row["edge_current_name"],
                "exists_in_mode_currents_csv": key in available,
                "difference_from_mode_current": diff,
                "pass": key in available and diff == 0,
            })
    return checks


def export_all() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    on_rows, off_rows = build_paper_rows()
    table1_rows = build_table1_rows(on_rows)
    source_checks = validate_sources(on_rows, off_rows)
    if not all(row["pass"] for row in source_checks):
        raise RuntimeError("论文表中存在不来自 mode_currents_symbolic.csv 的电流。")
    _write_csv(OUTPUTS / "AH_turn_on_current_table_for_paper.csv", on_rows)
    _write_csv(OUTPUTS / "AH_turn_off_current_table_for_paper.csv", off_rows)
    _write_csv(OUTPUTS / "paper_table1_comparison.csv", table1_rows)
    _write_turn_on_doc(on_rows)
    _write_turn_off_doc(off_rows)
    _write_table1_doc(table1_rows)
    _write_final_check(on_rows, off_rows, table1_rows, source_checks)


def _write_turn_on_doc(rows: list[dict]) -> None:
    lines = [
        "# A-H Traditional TPS 开通电流论文总表", "",
        "仅列论文图3映射确认的 `tS1/tS4/tQ1/tQ4`。全部表达式来自已推导的 `I0...I8`。", "",
    ]
    for mode in "ABCDEFGH":
        lines += [f"## Mode {mode}", "",
                  "| event | switch | edge | boundary current | plain/simplified expression | LaTeX | source |",
                  "|---|---|---:|---|---|---|---|"]
        for row in (r for r in rows if r["mode"] == mode):
            lines.append(
                f"| `{row['switch_event']}` | {row['switch_name']} | {row['edge_index']} | "
                f"`{row['edge_current_name']}` | `{row['current_expr']}` | "
                f"${row['current_latex']}$ | confirmed_from_fig3_mapping |"
            )
        lines.append("")
    lines += ["## LaTeX 表", "", "```latex", r"\begin{longtable}{ccccc}", 
              r"Mode & Event & Edge & Boundary current & Current expression \\", r"\hline"]
    for row in rows:
        lines.append(
            f"{row['mode']} & {row['switch_event']} & {row['edge_index']} & "
            f"{row['edge_current_name']} & ${row['current_latex']}$ \\\\"
        )
    lines += [r"\end{longtable}", "```", ""]
    (DOCS / "AH_TURN_ON_CURRENT_TABLE_FOR_PAPER.md").write_text("\n".join(lines), encoding="utf-8")


def _write_turn_off_doc(rows: list[dict]) -> None:
    lines = [
        "# A-H Traditional TPS 关断电流论文总表", "",
        "全部关断事件映射均为 `inferred`。电流定义为忽略死区的 ideal boundary current；"
        "`turn_off_index=Abs(Ioff)`。", "",
    ]
    for mode in "ABCDEFGH":
        lines += [f"## Mode {mode}", "",
                  "| candidate event | switch | edge | boundary current | plain/simplified expression | LaTeX | turn-off index | confidence |",
                  "|---|---|---:|---|---|---|---|---|"]
        for row in (r for r in rows if r["mode"] == mode):
            lines.append(
                f"| `{row['candidate_switch_event']}` | {row['switch_name']} | {row['edge_index']} | "
                f"`{row['edge_current_name']}` | `{row['current_expr']}` | ${row['current_latex']}$ | "
                f"`{row['turn_off_index_expr']}` | inferred |"
            )
        lines.append("")
    lines += ["## LaTeX 表", "", "```latex", r"\begin{longtable}{ccccc}", 
              r"Mode & Candidate off event & Edge & Boundary current & Current expression \\", r"\hline"]
    for row in rows:
        lines.append(
            f"{row['mode']} & {row['candidate_switch_event']} & {row['edge_index']} & "
            f"{row['edge_current_name']} & ${row['current_latex']}$ \\\\"
        )
    lines += [r"\end{longtable}", "```", ""]
    (DOCS / "AH_TURN_OFF_CURRENT_TABLE_FOR_PAPER.md").write_text("\n".join(lines), encoding="utf-8")


def _write_table1_doc(rows: list[dict]) -> None:
    lines = [
        "# 论文表1 D/G 开通电流最终核对", "",
        "仅核对已有论文表1数据的 D/G 四个关键开通事件；未编造其他模式论文表达式。", "",
        "| mode | event | generated expression | paper expression | diff | status |",
        "|---|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['mode']} | {row['event']} | `{row['generated_expr']}` | "
            f"`{row['paper_expr']}` | `{row['diff_expr']}` | **{row['match_status']}** |"
        )
    lines.append("")
    (DOCS / "PAPER_TABLE1_COMPARISON.md").write_text("\n".join(lines), encoding="utf-8")


def _write_final_check(on_rows, off_rows, table1_rows, source_checks) -> None:
    solutions = derive_all_mode_currents()
    on_counts = Counter(row["mode"] for row in on_rows)
    off_counts = Counter(row["mode"] for row in off_rows)
    lines = [
        "# Traditional TPS 最终符号公式检查", "",
        f"- A-H 均有 I0...I8：{'PASS' if all(len(s.currents) == 9 for s in solutions.values()) else 'FAIL'}",
        f"- A-H 均有 tS1/tS4/tQ1/tQ4：{'PASS' if all(on_counts[m] == 4 for m in 'ABCDEFGH') else 'FAIL'}",
        f"- A-H 均有 8 个 inferred 关断事件：{'PASS' if all(off_counts[m] == 8 for m in 'ABCDEFGH') else 'FAIL'}",
        f"- 所有输出电流来自 mode_currents_symbolic.csv：{'PASS' if all(r['pass'] for r in source_checks) else 'FAIL'}",
        f"- 未凭空生成新电流：{'PASS' if all(r['pass'] for r in source_checks) else 'FAIL'}",
        f"- D/G 论文表1核对：{'PASS' if all(r['match_status'] == 'PASS' for r in table1_rows) else 'FAIL'}", "",
        "## 论文使用建议", "",
        "- `AH_TURN_ON_CURRENT_TABLE_FOR_PAPER.md` 中 confirmed 开通公式可直接用于论文。",
        "- `AH_TURN_OFF_CURRENT_TABLE_FOR_PAPER.md` 必须标注为 inferred、ideal boundary current、dead time ignored。",
        "- 建议人工复核图3未直接标注的关断事件命名，以及实际含死区时的关断电流取值时刻。",
        "- A/C/E/F/H 没有论文表1对照数据，未进行外部公式核对。", "",
    ]
    (DOCS / "FINAL_SYMBOLIC_FORMULA_CHECK.md").write_text("\n".join(lines), encoding="utf-8")


def _read_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def _parse(text: str) -> sp.Expr:
    return sp.sympify(text, locals=SYMPY_LOCALS)


def _write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=tuple(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    export_all()
    print(f"已生成论文用开通/关断电流总表到 {DOCS} 和 {OUTPUTS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
