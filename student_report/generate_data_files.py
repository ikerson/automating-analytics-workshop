"""
Author-only script — run by the workshop author, not participants.

Regenerates the two pre-provided static data files for Phase 1 (Sessions 3–7):
    student_report/data/enrollment.csv   — five-table Oracle enrollment JOIN
    student_report/data/schools.csv      — CCD directory 2019, NY+NJ, 9 columns

Both files are committed to the repo so participants can work through Phase 1
without a database or API connection. This script is kept (not deleted) so the
static files can be refreshed when the source data changes.

Requires: the GSU network (VPN if off-campus) for the Oracle query, plus reachability
to the Urban Institute API for the school directory. Run from the repo root:
    python student_report/generate_data_files.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from db import get_enrollment
from api import get_school_data

DATA_DIR = Path(__file__).parent / "data"


def main():
    print("Generating enrollment.csv (requires GSU network)...")
    enrollment_df = get_enrollment()
    out = DATA_DIR / "enrollment.csv"
    enrollment_df.to_csv(out, index=False)
    print(f"  Saved {out}  ({len(enrollment_df)} rows)")

    print("Generating schools.csv (Urban Institute API)...")
    school_df = get_school_data(2019)
    out = DATA_DIR / "schools.csv"
    school_df.to_csv(out, index=False)
    print(f"  Saved {out}  ({len(school_df)} rows)")

    print("\nDone. Commit the refreshed files to git:")
    print("  git add student_report/data/enrollment.csv student_report/data/schools.csv")
    print("  git commit -m 'refresh pre-provided data files'")


if __name__ == "__main__":
    main()
