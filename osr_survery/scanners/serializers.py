from rest_framework import serializers
from .models import AppUser, Property, Scan

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ('property_name', 'address', 'lat', 'lon')


class NewScanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scan
        fields = ('user', 'property', 'image')

class ScanSerializer(serializers.ModelSerializer):
    class Meta:
        model= Scan
        fields = ('user', 'property', 'image', 'raw_text', 'scan_date')




