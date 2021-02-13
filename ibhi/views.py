from django.shortcuts import render
from django.http.response import HttpResponse
from django.template import loader
from django.views import View
import pandas as pd
from rest_pandas import PandasSimpleView
from functools import reduce

from .models import (BwActivityTime, BwActivityDay, BwGeography,
                     BwVolume, BwSentiments, BwNetSentiment,
                     BwEmotions, Gender, BwContentSources,
                     ClineCenter, YahooStockData, ShortInterest,
                     CCEventTimeline)

# 1. BwActivityDay object
day_wise_vol_main = pd.DataFrame(BwActivityDay.objects.all().values())
day_wise_vol_main.drop(columns=['id'], inplace=True)

# 2. BwActivityTime object
time_wise_vol_main = pd.DataFrame(BwActivityTime.objects.all().values())
time_wise_vol_main.drop(columns=['id'], inplace=True)

# 3. BwGeography object
geo_vol_main = pd.DataFrame(BwGeography.objects.all().values())
geo_vol_main.drop(columns=['id'], inplace=True)

# 4. BwVolume object
volume_main = pd.DataFrame(BwVolume.objects.all().values())
volume_main.drop(columns=['id'], inplace=True)

# 5. BwSentiments object
#sentiments_main = pd.DataFrame(BwSentiments.objects.all().values())
#sentiments_main.drop(columns=['id'], inplace=True)

# 6. BwNetSentiment object
net_sentiments_main = pd.DataFrame(BwNetSentiment.objects.all().values())
net_sentiments_main.drop(columns=['id'], inplace=True)

# 7. BwEmotions object
emotions_main = pd.DataFrame(BwEmotions.objects.all().values())
emotions_main.drop(columns=['id'], inplace=True)

# 8. Gender object
gender_main = pd.DataFrame(Gender.objects.all().values())
gender_main.drop(columns=['id'], inplace=True)

# 9. BwContentSources object
content_sources_main = pd.DataFrame(BwContentSources.objects.all().values())
content_sources_main.drop(columns=['id'], inplace=True)


# Visual 1
class BwVegaVisual1(PandasSimpleView):

    def write_data(self):
        df = day_wise_vol_main.copy(deep=True)
        return df

    def get_data(self, request, *args, **kwargs):
        return BwVegaVisual1.write_data(self)

# Visual 2
class BwVegaVisual2(PandasSimpleView):

    def write_data(self):
        df = time_wise_vol_main.copy(deep=True)
        return df

    def get_data(self, request, *args, **kwargs):
        return BwVegaVisual2.write_data(self)

# Visual 3
class BwVegaVisual3(PandasSimpleView):

    def write_data(self):
        df = geo_vol_main.copy(deep=True)
        return df

    def get_data(self, request, *args, **kwargs):
        return BwVegaVisual3.write_data(self)

# Visual 4
class BwVegaVisual4(PandasSimpleView):

    def write_data(self):
        volume = volume_main.copy(deep=True)
        sentiments = sentiments_main.copy(deep=True)
        net_sentiments = net_sentiments_main.copy(deep=True)
        emotions = emotions_main.copy(deep=True)
        content_sources = content_sources_main.copy(deep=True)
        gender = gender_main.copy(deep=True)

        data_frame = [volume, sentiments, net_sentiments,
                      emotions, content_sources, gender]

        df_merged = reduce(lambda left, right: pd.merge(left, right, on=['days'],
                                                        how='outer'), data_frame).fillna('void')

        columns = ['volume', 'positive', 'neutral', 'negative', 'net_sent_vol',
                   'anger', 'fear', 'disgust', 'joy', 'surprise', 'sadness', "male",
                   "female", "blogs", "twitter", "reddit"]

        df_melted = pd.melt(df_merged, id_vars=['days'],
                            value_vars=columns)

        return df_melted

    def get_data(self, request, *args, **kwargs):
        return BwVegaVisual4.write_data(self)



class IBHITestView(View):

    def get(self, request):

        return render(request,
                      'ibhi/test.html',
                      {}
                      )

class OverviewLayoutView(View):

    def get(self, request):

        return render(request,
                      'ibhi/01_report.html',
                      {}
                      )

class FluidLayoutView(View):

    def get(self, request):


        return render(request,
                      'ibhi/02_report.html',
                      {}
                      )

class IconLayoutView(View):

    def get(self, request):


        return render(request,
                      'ibhi/03_report.html',
                      {}
                      )


