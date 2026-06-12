"""校验并导出 A-H VoltageSegment。"""

import csv
from pathlib import Path

from .voltage_segments import (
    export_voltage_segments,
    get_mode_voltage_segments,
    validate_voltage_segments,
)


OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"


def main() -> int:
    rows = []
    segment_rows = []
    for mode in "ABCDEFGH":
        rows.extend(validate_voltage_segments(mode))
        export_voltage_segments(mode, OUTPUT_DIR / f"voltage_segments_{mode}.csv")
        model = get_mode_voltage_segments(mode)
        for segment in model.segments:
            segment_rows.append({
                "mode": mode,
                "segment_index": segment.index,
                "start_edge": segment.start_edge,
                "end_edge": segment.end_edge,
                "duration_expr": str(segment.duration_expr),
                "v1_state": segment.v1_state,
                "v2_state": segment.v2_state,
                "vL_expr": str(segment.vL_expr),
                "slope_expr": str(segment.slope_expr),
                "zero_duration_possible": segment.zero_duration_possible,
                "source": segment.source,
                "note": segment.note,
            })
    output = OUTPUT_DIR / "voltage_segment_validation.csv"
    fields = tuple(rows[0].keys())
    with output.open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    segments_output = OUTPUT_DIR / "voltage_segments_symbolic.csv"
    with segments_output.open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.DictWriter(stream, fieldnames=tuple(segment_rows[0].keys()))
        writer.writeheader()
        writer.writerows(segment_rows)
    print(f"Wrote {len(rows)} validation rows to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
