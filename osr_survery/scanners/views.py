from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import viewsets
from .serializers import PropertySerializer, ScanSerializer
from .models import Property, Scan

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from rest_framework.decorators import api_view

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




### Scan Views ###

@api_view(['GET', 'POST'])
def scan_list(request):
    pass
    #return all scans or add a new one - same as above




@api_view(['GET', 'PUT', 'DELETE'])
def scan_detail(request, pk):
    pass
    # single specific scan - same as above




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


        
