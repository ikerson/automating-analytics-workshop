import argparse
from pathlib import Path
from db import get_enrollment
from api import get_school_data
from transform import merge_data, summarize_by_course, summarize_by_school
from report import save_enrollment_chart, save_school_chart, save_excel_report


def main(args):
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)

    print("Fetching enrollment data from Oracle...")
    enrollment_df = get_enrollment()
    print(f"  {len(enrollment_df)} enrollment records")

    print(f"Fetching school data from API (year={args.year}, state={args.state})...")
    school_df = get_school_data(args.year, args.state)
    print(f"  {len(school_df)} school records")

    print("Merging and summarizing...")
    merged_df = merge_data(enrollment_df, school_df)
    course_summary = summarize_by_course(merged_df)
    school_summary = summarize_by_school(merged_df)

    merged_csv = output / "merged.csv"
    merged_df.to_csv(merged_csv, index=False)
    print(f"  Saved {merged_csv}")

    print("Generating charts...")
    chart1 = save_enrollment_chart(course_summary, output)
    chart2 = save_school_chart(school_summary, output)

    print("Generating Excel report...")
    excel_path = save_excel_report(
        merged_df, course_summary, school_summary,
        [chart1, chart2], output,
    )

    print(f"\nDone. Outputs in {output}/")
    print(f"  {merged_csv.name}")
    print(f"  {chart1.name}")
    print(f"  {chart2.name}")
    print(f"  {excel_path.name}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate student enrollment and school data report."
    )
    parser.add_argument(
        '--year', type=int, default=2019,
        help='CCD data year (default: 2019)',
    )
    parser.add_argument(
        '--state', type=int, default=36,
        help='State FIPS code (default: 36 = New York)',
    )
    parser.add_argument(
        '--output', type=str, default='reports/',
        help='Output directory (default: reports/)',
    )
    args = parser.parse_args()
    main(args)
