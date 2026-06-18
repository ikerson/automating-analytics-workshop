"""
One-time script to generate the two pre-provided data files for the restructured workshop.

Run this from the repo root with the GSU network active (VPN if off-campus):
    python student_report/generate_data_files.py

Produces:
    student_report/data/enrollment.csv   — five-table Oracle enrollment JOIN
    student_report/data/schools.csv      — CCD directory 2019, NY+NJ, 9 columns

Both files are committed to the repo as static pre-provided data for Phase 1 (Sessions 3–7).
Delete this script after committing the files.
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

    print("\nDone. Commit both files to git:")
    print("  git add student_report/data/enrollment.csv student_report/data/schools.csv")
    print("  git commit -m 'add pre-provided data files for phase 1'")
    print("  git rm student_report/generate_data_files.py")
    print("  git commit -m 'remove data file generation helper'")


if __name__ == "__main__":
    main()
