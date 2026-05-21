from educationdata import EducationDataAPI

CCD_COLUMNS = [
    'ncessch',
    'school_name',
    'zip_mailing',
    'city_location',
    'state_location',
    'school_level',
    'enrollment',
    'lowest_grade_offered',
    'highest_grade_offered',
]


def get_school_data(year):
    api = EducationDataAPI()
    result = api.ccd_directory(year, fips='36,34')
    df = result.to_df()
    return df[CCD_COLUMNS].copy()
