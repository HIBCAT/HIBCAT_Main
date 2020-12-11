from django.shortcuts import render
from django.http.response import HttpResponse
from django.template import loader
from django.views import View
import pandas as pd
from rest_pandas import PandasSimpleView

from .models import (BwGeography, Gender, BwContentSources,
                     BwNetSentiment, BwEmotions, BwSentiments, BwVolume,
                     ClineCenter, YahooStockData, ShortInterest,)

# Create your views here.
class SMOperations(PandasSimpleView):

    yahoo_stock_data = YahooStockData.objects.all().values()
    short_interest = ShortInterest.objects.all().values()
    clinecenter = ClineCenter.objects.all().values()

    def write_data(self):
        a = pd.DataFrame(SMOperations.clinecenter)
        return a

    def get_data(self, request, *args, **kwargs):
        return SMOperations.write_data(self)

class IBHIReportView(View):

    def get(self, request):

        return render(request,
                      'ibhi/report.html',
                      {}
                      )

class IBHIInsightsView(View):

    def get(self, request):

        return render(request,
                      {}
                      )

class IBHIBeliefsView(View):

    def get(self, request):


        return render(request,
                      'ibhi/beliefs.html',
                      {}
                      )

class IBHIPitchView(View):

    def get(self, request):


        return render(request,
                      'ibhi/pitch.html',
                      {}
                      )
