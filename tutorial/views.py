from django.http import JsonResponse
from .models import Tutorial
from .serializers import TutorialSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

import requests
import boto3
from django.http import HttpResponse

import uuid

# dynamodb = boto3.client("dynamodb", endpoint_url="http://localhost:8000")
dynamodb_resource = boto3.resource("dynamodb")


'''def store_data(request):
    # make API request and get data
    response = requests.get("https://localhost:7000/tutorials/")
    data = response.json()

    # create a new DynamoDB client

    table_name = "my-table"
    # create the DynamoDB table if it doesn't exist
    if table_name not in dynamodb.tables.all():
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {"AttributeName": "id", "KeyType": "HASH"},
            ],
            AttributeDefintion=[
                {"AttributeName": "id", "AttributeType": "S"},
                {"AttributeName": "tutorial_title", "AttributeType": "S"},
                {"AttributeName": "tutorial_content", "AttributeType": "S"},
                {"AttributeName": "tutorial_published", "AttributeType": "S"},
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 10, "WriteCapacityUnits": 10},
        )
    # wait until the table exists
    table.meta.client.get_waiter("table_exists").wait(TableName=table_name)
    # create a new item in the DynamoDB table
    """item = {
        "id": {"S": data[0]["id"]},
        "tutorial_title": {"S": data[0]["tutorial_title"]},
        "tutorial_content": {"S": data[0]["tutorial_content"]},
        "tutorial_published": {"S": data[0]["tutorial_published"]},
    }
    dynamodb.put_item(TableName="my-table", Item=item)"""
    # Store the data in DynamoDB
    with dynamodb_resource.Table(table_name).batch_writer() as batch:
        for item in data:
            batch.put_item(Item=item)

    # return a response to the client
    return HttpResponse("Data stored successfully")'''


# decorator is something we write above functions to describe its functionality
@api_view(["GET", "POST"])
def tutorial_list(request):
    if request.method == "GET":
        tutorials = Tutorial.objects.all()
        serializer = TutorialSerializer(tutorials, many=True)
        # JsonResponse is a Django class that allows us to return JSON objects from the API
        return Response(serializer.data)
    if request.method == "POST":
        table = dynamodb_resource.Table("my-table")
        item = {
            "id": str(uuid.uuid1()),
            "tutorial_title": request.data["tutorial_title"],
            "tutorial_content": request.data["tutorial_content"],
            "tutorial_published": request.data["tutorial_published"],
        }
        table.put_item(Item=item)
        """serializer = TutorialSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Response is a REST framework class that allows us to return JSON objects from the API
            return Response(serializer.data, status=201)"""
        return Response(item, status=201)


"""Response gives rest framework interface to show the response on the web page 
but JsonResponse just shows json formatted data on the web page"""


@api_view(["GET", "PUT", "DELETE"])
def tutorial_ind(request, pk):
    # pk is the primary key of the tutorial
    try:
        tutorial = Tutorial.objects.get(pk=pk)
    except Tutorial.DoesNotExist:
        return Response(status=404)
    if request.method == "GET":
        serializer = TutorialSerializer(tutorial)
        return Response(serializer.data)
    if request.method == "PUT":
        serializer = TutorialSerializer(tutorial, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    if request.method == "DELETE":
        tutorial.delete()
        return Response(status=204)
