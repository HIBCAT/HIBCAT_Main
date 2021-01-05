from django.shortcuts import render
from django.http.response import HttpResponse
from django.template import loader
from django.views import View
import pandas as pd
from rest_pandas import PandasSimpleView
from functools import reduce

from .models import (BwGeography, Gender, BwContentSources,
                     BwNetSentiment, BwEmotions, BwSentiments,
                     BwVolume, BwActivityDay, BwActivityTime,
                     ClineCenter, YahooStockData, ShortInterest,)

day_wise_vol_main = pd.DataFrame(BwActivityDay.objects.all().values())
day_wise_vol_main.drop(columns=['id'], inplace=True)

time_wise_vol_main = pd.DataFrame(BwActivityTime.objects.all().values())
time_wise_vol_main.drop(columns=['id'], inplace=True)

geo_vol_main = pd.DataFrame(BwGeography.objects.all().values())
geo_vol_main.drop(columns=['id'], inplace=True)

volume_main = pd.DataFrame(BwVolume.objects.all().values())
volume_main.drop(columns=['id'], inplace=True)

sentiments_main = pd.DataFrame(BwSentiments.objects.all().values())
sentiments_main.drop(columns=['id'], inplace=True)

net_sentiments_main = pd.DataFrame(BwNetSentiment.objects.all().values())
net_sentiments_main.drop(columns=['id'], inplace=True)

emotions_main = pd.DataFrame(BwEmotions.objects.all().values())
emotions_main.drop(columns=['id'], inplace=True)

content_sources_main = pd.DataFrame(BwContentSources.objects.all().values())
content_sources_main.drop(columns=['id'], inplace=True)

gender_main = pd.DataFrame(Gender.objects.all().values())
gender_main.drop(columns=['id'], inplace=True)

# Create your views here.
# Visual 1
class BwVegaVisual1(PandasSimpleView):

    def write_data(self):
        df = day_wise_vol_main
        return df

    def get_data(self, request, *args, **kwargs):
        return BwVegaVisual1.write_data(self)


# Visual 2
class BwVegaVisual2(PandasSimpleView):

    def write_data(self):
        df = time_wise_vol_main
        return df

    def get_data(self, request, *args, **kwargs):
        return BwVegaVisual2.write_data(self)

# Visual 3
class BwVegaVisual3(PandasSimpleView):

    def write_data(self):
        df = geo_vol_main
        print(df.columns)
        return df

    def get_data(self, request, *args, **kwargs):
        return BwVegaVisual3.write_data(self)

# Visual 4
class BwVegaVisual4(PandasSimpleView):

    def write_data(self):
        volume = volume_main
        sentiments = sentiments_main
        net_sentiments = net_sentiments_main
        emotions = emotions_main
        content_sources = content_sources_main
        gender = gender_main

        data_frames = [volume, sentiments, net_sentiments, emotions, gender,content_sources]

        df_merged = reduce(lambda left, right: pd.merge(left, right, on=['days'],
                                                        how='outer'), data_frames).fillna('void')

        columns = ['volume', 'positive', 'neutral', 'negative', 'net_sent_vol',
                   'anger', 'fear', 'disgust', 'joy', 'surprise', 'sadness', "male",
                   "female", "blogs", "twitter", "reddit"]

        df_melted = pd.melt(df_merged, id_vars=['days'], value_vars=columns)

        return df_melted

    def get_data(self, request, *args, **kwargs):
        return BwVegaVisual4.write_data(self)







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
