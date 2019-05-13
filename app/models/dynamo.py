import boto3
from botocore.exceptions import ClientError
import datetime
from flask import jsonify
import json
import uuid
from functools import reduce


class Dynamo():
    def __init__(self):
        self.name = 'dynamodb'
        self.region = 'ap-southeast-1'

    def get_dynamodb_resource(self, ):
        self.dyn = boto3.resource(self.name, region_name=self.region)

    def create_table(self, name: str, ):
        try:
            table = self.dyn.create_table(
                TableName=name,
                KeySchema=[
                    {
                        'AttributeName': 'muid',
                        'KeyType': 'HASH'  # Partition key
                    },
                    {
                        'AttributeName': 'id',
                        'KeyType': 'RANGE'  # Sort key
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'muid',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'id',
                        'AttributeType': 'N'
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
            )

            # wait until the table exists
            table.meta.client.get_waiter('table_exists').wait(
                TableName=name)
            print('created table {}.'.format(name))

        except ClientError as e:
            # If there is the table already, the error will be skipped
            if e.response['Error']['Code'] != 'ResourceInUseException':
                raise e
            else:
                print("Resource Already In Use")

    def insert_record(self, table: str, record):
        table = self.dyn.Table(table)
        try:
            response = table.put_item(
                Item={
                    "id": uuid.uuid4().hex,
                    "muid": record.get('muid', 'N/A'),
                    "cuid": record.get('cuid', 'N/A'),
                    "timestamp": datetime.datetime.utcnow().strftime("%A, %d. %B %Y %I:%M%p"),
                    "page_url": record.get('page_url', 'N/A') or 'N/A',
                    "screen": record.get('screen', 'N/A') or 'N/A',
                    "browser_client": record.get('browser_client', 'N/A') or 'N/A',
                    "page_hostname": record.get('page_hostname', 'N/A') or 'N/A',
                    "referrer": record.get('referrer', 'N/A') or 'N/A',
                    "page_title": record.get('page_title', 'N/A') or 'N/A',
                    "meta_tag_content": record.get('meta_tag_content', 'N/A') or 'N/A',
                    "location": record.get('location', 'N/A') or 'N/A',
                    "ip_address": record.get('ip_address', 'N/A') or 'N/A',
                    "event_data":
                    {
                        "type": record.get("event_data", 'N/A').get("type", "N/A"),
                        "element": {
                            str(k): v or 'N/A' for k, v in record['event_data']['element'].items()
                        }if ('element' in record['event_data'] and isinstance(record['event_data']['element'], dict)) else 'N/A' or 'N/A'
                    }
                })
            print("Response = ", response)

        except ValueError:
            pass

    def read_record(self, table, cuid):
        table = self.dyn.Table(table)
        response = table.get_item(
            Key={
                'Id': str(cuid),
            }
        )
        if 'Item' in response:
            return response['Item']
        else:
            return None

    def update_record(self, old, new):
        raise NotImplementedError

    def delete_record(self, ):
        raise NotImplementedError

    def check_empty(self, record, key):
        """
        check if the record has empty value for a key 
        """
        raise NotImplementedError

    def __repr__(self, ):
        return "DynamoDb Myriad: {}".format(str(self.name))

    def __str__(self, ):
        return str(self.name)
