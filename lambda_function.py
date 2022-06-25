import json
import boto3
from boto3.dynamodb.conditions import Key, Attr


def lambda_handler(event, context):
    
    # DynamoDBのテーブルアクセスクラスを生成    
    dynamoDB = boto3.resource('dynamodb')
    table= dynamoDB.Table('dictionary')
    
    # return用メッセージ
    dict = {"returnMsg": "null"}
    
    routeKey = event['routeKey']
    
    # 複数件取得
    if routeKey == 'GET /items':
        response = table.scan()
        return response['Items']
    
    # 1件取得    
    elif routeKey == 'GET /items/{id}':
        id = event['pathParameters']['id']
        response = table.get_item(
            Key={
                'id': int(id)
            }
        )
        return response['Item']
    
    # 1件追加 or 更新
    elif routeKey == 'PUT /items':
        
        data = json.loads(event.get("body"))
        print(data)
        
        table.put_item(
            Item = {
                "id": int(data["id"]),
                "word": data["word"],
                "explanation": data["explanation"]
            }
        )
        dict["returnMsg"] = "PUT complete!"
        return json.dumps(dict)
    
    # 1件削除    
    elif routeKey == 'DELETE /items/{id}':
        id = event['pathParameters']['id']
        table.delete_item(
            Key={
                'id': int(id)
                
            }
        )
        dict["returnMsg"] = "DELETE complete!"
        return json.dumps(dict)
    
    # それ以外
    else:
        dict["returnMsg"] = "not match"
        return json.dumps(dict)
