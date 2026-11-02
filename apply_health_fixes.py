"""
Migration script: apply_health_fixes.py
Updates existing health_ops.db with confirmed baseline lab values, hydration markers,
body-composition markers, and PTH marker.

This script is idempotent: running it multiple times produces no changes after the first run.
"""

import os
import sqlite3
import sys

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "health_ops.db")

def run_migration():
    if not os.path.exists(DB_PATH):
        print(f"Error: Database file not found at {DB_PATH}")
        sys.exit(1)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    added = []
    updated = []
    skipped = []
    conflicts = []

    # 1. HbA1c
    cursor.execute("SELECT marker_name, baseline_value, current_value, unit, notes FROM baselines WHERE marker_name = 'HbA1c'")
    row = cursor.fetchone()
    if row:
        _, base_val, cur_val, unit, notes = row
        target_base = 9.1
        target_cur = 7.1
        target_notes = "Most recent lab value Oct 2026 (confirmed); peak was 9.1"
        if base_val == target_base and cur_val == target_cur and notes == target_notes:
            skipped.append(("HbA1c", f"Already up-to-date (baseline={base_val}, current={cur_val})"))
        else:
            cursor.execute("""
                UPDATE baselines
                SET baseline_value = ?, current_value = ?, notes = ?
                WHERE marker_name = 'HbA1c'
            """, (target_base, cur_val, target_notes))
            updated.append(("HbA1c", f"Updated baseline: {base_val} -> {target_base}, kept current: {cur_val}, notes updated"))
    else:
        conflicts.append(("HbA1c", "Marker 'HbA1c' not found in database"))

    # 2. Weight
    cursor.execute("SELECT marker_name, baseline_value, current_value, unit, notes FROM baselines WHERE marker_name = 'Weight'")
    row = cursor.fetchone()
    target_weight_notes = "Visit 2 Oct 12 2026: 301.1 InBody / 299.4 BOD POD"
    if row:
        _, base_val, cur_val, unit, notes = row
        if base_val == 362.3 and cur_val == 301.1 and notes == target_weight_notes and unit == "lbs":
            skipped.append(("Weight", f"Already up-to-date (baseline=362.3, current=301.1, unit=lbs)"))
        else:
            cursor.execute("""
                UPDATE baselines
                SET baseline_value = 362.3, current_value = 301.1, unit = 'lbs', notes = ?
                WHERE marker_name = 'Weight'
            """, (target_weight_notes,))
            updated.append(("Weight", f"Updated baseline: {base_val} -> 362.3, current: {cur_val} -> 301.1, notes updated"))
    else:
        cursor.execute("""
            INSERT INTO baselines (marker_name, baseline_value, current_value, unit, notes)
            VALUES ('Weight', 362.3, 301.1, 'lbs', ?)
        """, (target_weight_notes,))
        added.append(("Weight", "Inserted baseline 362.3, current 301.1, unit lbs"))

    # 3. Hydration markers (add only if absent)
    hydration_markers = [
        ("Urine 24h Volume", 3762.0, 3762.0, "g/24h", "24h collection Oct 22, 2026 (~3.7 L); full collection confirmed by creatinine output"),
        ("Urine 24h Specific Gravity", 1.0173, 1.0173, "ratio", "Mid-range concentration; 24h average"),
        ("Urine 24h Osmolality", 450.5, 450.5, "mOsm/kg", "Mid-range concentrating work"),
        ("Urine 24h Creatinine", 66.7, 66.7, "mg/dL", "~2.5 g/day total; collection complete"),
        ("Morning Urine SG", 1.0155, 1.0155, "ratio", "First-morning sample"),
        ("Morning Urine Osmolality", 443.5, 443.5, "mOsm/kg", "First-morning sample"),
        ("Saliva Osmolality", 201.5, 201.5, "mOsm/kg", "Single morning snapshot"),
    ]

    for name, base_v, cur_v, unit, note in hydration_markers:
        cursor.execute("SELECT marker_name, baseline_value, current_value, unit, notes FROM baselines WHERE marker_name = ?", (name,))
        row = cursor.fetchone()
        if row:
            skipped.append((name, f"Already exists (baseline={row[1]}, current={row[2]})"))
        else:
            cursor.execute("""
                INSERT INTO baselines (marker_name, baseline_value, current_value, unit, notes)
                VALUES (?, ?, ?, ?, ?)
            """, (name, base_v, cur_v, unit, note))
            added.append((name, f"Added hydration marker: {base_v} {unit}"))

    # 4. Body-composition markers (add if missing, report conflicts)
    body_comp_markers = [
        ("Body Fat % (InBody)", 47.3, 47.3, "%", "Visit 2 baseline Oct 12 2026"),
        ("Body Fat % (BOD POD)", 46.0, 46.0, "%", "Visit 2 baseline Oct 12 2026"),
        ("Skeletal Muscle Index", 9.4, 9.4, "kg/m2", "Visit 2 baseline Oct 12 2026"),
        ("Phase Angle", 4.9, 4.9, "deg", "Visit 2 baseline Oct 12 2026"),
        ("Visceral Fat Area", 295.3, 295.3, "cm2", "Visit 2 baseline Oct 12 2026"),
        ("Resting Energy Expenditure", 2421.0, 2421.0, "kcal/day", "Visit 2 baseline Oct 12 2026"),
        ("ECW/TBW", 0.388, 0.388, "ratio", "Visit 2 baseline Oct 12 2026"),
    ]

    for name, base_v, cur_v, unit, note in body_comp_markers:
        cursor.execute("SELECT marker_name, baseline_value, current_value, unit, notes FROM baselines WHERE marker_name = ?", (name,))
        row = cursor.fetchone()
        if row:
            # Check for conflict
            if row[1] == base_v and row[2] == cur_v and row[3] == unit and row[4] == note:
                skipped.append((name, f"Already exists with exact values (baseline={base_v}, current={cur_v} {unit})"))
            else:
                conflicts.append((name, f"Existing values differ: got (base={row[1]}, cur={row[2]}, unit={row[3]}, notes={row[4]}), expected (base={base_v}, cur={cur_v}, unit={unit})"))
        else:
            cursor.execute("""
                INSERT INTO baselines (marker_name, baseline_value, current_value, unit, notes)
                VALUES (?, ?, ?, ?, ?)
            """, (name, base_v, cur_v, unit, note))
            added.append((name, f"Added body-composition marker: {base_v} {unit}"))

    # 5. PTH
    cursor.execute("SELECT marker_name, baseline_value, current_value, unit, notes FROM baselines WHERE marker_name = 'PTH'")
    row = cursor.fetchone()
    pth_note = "Recovered after parathyroidectomy; off Calcitriol; calcium 9.7 mg/dL"
    if row:
        _, base_val, cur_val, unit, notes = row
        if cur_val == 33.0 and pth_note in (notes or "") and unit == "pg/mL":
            skipped.append(("PTH", f"Already up-to-date (baseline={base_val}, current={cur_val} pg/mL)"))
        else:
            new_notes = f"{notes}; {pth_note}" if notes and pth_note not in notes else pth_note
            cursor.execute("""
                UPDATE baselines
                SET current_value = 33.0, unit = 'pg/mL', notes = ?
                WHERE marker_name = 'PTH'
            """, (new_notes,))
            updated.append(("PTH", f"Updated current_value: {cur_val} -> 33.0, notes updated"))
    else:
        cursor.execute("""
            INSERT INTO baselines (marker_name, baseline_value, current_value, unit, notes)
            VALUES ('PTH', 13.0, 33.0, 'pg/mL', ?)
        """, (pth_note,))
        added.append(("PTH", "Added PTH marker: baseline 13.0, current 33.0, pg/mL"))

    conn.commit()
    conn.close()

    print("=" * 60)
    print("MIGRATION SUMMARY")
    print("=" * 60)
    print(f"Added   : {len(added)}")
    for name, detail in added:
        print(f"  + [ADD] {name}: {detail}")
    print(f"Updated : {len(updated)}")
    for name, detail in updated:
        print(f"  * [UPD] {name}: {detail}")
    print(f"Skipped : {len(skipped)}")
    for name, detail in skipped:
        print(f"  - [SKIP] {name}: {detail}")
    if conflicts:
        print(f"Conflicts : {len(conflicts)}")
        for name, detail in conflicts:
            print(f"  ! [CONFLICT] {name}: {detail}")
    else:
        print("Conflicts : 0")
    print("=" * 60)
    return len(added), len(updated), len(skipped), len(conflicts)

if __name__ == "__main__":
    run_migration()
