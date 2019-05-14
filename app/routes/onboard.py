"""
ETL API 1.0
onboard.py
..................
contains endpoints for onboarding works using the API
"""

from . import routes
from pprint import pprint
import pandas as pd
from pandas import DataFrame, Series
from app.models.rds import RDSWorks
from app.config import muid_creds


def get_df_from_onboarded_data(s3url, ) -> DataFrame:
    """
    Return a dataframe out of the onboarded data
    """
    try:
        print("Getting onboarded file from S3..")
        df = pd.read_excel(s3url)
        print("Got file..")
        pprint(df.head())
        return df
    except Exception as e:
        print(e)


def transform_df(df: DataFrame, cols_to_send: list, ) -> DataFrame:
    """
    Pass the original DataFrame and return a
    DataFrame with only the columns that need to be sent to RDS
    Eg: for HC: cols_to_send = ["Email Address", "Phone", "Location"]
    """
    return df[cols_to_send].drop_duplicates()


def test_run(s3_url: str) -> None:
    """
    Test run getting file from s3 and 
    sending the contents to RDS after some transformation
    using above classe
    """
    df = get_df_from_onboarded_data(s3url=s3_url)
    df_filtered = transform_df(
        df, cols_to_send=["Email Address", "Phone", "Location"])

    rds = RDSWorks(**muid_creds)

    rds.connect_to_db()
    # Send 10 rows to db
    df.apply(send_row_to_table, rds=rds, axis=1)
    rds.close_connection()
