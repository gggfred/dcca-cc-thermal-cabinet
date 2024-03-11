import boto3
from boto3.dynamodb.conditions import Key

import json

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

def lambda_handler(event, context):
    qty = event["qty"]
    id = event["unique_id"]

    # Specify the table name
    table_name = 'Measurement'

    # Get the table
    table = dynamodb.Table(table_name)

    try:
        # Specify the query parameters
        query_params = {
            'KeyConditionExpression' : Key('unique_id').eq(id),
            'ScanIndexForward' : False,  # Sort in descending order
            'Limit' : qty  # Limit the result to the last 12 records
        }

        items = table.query(**query_params)['Items']

        ans = []
        for item in items:
            ans.append({
                'timestamp' : item.get('timestamp'),
                'temperature' : float(item.get('temperature'))
            })

        # Crear el objeto JSON
        response_obj = {
            'status': "ok",
            'measures' : json.dumps(ans)
        }
    
        # TODO implement
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps(response_obj)
        }
        
    except Exception as e:
        print("EXCEPTION: \033[1;32;40m {}  \n".format(str(e)))
        return {
            "statusCode": 500,
            "body": json.dumps({'message': f'Error al procesar el archivo {e}'})
        }
        
