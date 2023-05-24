import boto3


def create_table(table_name):
    # create a new DynamoDB client
    dynamodb = boto3.client(
        "dynamodb",
        endpoint_url="http://localhost:8000",
        aws_access_key_id="vishal",
        aws_secret_access_key="vishal",
    )
    # create the DynamoDB table if it doesn't exist
    # dynamodb.list_tables()["TableNames"] returns a list of table names
    if table_name not in dynamodb.list_tables()["TableNames"]:
        print("Creating table")
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {"AttributeName": "id", "KeyType": "HASH"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "id", "AttributeType": "S"},
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 10, "WriteCapacityUnits": 10},
        )
        return table
    else:
        print("Table already exists")
        dynamodb_resource = boto3.resource("dynamodb")
        return dynamodb_resource.Table(table_name)


# wait until the table exists

if __name__ == "__main__":
    table_name = "my-table"
    table = create_table(table_name)
    table.meta.client.get_waiter(
        "table_exists",
    ).wait(TableName=table_name)
    print("Table created successfully!")
