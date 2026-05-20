import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path


def save_enrollment_chart(summary_df, output_dir):
    path = Path(output_dir) / "enrollment_by_course.png"
    _, ax = plt.subplots(figsize=(10, 5))
    ax.bar(summary_df['course_name'], summary_df['student_count'], color='steelblue')
    ax.set_xlabel("Course")
    ax.set_ylabel("Number of Students")
    ax.set_title("Student Enrollment by Course")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    return path


def save_school_chart(school_summary_df, output_dir):
    path = Path(output_dir) / "students_by_school_area.png"
    _, ax = plt.subplots(figsize=(10, 5))
    ax.barh(
        school_summary_df['school_name'],
        school_summary_df['student_count'],
        color='teal',
    )
    ax.set_xlabel("Number of Students")
    ax.set_title("Students by Nearby School (Top 10 by ZIP Match)")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    return path


def save_excel_report(merged_df, course_summary_df, school_summary_df, chart_paths, output_dir):
    from openpyxl import load_workbook
    from openpyxl.drawing.image import Image as XLImage

    path = Path(output_dir) / "student_report.xlsx"
    with pd.ExcelWriter(path, engine='openpyxl') as writer:
        merged_df.to_excel(writer, sheet_name='Merged Data', index=False)
        course_summary_df.to_excel(writer, sheet_name='By Course', index=False)
        school_summary_df.to_excel(writer, sheet_name='By School Area', index=False)

    wb = load_workbook(path)
    ws = wb.create_sheet('Charts')
    row = 1
    for chart_path in chart_paths:
        img = XLImage(str(chart_path))
        ws.add_image(img, f'A{row}')
        row += 30
    wb.save(path)
    return path
