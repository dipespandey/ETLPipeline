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


def send_row_to_table(row: Series, rds: RDSWorks) -> None:
    """
    UseCase: HC Data
    Pass in the row and check in tables to see if muid exists already
    Handle 3 cases separately:
    1. abc@company.com, 1111111111
    2. abc@company.com, None
    3.            None, 1111111111
    Gotcha: email_muid == phone_muid == muid
    """
    # Handle case 1.
    if not pd.isnull(row["Email Address"]) and not pd.isnull(row["Phone"]):
        # both email and phone available in row
        print("email", row["Email Address"], "phone", row["Phone"])
        email_muid = rds.get_muid_from_table(
            table='identity_attributes', value=('value', row["Email Address"]), get='muid')
        phone_muid = rds.get_muid_from_table(
            table='identity_attributes', value=('value', row["Phone"]), get='muid')
        if email_muid is not None and phone_muid is not None:
            # muid is present against both attributes
            try:
                assert email_muid == phone_muid
                muid = email_muid
            except AssertionError as e:
                print("There seems to be some issue in your db. Please check your muid against email:{} and phone:{}".format(
                    row["Email Address"], row["Phone"]))
                pass
        elif email_muid is not None and phone_muid is None:
            # muid is present against email but not against phone
            muid = email_muid
            # Insert phone_muid to db
            rds.insert_sql(table="identity_attributes", attrs=[
                "muid", "attribute_type", "value", "hash_status", "client_id"], values=[
                muid, "phone", row["Phone"], 0, 5])

        elif email_muid is None and phone_muid is not None:
            # muid is present against phone but not against email
            muid = phone_muid
            # Insert email_muid to db
            rds.insert_sql(table="identity_attributes", attrs=[
                "muid", "attribute_type", "value", "hash_status", "client_id"], values=[
                muid, "email", row["Email Address"], 0, 5])
        else:
            # muid is not present against both email and phone
            # generate muid
            muid = rds.generate_muid()
            # Insert email_muid to db
            rds.insert_sql(table="identity_attributes", attrs=[
                "muid", "attribute_type", "value", "hash_status", "client_id"], values=[
                muid, "email", row["Email Address"], 0, 5])
            # Insert phone_muid to db
            rds.insert_sql(table="identity_attributes", attrs=[
                "muid", "attribute_type", "value", "hash_status", "client_id"], values=[
                muid, "phone", row["Phone"], 0, 5])

        if not pd.isnull(row["Location"]):
            # Insert phone_muid to db
            # if self.get_muid_from_table(table='data_attributes', value=row["Location"]) is None:
            rds.insert_sql(table="data_attributes", attrs=[
                "muid", "attribute_type", "value", "hash_status", "client_id"], values=[
                muid, "location", row["Location"], 0, 5])
            # else:
            #     print("Location already {} exists for muid {}".format(
            #         row["Location"], muid))
        else:
            print("Location not available for muid {}".format(muid))

    # Handle case 2.
    elif not pd.isnull(row["Email Address"]) and pd.isnull(row["Phone"]):
        # email available but phone unavailable in row
        print("email", row["Email Address"], "phone", row["Phone"])
        email_muid = rds.get_muid_from_table(
            table='identity_attributes', value=('value', row["Email Address"]), get='muid')
        if email_muid is None:
            print(email_muid)
            # muid not present against email
            # generate email
            email_muid = rds.generate_muid()
            # insert muid against email
            rds.insert_sql(table="identity_attributes", attrs=[
                "muid", "attribute_type", "value", "hash_status", "client_id"], values=[
                email_muid, "email", row["Email Address"], 0, 5])
        else:
            print("muid: {} already exists..".format(email_muid))
        if not pd.isnull(row["Location"]):
            # Insert location to db if not exists
            # if self.get_muid_from_table(table='identity_attributes', value=row["Location"]) is None:
            rds.insert_sql(table="data_attributes", attrs=[
                "muid", "attribute_type", "value", "hash_status", "client_id"], values=[
                email_muid, "Location", row["Location"], 0, 5])
            # else:
            #     print("Location {} exists for muid {}".format(
            #         row["Location"], email_muid))
        else:
            print("Location not available for muid {}".format(email_muid))

    # Handle case 3.
    elif pd.isnull(row["Email Address"]) and (not pd.isnull(row["Phone"])):
        # phone available but email unavailable in row
        phone_muid = rds.get_muid_from_table(
            table='identity_attributes', value=('value', row["Phone"]), get='muid')
        if phone_muid is None:
            # muid not present against phone
            # generate muid
            phone_muid = rds.generate_muid()
            # insert muid against phone
            rds.insert_sql(table="identity_attributes", attrs=[
                "muid", "attribute_type", "value", "hash_status", "client_id"], values=[
                phone_muid, "phone", row["Phone"], 0, 5])
        else:
            print("muid: {} already exists..".format(phone_muid))

        if not pd.isnull(row["Location"]):
            # Insert location to db if not exists
            # if self.get_muid_from_table(table='identity_attributes', value=row["Location"]) is None:
            rds.insert_sql(table="data_attributes", attrs=[
                "muid", "attribute_type", "value", "hash_status", "client_id"], values=[
                phone_muid, "location", row["Location"], 0, 5])
            # else:
            #     print("Location {} exists for muid {}".format(
            #         row["Location"], phone_muid))
        else:
            print("Location not available for muid {}".format(phone_muid))

    else:
        print("Email and Phone don't exist in row..")


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
