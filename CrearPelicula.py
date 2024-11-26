import boto3
import uuid
import os
import json

def lambda_handler(event, context):
    # Entrada (json)
    print(event) # Log json en CloudWatch
        
    try:
        tenant_id = event['body']['tenant_id']
        pelicula_datos = event['body']['pelicula_datos']
        nombre_tabla = os.environ["TABLE_NAME"]
        # Proceso
        uuidv4 = str(uuid.uuid4())
        pelicula = {
            'tenant_id': tenant_id,
            'uuid': uuidv4,
            'pelicula_datos': pelicula_datos
        }
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(nombre_tabla)
        response = table.put_item(Item=pelicula)
        # Salida (json)
        
        print(json.dumps({
            'tipo': "INFO",
            'log_datos': {
                'message': "Pelicula creada exitosamente",
                'pelicula': pelicula
            }
        })
        )
         # Log json en CloudWatch
        
        return {
            'statusCode': 200,
            'pelicula': pelicula,
            'response': response
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'tipo': "ERROR",
            'log_datos': {
                'message': "Error encontrado al crear la pelicula",
                'error': str(e)
            }
        }
