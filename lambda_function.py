import json
import boto3
import uuid

def lambda_handler(event, context):

    # 1. 入力パラメータの値をリストに格納
    required_params = ['reviewText', 'userName', 'mailAddress']
    # 2. 未入力パラメータをリストに格納(リストが空の場合全て入力されている)
    param_empty_check = [
        param for param in required_params 
        if param not in event or not str(event[param]).strip()
        ]

    # 3. 入力パラメータのチェック
    if param_empty_check:
        return {
            'statusCode': 400,
            'body': json.dumps('param does not exist')
        }
    
    # 4.入力パラメータの取得
    reviewText = event["reviewText"]  # 問い合わせの内容
    userName = event["userName"]  # 問い合わせの投稿者名
    mailAddress = event["mailAddress"]  # 問い投稿者のメールアドレス

    # 5.idの生成（uuidを取得）
    item_id = str(uuid.uuid4()) 
    
    # 6.DynamoDBリソースの初期化
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('lnquiryTable')
    
    # 7.DynamoDBに更新するitemの内容を辞書で定義
    item = {
        'id': item_id,
        'reviewText': reviewText,
        'userName': userName,
        'mailAddress': mailAddress
    }
    
    try:
        # 8.DynamoDBにデータを保存
        table.put_item(Item=item)
    except Exception as e:
        # 9.エラーが発生した場合、ステータスコード500（内部サーバエラー）を返す
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error saving item to DynamoDB: {str(e)}')
        }
    
    # 10ステータスコード200（正常終了）を返す
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'lnquiryTable saved successfully!',
            'id': item_id
        })
    }
