import argparse
from pathlib import Path
import pandas as pd
from db import get_enrollment
from api import get_school_data
from transform import get_students, merge_data, summarize_top_schools, summarize_by_zip, summarize_by_size
from report import save_top_schools_chart, save_size_chart, save_excel_report


def main(args):
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)

    print("Fetching enrollment data from Oracle...")
    enrollment_df = get_enrollment()
    students_df = get_students(enrollment_df)
    print(f"  {len(students_df)} students")

    print("Loading middle school survey data...")
    survey_path = Path(__file__).parent / "data" / "survey_middle_schools.csv"
    survey_df = pd.read_csv(survey_path, dtype={'student_id': int, 'ncessch': str})
    print(f"  {len(survey_df)} survey records")

    print(f"Fetching school data from API (year={args.year}, fips='36,34')...")
    school_df = get_school_data(args.year)
    print(f"  {len(school_df)} school records")

    print("Merging and summarizing...")
    merged_df = merge_data(students_df, survey_df, school_df)
    top_schools = summarize_top_schools(merged_df)
    zip_summary = summarize_by_zip(merged_df)
    size_summary = summarize_by_size(merged_df)

    merged_csv = output / "merged.csv"
    merged_df.to_csv(merged_csv, index=False)
    print(f"  Saved {merged_csv}")

    print("Generating charts...")
    chart1 = save_top_schools_chart(top_schools, output)
    chart2 = save_size_chart(size_summary, output)

    print("Generating Excel report...")
    excel_path = save_excel_report(
        merged_df, top_schools, zip_summary, size_summary,
        [chart1, chart2], output,
    )

    print(f"\nDone. Outputs in {output}/")
    print(f"  {merged_csv.name}")
    print(f"  {chart1.name}")
    print(f"  {chart2.name}")
    print(f"  {excel_path.name}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate middle school outreach report."
    )
    parser.add_argument('--year', type=int, default=2019, help='CCD data year (default: 2019)')
    parser.add_argument('--output', type=str, default='reports/', help='Output directory (default: reports/)')
    args = parser.parse_args()
    main(args)
