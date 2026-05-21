import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
import pytest
from transform import get_students, merge_data, summarize_top_schools, summarize_by_zip, summarize_by_size


@pytest.fixture
def enrollment_df():
    return pd.DataFrame({
        'student_id': [1, 1, 2],
        'first_name': ['Alice', 'Alice', 'Bob'],
        'last_name': ['Smith', 'Smith', 'Jones'],
        'zip': ['10001', '10001', '07030'],
        'city': ['New York', 'New York', 'Hoboken'],
        'state': ['NY', 'NY', 'NJ'],
        'course_name': ['Python 101', 'Data Analysis', 'Python 101'],
        'cost': [500, 600, 500],
        'enroll_date': ['2019-01-01', '2019-01-01', '2019-01-01'],
        'final_grade': ['A', 'B', 'A'],
    })


@pytest.fixture
def survey_df():
    return pd.DataFrame({
        'student_id': [1, 2],
        'middle_school_name': ['IS 71', 'Hoboken Middle School'],
        'ncessch': ['360007702472', '340183001982'],
    })


@pytest.fixture
def school_df():
    return pd.DataFrame({
        'ncessch': ['360007702472', '340183001982'],
        'school_name': ['IS 71', 'Hoboken Middle School'],
        'zip_mailing': ['10001', '07030'],
        'city_location': ['New York', 'Hoboken'],
        'state_location': ['NY', 'NJ'],
        'school_level': [2, 2],
        'enrollment': [450, 250],
        'lowest_grade_offered': [6, 6],
        'highest_grade_offered': [8, 8],
    })


def test_get_students_deduplicates(enrollment_df):
    result = get_students(enrollment_df)
    assert len(result) == 2


def test_get_students_columns(enrollment_df):
    result = get_students(enrollment_df)
    assert list(result.columns) == ['student_id', 'first_name', 'last_name', 'zip', 'city', 'state']


def test_merge_data_row_count(enrollment_df, survey_df, school_df):
    students = get_students(enrollment_df)
    result = merge_data(students, survey_df, school_df)
    assert len(result) == 2


def test_merge_data_school_size_bucket(enrollment_df, survey_df, school_df):
    students = get_students(enrollment_df)
    result = merge_data(students, survey_df, school_df).set_index('student_id')
    assert str(result.loc[1, 'school_size']) == 'Medium (300-700)'
    assert str(result.loc[2, 'school_size']) == 'Small (<300)'


def test_merge_data_zip_padding(school_df):
    students = pd.DataFrame({
        'student_id': [3],
        'first_name': ['Carol'],
        'last_name': ['Lee'],
        'zip': ['7030'],  # missing leading zero — should be padded to 07030
        'city': ['Hoboken'],
        'state': ['NJ'],
    })
    survey = pd.DataFrame({
        'student_id': [3],
        'middle_school_name': ['Hoboken Middle School'],
        'ncessch': ['340183001982'],
    })
    result = merge_data(students, survey, school_df)
    assert result.iloc[0]['school_name'] == 'Hoboken Middle School'


def test_merge_data_unmatched_student(enrollment_df, school_df):
    survey = pd.DataFrame({
        'student_id': [1],
        'middle_school_name': ['IS 71'],
        'ncessch': ['360007702472'],
    })
    students = get_students(enrollment_df)
    result = merge_data(students, survey, school_df)
    row2 = result[result['student_id'] == 2].iloc[0]
    assert pd.isna(row2['middle_school_name'])


def test_summarize_top_schools_columns(enrollment_df, survey_df, school_df):
    students = get_students(enrollment_df)
    merged = merge_data(students, survey_df, school_df)
    result = summarize_top_schools(merged)
    assert 'middle_school_name' in result.columns
    assert 'student_count' in result.columns
    assert len(result) <= 10


def test_summarize_by_zip_columns(enrollment_df, survey_df, school_df):
    students = get_students(enrollment_df)
    merged = merge_data(students, survey_df, school_df)
    result = summarize_by_zip(merged)
    assert 'zip_mailing' in result.columns
    assert 'student_count' in result.columns


def test_summarize_by_size_columns(enrollment_df, survey_df, school_df):
    students = get_students(enrollment_df)
    merged = merge_data(students, survey_df, school_df)
    result = summarize_by_size(merged)
    assert 'school_size' in result.columns
    assert 'student_count' in result.columns
