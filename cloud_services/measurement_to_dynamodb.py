import boto3
import json
from datetime import datetime
from dateutil import tz

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table("Measurement")

def lambda_handler(event, context):
    temperature = event["temperature"]
    epoch = event["epoch"]

    # Define a timezone
    timezone = tz.gettz("America/Guayaquil")

    datetime_from_epoch = datetime.fromtimestamp(epoch, tz=timezone)
    rtimestamp = datetime_from_epoch.strftime("%Y-%m-%d %H:%M:%S")

    # Generate a random integer as a unique identifier
    unique_id = "1"

    try:
        item = {
                "unique_id" : unique_id,
                "temperature" : temperature,
                "timestamp" : rtimestamp
            }

        table.put_item(Item = item)

        # Crear el objeto JSON
        response_obj = {
            'status': "ok"
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
        
