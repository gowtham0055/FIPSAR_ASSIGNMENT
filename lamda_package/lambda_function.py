import json
import psycopg2

def read_config():
    with open('config.json') as f:
        config = json.load(f)
    return config

def connect_to_database():
    config = read_config()
    db_host = config['DB_HOST']
    db_port = config['DB_PORT']
    db_user = config['DB_USER']
    db_password = config['DB_PASSWORD']
    db_name = config['DB_NAME']


    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        user=db_user,
        password=db_password,
        dbname=db_name
    )

    return conn

def lambda_handler(event, context):
    records = event['Records']
    
    try:
        connection = connect_to_database()
        cursor = connection.cursor()

        for record in records:
            body = json.loads(record['body'])
            height = body.get('height')
            weight = body.get('weight')

            query = "INSERT INTO person (height, weight) VALUES (%s, %s)"
            cursor.execute(query, (height, weight))
            connection.commit()

        cursor.close()
        connection.close()

        return {
            'statusCode': 200,
            'body': json.dumps('Data stored in the RDS database successfully.')
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps('Failed to store data in the RDS database.')
        }