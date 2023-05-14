from django.http import JsonResponse
from .models import Tutorial
from .serializers import TutorialSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response


# decorator is something we write above functions to describe its functionality
@api_view(["GET", "POST"])
def tutorial_list(request):
    if request.method == "GET":
        tutorials = Tutorial.objects.all()
        serializer = TutorialSerializer(tutorials, many=True)
        # JsonResponse is a Django class that allows us to return JSON objects from the API
        return Response(serializer.data)
    if request.method == "POST":
        serializer = TutorialSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Response is a REST framework class that allows us to return JSON objects from the API
            return Response(serializer.data, status=201)


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
