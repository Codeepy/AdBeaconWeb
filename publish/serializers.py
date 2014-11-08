__author__ = 'Abdu'

from publish.models import CompanyDetail, Advertisement, BeaconDevice
from rest_framework import serializers


class AdvtSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = ('pic', 'beacon', 'from_date', 'to_date')

class DevSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeaconDevice
        fields = ('uuid', 'location', 'postcode', 'longitude', 'latitude')

