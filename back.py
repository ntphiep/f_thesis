import json
from concurrent.futures import ThreadPoolExecutor
import boto3
import datetime
from boto3.dynamodb.conditions import Attr


from boto3.dynamodb.types import TypeSerializer
serializer = TypeSerializer()
def python_to_dynamo(python_object: dict) -> dict:
    return {
        k: serializer.serialize(v)
        for k, v in python_object.items()
    }


dynamodb = boto3.resource('dynamodb')
client = boto3.client('dynamodb')

source_policy_table = dynamodb.Table('exto-dev-user-policy-info')
source_report_table = dynamodb.Table('exto-dev-user-report-info')


def chunked(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i:i + size]


def lambda_handler(event, context):
    transact_items = []

    response_policy = source_policy_table.scan(
        ProjectionExpression='userId,userEmail'
    )
    items_policy = response_policy['Items']

    response_report = source_report_table.scan(
        ProjectionExpression='reportId,userId,parentFolderId',
        FilterExpression=(
            (Attr('parentFolderId').not_exists() | Attr('parentFolderId').eq(None)) &
            Attr('isFolder').eq(False)
        )
    )
    items_report = response_report['Items']

    for item in items_policy:
        userId = item.get('userId')
        userEmail = item.get('userEmail')
        
        f_saved_item = {
            "userId": userId,
            "reportId": "SAVED",
            "isFolder": True,
            "reportInfo": None,
            "reportName": "My Recipe",
            "createDate": int(datetime.datetime.now().timestamp()),
            "reportOwner": userEmail,
            "parentFolderId": None,
            "childs": set([ir.get('reportId') for ir in items_report if ir.get('reportId').partition("-")[0] == "SAVED" and ir.get('userId') == userId])
        }
        if not f_saved_item['childs']: # set trống không insert vào dynamo được
            f_saved_item['childs'] = None

        f_shared_item = {
            "userId": userId,
            "reportId": "SHARED",
            "isFolder": True,
            "reportInfo": None,
            "reportName": "Shared Recipe",
            "createDate": int(datetime.datetime.now().timestamp()),
            "reportOwner": userEmail,
            "parentFolderId": None,
            "childs": set([ir.get('reportId') for ir in items_report if ir.get('reportId').partition("-")[0] == "SHARED" and ir.get('userId') == userId ])
        }
        if not f_shared_item['childs']: # set trống không insert vào dynamo được
            f_shared_item['childs'] = None

        transact_items.append({
            'Put': {
                'TableName': 'exto-dev-user-report-info',
                'Item': python_to_dynamo(f_saved_item)
            }
        })

        transact_items.append({
            'Put': {
                'TableName': 'exto-dev-user-report-info',
                'Item': python_to_dynamo(f_shared_item)
            }
        })



    for batch_index, batch in enumerate(chunked(transact_items, 100), start=1):
        try:
            client.transact_write_items(TransactItems=batch)
            # logger.info(f"Batch {batch_index} inserted successfully")
        except Exception as e:
            print(e)
            # logger.error(f"Error in {batch_index}:\n {e.response['Error']['Message']}")

    if items_report:
        for item in items_report:
            source_report_table.update_item(
                Key={
                    'userId': item['userId'],
                    'reportId': item['reportId']
                },
                UpdateExpression="SET parentFolderId = :val",
                ExpressionAttributeValues={
                    ':val': item.get('reportId', '').partition("-")[0]
                }
            )


    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

