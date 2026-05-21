import pandas as pd


def get_students(enrollment_df):
    return (
        enrollment_df[['student_id', 'first_name', 'last_name', 'zip', 'city', 'state']]
        .drop_duplicates(subset=['student_id'])
        .copy()
    )


def merge_data(students_df, survey_df, school_df):
    students_df = students_df.copy()
    survey_df = survey_df.copy()
    school_df = school_df.copy()

    students_df['zip'] = students_df['zip'].astype(str).str.zfill(5)
    school_df['zip_mailing'] = (
        school_df['zip_mailing'].astype(str).str.split('.').str[0].str.zfill(5)
    )
    survey_df['ncessch'] = survey_df['ncessch'].astype(str).str.split('.').str[0]
    school_df['ncessch'] = school_df['ncessch'].astype(str).str.split('.').str[0]

    merged = students_df.merge(survey_df, on='student_id', how='left')
    merged = merged.merge(school_df, on='ncessch', how='left')

    merged['school_size'] = pd.cut(
        merged['enrollment'],
        bins=[0, 300, 700, float('inf')],
        labels=['Small (<300)', 'Medium (300-700)', 'Large (700+)'],
    )

    return merged


def summarize_top_schools(merged_df):
    matched = merged_df.dropna(subset=['middle_school_name'])
    return (
        matched.groupby(['middle_school_name', 'city_location', 'zip_mailing', 'school_size'])
        .agg(student_count=('student_id', 'count'), school_enrollment=('enrollment', 'first'))
        .reset_index()
        .sort_values('student_count', ascending=False)
        .head(10)
    )


def summarize_by_zip(merged_df):
    matched = merged_df.dropna(subset=['zip_mailing'])
    return (
        matched.groupby(['zip_mailing', 'city_location'])
        .agg(student_count=('student_id', 'count'))
        .reset_index()
        .sort_values('student_count', ascending=False)
    )


def summarize_by_size(merged_df):
    return (
        merged_df.groupby('school_size', observed=True)
        .agg(student_count=('student_id', 'count'))
        .reset_index()
    )
