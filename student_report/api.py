from educationdata import EducationDataAPI

CCD_COLUMNS = [
    'ncessch', 'school_name', 'zip_mailing',
    'enrollment', 'city_location', 'state_location',
]


def get_school_data(year, state_fips):
    api = EducationDataAPI()
    result = api.ccd_directory(year, fips=state_fips)
    df = result.to_df()
    return df[CCD_COLUMNS].copy()
