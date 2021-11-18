from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import PropertySerializer, ScanSerializer, NoteSerializer
from .models import AppUser, Property, Scan

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from rest_framework.decorators import api_view

from PIL import Image

from .tesseract_backend.main import scan_to_string
from .gis_distance import find_twenty_closest

import json

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")




### Property Views ###

@api_view(['GET', 'POST'])
def property_list(request):
    if request.method == 'GET':
        properties = Property.objects.all()

        # changes a "get" request from asking for a list to asking for a single object
        # why is this necessary?
        property_name = request.query_params.get("property_name", None)
        if property_name is not None:
            properties = properties.filter(property_name__icontains=property_name)

        property_serializer = PropertySerializer(properties, many=True)
        return JsonResponse(property_serializer.data, safe=False)

    if request.method == 'POST':
        property_data = JSONParser().parse(request)
        # good chance to check what is missing and send that as a response
        property_serializer = PropertySerializer(data=property_data)
        if property_serializer.is_valid():
            property_serializer.save()
            return JsonResponse(property_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(property_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


@api_view(['GET', 'PUT', 'DELETE'])
def property_detail(request, pk):
    try:
        property = Property.objects.get(pk=pk)
    except Property.DoesNotExist:
        return JsonResponse({"message": "A property with that ID cannot be found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        property_serializer = PropertySerializer(property)
        return JsonResponse(property_serializer.data)

    if request.method == 'PUT':
        property_data = JSONParser().parse(request)
        property_serializer = PropertySerializer(property, data=property_data)
        if property_serializer.is_valid():
            property_serializer.save()
            return JsonResponse({'message': 'Property updated succesfully'}, status=status.HTTP_204_NO_CONTENT)

    if request.method == 'DELETE':
        property.delete()


@api_view(['GET'])
def nearby_properties(request):
    # should return the top 20 nearby properties
     if request.method == 'GET':
        properties = Property.objects.all()
        print("The request looks like this: ")
        latitude = (request.query_params.get("latitude", None))
        longitude = (request.query_params.get("longitude", None))
        #measure the distance of all properties from user and return top 20 closest
        user_lat_lon = {"lat":latitude, "lon":longitude}
        closest_properties = find_twenty_closest(user_lat_lon, properties)
        closest_properties = Property.objects.filter(pk__in=closest_properties)
        property_serializer = PropertySerializer(closest_properties, many=True)
        return JsonResponse(property_serializer.data, safe=False)

### Scan Views ###

@api_view(['GET', 'POST'])
def scan_list(request):
    print("give me something ok?")
    if request.method == 'GET':
        scans = Scan.objects.all()
        scan_serializer = PropertySerializer(scans, many=True)
        return JsonResponse(scan_serializer.data, safe=False)

    if request.method == 'POST':
        # print("Are we posting at least?")
        # print(request.data)
        request_data = request.data
        #request_data = JSONParser().parse(request)
        # good chance to check what is missing and send that as a response
        # print("-------------------------------------------------------")
        # print("the hunt begins")
        scan_serializer = ScanSerializer(data=request_data, partial=True)
        # print("serializer made")
        scan_serializer.user = AppUser.objects.get(pk=request_data["user"])  
        # print("user added")
        scan_serializer.property = Property.objects.get(pk=request_data["property"])  
        # print("property added")  
        # print(scan_serializer.initial_data)
        if scan_serializer.is_valid():
            # print("better than you think")
            new_scan_object = scan_serializer.save()
            # print("here comes the image")
            # print(new_scan_object.image.name)
            # print(new_scan_object.image.path)
            just_the_image = Image.open(new_scan_object.image.path) # scan the imate 
            # just_the_image.show()
            # bw_image = just_the_image.convert("L")
            # bw_image.save("dorks.png")
            scan_text_found = scan_to_string(just_the_image)
            # print(scan_text_found)
            new_scan_object.raw_text = scan_text_found
            return_scan_serializer = ScanSerializer(new_scan_object) # needed to add the found text into the response
            scan_serializer.save() # save the unreviewed text to the database as well
            return JsonResponse(return_scan_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(scan_serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET', 'PUT', 'DELETE'])
def scan_detail(request, pk):
    try:
        scan = Scan.objects.get(pk=pk)
    except Scan.DoesNotExist:
        return JsonResponse({'message': 'This scan does not exist'}, status=status.HTTP_404_NOT_FOUND)

    # single specific scan - same as above
    # this needs a partial update for adding back the correct text from the web app
    if request.method == 'PUT':
        scan_data = JSONParser().parse(request)
        scan_serializer = ScanSerializer(scan, data=scan_data, partial=True)
        if scan_serializer.is_valid():
            scan_serializer.save()
            return JsonResponse(scan_serializer.data)
        return JsonResponse(scan_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'GET':
        scan_serializer = ScanSerializer(scan)
        return JsonResponse(scan_serializer.data)

    elif request.method == 'DELETE':
        scan.delete()
        return JsonResponse({'message': "Scan was deleted successfully"}, status=status.HTTP_204_NO_CONTENT)




@api_view(['GET', 'POST'])
def get_scans_by_property(request, pk): 

    try:
        property = Property.objects.get(pk=pk)
    except Property.DoesNotExist:
        return JsonResponse({"message": "A property with that ID cannot be found"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        scans = Scan.object.all()
        if scans is None:
            return JsonResponse({"message": "This property has no scans in the database"}, status=status.HTTP_404_NOT_FOUND)
        else:
            scans = scans.filter(property=property)
            scan_serializer = ScanSerializer(scans, many=True)
            return JsonResponse(scan_serializer.data, safe=False)

    if request.method == 'POST':
        scan_data = JSONParser().parse(request)
        # good chance to check what is missing and send that as a response
        scan_serializer = ScanSerializer(data=scan_data)
        if scan_serializer.is_valid():
            scan_serializer.save()
            return JsonResponse(scan_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(scan_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        
class PostNote(APIView):
    def get(self, request):
        data = {
            'first_name': 'grant',
            'last_name': 'zhu'
        }
        return Response(data)

    def post(self, request):
        request_data = request.data

        serializer = NoteSerializer(data=request_data)
        serializer.user = AppUser.objects.get(pk=request_data["user"])   

        if serializer.is_valid(raise_exception=True):
            serializer.save()

        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
