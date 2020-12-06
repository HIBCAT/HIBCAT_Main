from django.shortcuts import render
from django.http.response import HttpResponse
from django.template import loader
from .models import (BwGeography, Gender, BwContentSources, BwNetSentiment, BwEmotions, BwSentiments, BwVolume,
                     ClineCenter, YahooStockData, ShortInterest,)

# Create your views here.
