from rest_framework import serializers
from .models import (BwGeography, Gender, BwContentSources,
                     BwNetSentiment, BwEmotions, BwSentiments, BwVolume,
                     ClineCenter, YahooStockData, ShortInterest,)


class BwGeographySerializer(serializers.ModelSerializer):

    class Meta:
        model = BwGeography
        fields = '__all__'


class GenderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Gender
        fields = '__all__'



class BwContentSourcesSerializer(serializers.ModelSerializer):

    class Meta:
        model = BwContentSources
        fields = '__all__'


class BwNetSentimentSerializer(serializers.ModelSerializer):

    class Meta:
        model = BwNetSentiment
        fields = '__all__'


class BwEmotionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = BwEmotions
        fields = '__all__'


class BwSentimentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = BwSentiments
        fields = '__all__'


class BwVolumeSerializer(serializers.ModelSerializer):

    class Meta:
        model = BwVolume
        fields = '__all__'


class ClineCenterSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClineCenter
        fields = '__all__'


class YahooStockDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = YahooStockData
        fields = '__all__'


class ShortInterestSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShortInterest
        fields = '__all__'