import json
import boto3

client = boto3.client('dynamodb')

def lambda_handler(event, context):
    # read the item
    data = client.get_item(
        TableName='tableForResumeSite',
        Key = {
            'SiteLink': {
                'S': 'enzezhou.com'
            }
        },
        ExpressionAttributeNames={
                '#name': 'Likes'
        },
        ProjectionExpression= '#name'
    )
    #extract likes and do the incremntation
    count = data.get('Item').get('Likes').get('N')
    count = int(count)+1
    
    #update likes
    update = client.update_item(
        TableName='tableForResumeSite',
        Key = {
                'SiteLink': {
                    'S': 'enzezhou.com'
                }
        },
        UpdateExpression='SET Likes = :count',
        ExpressionAttributeValues={
            ':count': {'N':str(count)}
        }
    )

    #send a message
    response = {
      'statusCode': 200,
      'body': str(count),
      'headers': {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': 'https://enzezhou.com'
      },
    }
    return response;
