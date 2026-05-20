import pandas as pd


def merge_data(enrollment_df, school_df):
    enrollment_df = enrollment_df.copy()
    school_df = school_df.copy()
    enrollment_df['zip'] = enrollment_df['zip'].astype(str).str.zfill(5)
    school_df['zip_mailing'] = school_df['zip_mailing'].astype(str).str.zfill(5)
    return enrollment_df.merge(
        school_df,
        left_on='zip',
        right_on='zip_mailing',
        how='left',
    )


def summarize_by_course(df):
    return (
        df.groupby('course_name')
        .agg(student_count=('student_id', 'count'), avg_cost=('cost', 'mean'))
        .reset_index()
        .sort_values('student_count', ascending=False)
    )


def summarize_by_school(df):
    matched = df.dropna(subset=['school_name'])
    return (
        matched.groupby('school_name')
        .agg(
            student_count=('student_id', 'count'),
            school_enrollment=('enrollment', 'first'),
        )
        .reset_index()
        .sort_values('student_count', ascending=False)
        .head(10)
    )
