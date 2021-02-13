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

# Feature 1
feature_1_bw = pd.DataFrame(BwSentiments.objects.all().values('days', 'positive', 'neutral',
                                                              'negative', 'net_sentiment','volume'))


# 1. BwActivityDay object
day_wise_vol_main = pd.DataFrame(ClineCenter.objects.all().values('publication_date_only', 'bing_liu_net_sentiment'))
#day_wise_vol_main.drop(columns=['id'], inplace=True)

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

    def brand_watch_df(self):
        brandwatch_01 = feature_1_bw.copy(deep=True)
        brandwatch_01['days'] = pd.to_datetime(brandwatch_01['days'])
        brandwatch_01.sort_values(by='days', ascending=False, inplace=True)

        # 1. Normalizing the net_sentiment on a scale of 0 to 100.
        # Normalization: (b-a) * [(x-y)/(z-y)] + a
        # (a,b): Range of normalized score
        # (0, 100)
        # x : Value to be normalized
        # y : Min value from the range
        # z : Max value from the range

        a = 0
        b = 100
        y = brandwatch_01['net_sentiment'].min()
        z = brandwatch_01['net_sentiment'].max()
        brandwatch_01['bw_net_senti_0_100'] = (b - a) * ((brandwatch_01['net_sentiment'] - y) / (z - y)) + a

        # 2. Standardized volume
        # x : value to be standardized
        # bw_vol_mean = mean of the range
        # bw_vol_std = standard deviation of the range

        bw_vol_mean = brandwatch_01['volume'].mean()
        bw_vol_std = brandwatch_01['volume'].std()
        brandwatch_01['bw_std_vol'] = (brandwatch_01['volume'] - bw_vol_mean) / bw_vol_std

        # 3. Normalizing the standardized volume on a scale of 0 to 20
        # Normalization: (b-a) * [(x-y)/(z-y)] + a
        # (a,b): Range of normalized score
        # (0, 20)
        # x : Value to be normalized
        # bw_std_vol_y : Min value from the range
        # bw_std_vol_z : Max value from the range

        bw_a = 0
        bw_b = 20
        bw_std_vol_y = brandwatch_01['bw_std_vol'].min()
        bw_std_vol_z = brandwatch_01['bw_std_vol'].max()
        brandwatch_01['bw_std_vol_0_20'] = (bw_b - bw_a) * (
                (brandwatch_01['bw_std_vol'] - bw_std_vol_y) / (bw_std_vol_z - bw_std_vol_y)) + bw_a

        # Dropping net_sentiment as it is not normalized on the scale of 0 to 100
        # Dropping bw_std_vol as I have replaced it with a normalized range on a scale of 0 to 20
        brandwatch_01.drop(columns=['net_sentiment', 'bw_std_vol'], inplace=True)

        # 4. Steps to calculate VWAP (Taking cumulative of 10 days)

        # https://school.stockcharts.com/doku.php?id=technical_indicators:vwap_intraday
        # 1. sen_vol = Multiply the net sentiment by the period's volume.
        # 2. Create a running total of these values. This is also known as a cumulative total.
        # 3. Create a running total of volume (cumulative volume).
        # 4. Divide the running total of price-volume by the running total of volume.

        brandwatch_01['sen_vol'] = brandwatch_01['bw_net_senti_0_100'] * brandwatch_01['bw_std_vol_0_20']

        # Calculating Cumulative Total (cumulative_sen_vol)
        # Calculating Cumulative Volume (cumulative_vol)
        # Subtracting by six as I am taking a mean total of n = 7 days.
        # And flag = n-1 (This leaves last 7 rows uncalculated to avoid index error)

        flag = len(brandwatch_01) - 6
        cumulative_sen_vol = [None] * len(brandwatch_01)
        cumulative_vol = [None] * len(brandwatch_01)

        for i in range(len(brandwatch_01)):
            if i != flag:
                a = sum(brandwatch_01['sen_vol'][i:i + 7])
                b = sum(brandwatch_01['bw_std_vol_0_20'][i:i + 7])
                cumulative_sen_vol[i] = a
                cumulative_vol[i] = b
            else:
                break

        brandwatch_01['cumulative_sen_vol'] = cumulative_sen_vol
        brandwatch_01['cumulative_vol'] = cumulative_vol

        # Now dividing the cumulative_sen_vol/cumulative_vol to get the Volumetric Weighted Average Sentiment (7 day)
        # Inspiration:
        # https://school.stockcharts.com/doku.php?id=technical_indicators:vwap_intraday
        brandwatch_01['bw_vwas'] = brandwatch_01['cumulative_sen_vol'] / brandwatch_01['cumulative_vol']

        # Now dropping the unnecessary columns
        brandwatch_01.drop(columns=['sen_vol', 'cumulative_sen_vol',
                                    'cumulative_vol'], inplace=True)
        return brandwatch_01


    def write_data(self):
        # Now below is the full code for the part one of the Feature one:
        # Part 1: BW Dataset
        brandwatch = BwVegaVisual1.brand_watch_df(self)

        # Part 2: Cline Center Dataset

        # Part 3: Event Timeline Dataset
        return a

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


