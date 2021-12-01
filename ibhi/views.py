from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from .utils import PageLinksMixin
from .forms import ArcherExplorerForm


from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.template import loader
from django.views import View
import pandas as pd
import datetime
from rest_pandas import PandasSimpleView
import csv
from functools import reduce
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

from .models import (BwActivityTime, BwActivityDay, BwGeography,
                     BwVolume, BwSentiments, BwNetSentiment,
                     BwEmotions, Gender, BwContentSources,
                     ClineCenter, YahooStockData, ShortInterest,
                     CCEventTimeline,
                     ResearchPapers, APIDataDictionary,
                     RawDataDictionary, InternalLinks, Ideas
                     )


# Feature 3
class BwNewsExplorerVis(PandasSimpleView):

    def date_df(self, brand_name):

        # Part 1:
        f3_clinecenter_01 = pd.DataFrame(ClineCenter.objects.all().values('publication_date_only', 'bing_liu_net_sentiment', 'brand'))
        f3_clinecenter_01 = f3_clinecenter_01[f3_clinecenter_01['brand'] == brand_name]
        f3_clinecenter_01.drop(columns=['brand'], inplace=True)
        f3_clinecenter_01['publication_date_only'] = pd.to_datetime(f3_clinecenter_01['publication_date_only'])
        f3_clinecenter_01.sort_values(by='publication_date_only', ascending=False, inplace=True)
        f3_clinecenter_01.reset_index(inplace=True, drop=True)

        # Now creating the main dataframe : clinecenter_02
        f3_clinecenter_02 = pd.DataFrame({"publication_date_only":
                                              list(set(f3_clinecenter_01['publication_date_only']))
                                          })
        f3_clinecenter_02['publication_date_only'] = pd.to_datetime(f3_clinecenter_02['publication_date_only'])
        f3_clinecenter_02.sort_values(by='publication_date_only', ascending=False, inplace=True)
        f3_clinecenter_02['cc_positive'] = 0
        f3_clinecenter_02['cc_negative'] = 0
        f3_clinecenter_02['cc_neutral'] = 0
        f3_clinecenter_02.reset_index(inplace=True, drop=True)

        # Now calculating the volume of the posts:
        # I will be ignoring the None type values in bing_liu_net_sentiment

        unique_index = pd.Index(f3_clinecenter_02['publication_date_only'])

        for i in range(len(f3_clinecenter_01)):

            # Finding the matching index of dates in the main dataframes indexes
            index_match = unique_index.get_loc(f3_clinecenter_01['publication_date_only'][i])

            if f3_clinecenter_01['bing_liu_net_sentiment'][i] == 1:
                f3_clinecenter_02['cc_positive'][index_match] += 1
            elif f3_clinecenter_01['bing_liu_net_sentiment'][i] == 0:
                f3_clinecenter_02['cc_neutral'][index_match] += 1
            elif f3_clinecenter_01['bing_liu_net_sentiment'][i] < 0:
                f3_clinecenter_02['cc_negative'][index_match] += 1
            else:
                pass

        f3_clinecenter_02['cc_volume'] = f3_clinecenter_02['cc_negative'] + f3_clinecenter_02['cc_neutral'] + \
                                         f3_clinecenter_02['cc_positive']


        f3_clinecenter_02.reset_index(inplace=True, drop=True)


        return f3_clinecenter_02

    def merged_data(self):
        final_df = pd.DataFrame()
        brands = pd.DataFrame(ClineCenter.objects.all().values('brand'))

        for brand_name in brands['brand'].unique():
            df1 = BwNewsExplorerVis.date_df(self, brand_name)
            final_df = pd.concat([final_df, df1])
            final_df.reset_index(inplace=True, drop=True)

        final_df_02 = pd.DataFrame(ClineCenter.objects.all().values('publication_date_only', 'brand', 'bing_liu_net_sentiment', 'bing_liu_pos', 'bing_liu_neg','title'))
        final_df_02['publication_date_only'] = pd.to_datetime(final_df_02['publication_date_only'])
        final_df_02.sort_values(by='publication_date_only', ascending=False, inplace=True)
        final_df_02.reset_index(inplace=True, drop=True)

        final_df_03 = pd.merge(left=final_df, right=final_df_02, left_on='publication_date_only', right_on='publication_date_only')

        final_df_03.reset_index(inplace=True, drop=True)

        return final_df_03

    def write_data(self):
        return BwNewsExplorerVis.merged_data(self)


    def get_data(self, request, *args, **kwargs):
        return BwNewsExplorerVis.write_data(self)

# Feature 1
class BwNetSentimentExplorerVis(PandasSimpleView):

    def brand_watch_df(self, brand_name):
        brandwatch_01 = pd.DataFrame(BwSentiments.objects.all().values('days', 'positive', 'neutral',
                                                              'negative', 'net_sentiment','volume', 'brand'))
        brandwatch_01 = brandwatch_01[brandwatch_01['brand']==brand_name]
        brandwatch_01.drop(columns=['brand'], inplace=True)
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
        brandwatch_01.rename(columns={'days': 'date', 'positive': 'bw_positive',
                                      'neutral': 'bw_neutral',
                                      'negative': 'bw_negative',
                                      'volume': 'bw_volume'}, inplace=True)
        # Melting the columns
        brandwatch_01 = pd.melt(brandwatch_01, id_vars=["date"],
                                value_vars=["bw_positive", "bw_neutral", "bw_negative",
                                            "bw_volume", "bw_net_senti_0_100",
                                            "bw_std_vol_0_20", "bw_vwas"],
                                var_name="attributes", value_name="values")

        # Changing the datatype of attributes from 'str' to 'category'
        # The dataset brandwatch_01 will consume only 1/5 times of the memory than the original
        brandwatch_01["attributes"] = brandwatch_01["attributes"].astype("category")

        # 5 Adding extra columns so that timeline dataset can be concatenated easily

        brandwatch_01['end_date'] = [None] * len(brandwatch_01)
        brandwatch_01['event_type'] = [None] * len(brandwatch_01)
        brandwatch_01['description'] = [None] * len(brandwatch_01)
        brandwatch_01['brand'] = brand_name

        return brandwatch_01

    def cline_center_df(self, brand_name):
        # Feature one:
        # Part 2: Cline Center

        # As the test is successful, I will perform the analysis on the real data.
        # 1. Perform analysis on real data
        # 2. Add the columns with volume and standardized score
        # 3. Melt the columns

        # 1:
        clinecenter_01 = pd.DataFrame(ClineCenter.objects.all().values('publication_date_only', 'bing_liu_net_sentiment', 'brand'))
        clinecenter_01 = clinecenter_01[clinecenter_01['brand']==brand_name]
        clinecenter_01.drop(columns=['brand'], inplace=True)
        clinecenter_01['publication_date_only'] = pd.to_datetime(clinecenter_01['publication_date_only'])
        clinecenter_01.sort_values(by='publication_date_only', ascending=False, inplace=True)
        clinecenter_01.reset_index(inplace=True, drop=True)

        # Now creating the main dataframe : clinecenter_02
        clinecenter_02 = pd.DataFrame({"date":
                                           list(set(clinecenter_01['publication_date_only']))
                                       })
        clinecenter_02['date'] = pd.to_datetime(clinecenter_02['date'])
        clinecenter_02.sort_values(by='date', ascending=False, inplace=True)
        clinecenter_02['cc_positive'] = 0
        clinecenter_02['cc_negative'] = 0
        clinecenter_02['cc_neutral'] = 0
        clinecenter_02.reset_index(inplace=True, drop=True)

        # Now calculating the volume of the posts:
        # I will be ignoring the None type values in bing_liu_net_sentiment

        unique_index = pd.Index(clinecenter_02['date'])

        for i in range(len(clinecenter_01)):

            # Finding the matching index of dates in the main dataframes indexes
            index_match = unique_index.get_loc(clinecenter_01['publication_date_only'][i])

            if clinecenter_01['bing_liu_net_sentiment'][i] == 1:
                clinecenter_02['cc_positive'][index_match] += 1
            elif clinecenter_01['bing_liu_net_sentiment'][i] == 0:
                clinecenter_02['cc_neutral'][index_match] += 1
            elif clinecenter_01['bing_liu_net_sentiment'][i] < 0:
                clinecenter_02['cc_negative'][index_match] += 1
            else:
                pass

        clinecenter_02['cc_volume'] = clinecenter_02['cc_negative'] + clinecenter_02['cc_neutral'] + clinecenter_02[
            'cc_positive']

        # 2.1 Calculate the standardized net sentiment
        # 2.2 Calculate the normalized net sentiment (0 to 100)
        # 2.3 Standardize the volume
        # 2.4 Normalize the volume on the scale of (0 to 20)
        # 2.5 Drop the non-normalized columns of volume and net sentiment
        # 2.6 Calculate VWAP

        clinecenter_02['cc_net_sent'] = [None] * len(clinecenter_02)

        # 2.1 Calculate the standardized net sentiment
        for i in range(len(clinecenter_02)):
            diff = clinecenter_02['cc_positive'][i] - clinecenter_02['cc_negative'][i]
            sum_1 = clinecenter_02['cc_positive'][i] + clinecenter_02['cc_negative'][i]
            if diff != 0:
                clinecenter_02['cc_net_sent'][i] = diff / sum_1
            else:
                clinecenter_02['cc_net_sent'][i] = 0

        # 2.2 Calculate the normalized net sentiment (0 to 100)
        # Normalization: (b-a) * [(x-y)/(z-y)] + a
        # (a,b): Range of normalized score
        # (0, 100)
        # x : Value to be normalized
        # y : Min value from the range
        # z : Max value from the range

        a = 0
        b = 100
        y = clinecenter_02['cc_net_sent'].min()
        z = clinecenter_02['cc_net_sent'].max()
        clinecenter_02['cc_net_senti_0_100'] = (b - a) * ((clinecenter_02['cc_net_sent'] - y) / (z - y)) + a

        # 2.3 Standardize the volume
        # x : value to be standardized
        # bw_vol_mean = mean of the range
        # bw_vol_std = standard deviation of the range

        cc_vol_mean = clinecenter_02['cc_volume'].mean()
        cc_vol_std = clinecenter_02['cc_volume'].std()
        clinecenter_02['cc_std_vol'] = (clinecenter_02['cc_volume'] - cc_vol_mean) / cc_vol_std

        # 2.4 Normalizing the standardized volume on a scale of 0 to 20
        # Normalization: (b-a) * [(x-y)/(z-y)] + a
        # (a,b): Range of normalized score
        # (0, 20)
        # x : Value to be normalized
        # bw_std_vol_y : Min value from the range
        # bw_std_vol_z : Max value from the range

        cc_a = 0
        cc_b = 20
        cc_std_vol_y = clinecenter_02['cc_std_vol'].min()
        cc_std_vol_z = clinecenter_02['cc_std_vol'].max()
        clinecenter_02['cc_std_vol_0_20'] = (cc_b - cc_a) * (
                (clinecenter_02['cc_std_vol'] - cc_std_vol_y) / (cc_std_vol_z - cc_std_vol_y)) + cc_a

        # 2.5 Drop the non-normalized columns of volume and net sentiment

        # Dropping cc_net_sent as it is not normalized on the scale of 0 to 100
        # Dropping cc_std_vol as I have replaced it with a normalized range on a scale of 0 to 20
        clinecenter_02.drop(columns=['cc_net_sent', 'cc_std_vol'], inplace=True)

        # 2.6: Calculating VWAS (Volumetric Weighted Average Sentiment) Score:
        # 4. Steps to calculate VWAP (Taking cumulative of 10 days)

        # https://school.stockcharts.com/doku.php?id=technical_indicators:vwap_intraday
        # 1. sen_vol = Multiply the net sentiment by the period's volume.
        # 2. Create a running total of these values. This is also known as a cumulative total.
        # 3. Create a running total of volume (cumulative volume).
        # 4. Divide the running total of price-volume by the running total of volume.

        clinecenter_02['sen_vol'] = clinecenter_02['cc_net_senti_0_100'] * clinecenter_02['cc_std_vol_0_20']

        # Calculating Cumulative Total (cumulative_sen_vol)
        # Calculating Cumulative Volume (cumulative_vol)
        # Subtracting by six as I am taking a mean total of n = 7 days.
        # And flag = n-1 (This leaves last 7 rows uncalculated to avoid index error)

        flag = len(clinecenter_02) - 6
        cumulative_sen_vol = [None] * len(clinecenter_02)
        cumulative_vol = [None] * len(clinecenter_02)

        for i in range(len(clinecenter_02)):
            if i != flag:
                a = sum(clinecenter_02['sen_vol'][i:i + 7])
                b = sum(clinecenter_02['cc_std_vol_0_20'][i:i + 7])
                cumulative_sen_vol[i] = a
                cumulative_vol[i] = b
            else:
                break

        clinecenter_02['cumulative_sen_vol'] = cumulative_sen_vol
        clinecenter_02['cumulative_vol'] = cumulative_vol

        # Now dividing the cumulative_sen_vol/cumulative_vol to get the Volumetric Weighted Average Sentiment (7 day)
        # Inspiration:
        # https://school.stockcharts.com/doku.php?id=technical_indicators:vwap_intraday
        clinecenter_02['cc_vwas'] = clinecenter_02['cumulative_sen_vol'] / clinecenter_02['cumulative_vol']

        # 2.7 Now dropping the unnecessary columns
        clinecenter_02.drop(columns=['sen_vol', 'cumulative_sen_vol',
                                     'cumulative_vol'], inplace=True)

        # 2.8 Melting the columns

        clinecenter_02 = pd.melt(clinecenter_02, id_vars=["date"],
                                 value_vars=["cc_positive", "cc_negative", "cc_neutral",
                                             "cc_volume", "cc_net_senti_0_100",
                                             "cc_std_vol_0_20", "cc_vwas"],
                                 var_name="attributes", value_name="values")

        # 3 Add the news article data over here.
        # 3.1 Creating another field for news article title.
        clinecenter_03 = pd.DataFrame(ClineCenter.objects.all().values('publication_date_only', 'title', 'brand'))
        clinecenter_03['publication_date_only'] = pd.to_datetime(clinecenter_03['publication_date_only'])
        clinecenter_03.sort_values(by='publication_date_only', ascending=False, inplace=True)
        clinecenter_03.reset_index(inplace=True, drop=True)
        clinecenter_03.rename(columns={'publication_date_only': 'date', 'title': 'Title'}, inplace=True)

        # 3.2 Now melting the columns
        clinecenter_03 = pd.melt(clinecenter_03, id_vars=["date"],
                                 value_vars=["Title"],
                                 var_name="attributes", value_name="values")

        # 3.3 Now appending the column melted in the step # 2.8 and # 3.2
        clinecenter_04 = clinecenter_02.append(clinecenter_03, ignore_index=True)

        # 3.4 Adding extra columns so that timeline dataset can be concatenated easily
        clinecenter_04['end_date'] = [None] * len(clinecenter_04)
        clinecenter_04['event_type'] = [None] * len(clinecenter_04)
        clinecenter_04['description'] = [None] * len(clinecenter_04)
        clinecenter_04['brand'] = brand_name

        return clinecenter_04

    # def timeline_df(self, brand_name):
    #     # Part 3: Timeline Data
    #     # Melting will be problematic. So I have to restructure the data.
    #     # 1. Rename the start_date = date
    #     # 2. Add empty columns 'attributes' and 'values'
    #     timeline_01 = pd.DataFrame(CCEventTimeline.objects.all().values('date', 'end_date', 'event_type', 'description', 'brand'))
    #     timeline_01 = timeline_01[timeline_01['brand']==brand_name]
    #     timeline_01['date'] = pd.to_datetime(timeline_01['date'])
    #     timeline_01['end_date'] = pd.to_datetime(timeline_01['end_date'])
    #     timeline_01['end_date'] =  timeline_01['end_date'].dt.date
    #     timeline_01['attributes'] = [None] * len(timeline_01)
    #     timeline_01['values'] = [None] * len(timeline_01)
    #     return timeline_01


    def merged_data(self):
        final_df = pd.DataFrame()
        brands = pd.DataFrame(ClineCenter.objects.all().values('brand'))

        for brand_name in brands['brand'].unique():
            df1 = BwNetSentimentExplorerVis.brand_watch_df(self, brand_name)
            df2 = BwNetSentimentExplorerVis.cline_center_df(self, brand_name)
            # df3 = BwNetSentimentExplorerVis.timeline_df(self, brand_name)
            # df3 needs to be added in the next line
            final_df = pd.concat([final_df, df1, df2])
            final_df.reset_index(inplace=True, drop=True)

        return final_df



    def write_data(self):
        # Now below is the full code for the part one of the Feature one:
        return BwNetSentimentExplorerVis.merged_data(self)

    def get_data(self, request, *args, **kwargs):
        return BwNetSentimentExplorerVis.write_data(self)

# Feature 2
class BwSentimentTrendVis(PandasSimpleView):

    def bw_cc_df(self, brand_name):

        # Preparing the clinecenter data first.

        # Part 1:
        f2_clinecenter_01 = pd.DataFrame(ClineCenter.objects.all().values('publication_date_only', 'bing_liu_net_sentiment', 'brand'))
        f2_clinecenter_01 = f2_clinecenter_01[f2_clinecenter_01['brand']==brand_name]
        f2_clinecenter_01.drop(columns=['brand'], inplace=True)
        f2_clinecenter_01['publication_date_only'] = pd.to_datetime(f2_clinecenter_01['publication_date_only'])
        f2_clinecenter_01.sort_values(by='publication_date_only', ascending=False, inplace=True)
        f2_clinecenter_01.reset_index(inplace=True, drop=True)

        # Now creating the main dataframe : clinecenter_02
        f2_clinecenter_02 = pd.DataFrame({"date":
                                              list(set(f2_clinecenter_01['publication_date_only']))
                                          })
        f2_clinecenter_02['date'] = pd.to_datetime(f2_clinecenter_02['date'])
        f2_clinecenter_02.sort_values(by='date', ascending=False, inplace=True)
        f2_clinecenter_02['cc_positive'] = 0
        f2_clinecenter_02['cc_negative'] = 0
        f2_clinecenter_02['cc_neutral'] = 0
        f2_clinecenter_02.reset_index(inplace=True, drop=True)

        # Now calculating the volume of the posts:
        # I will be ignoring the None type values in bing_liu_net_sentiment

        unique_index = pd.Index(f2_clinecenter_02['date'])

        for i in range(len(f2_clinecenter_01)):

            # Finding the matching index of dates in the main dataframes indexes
            index_match = unique_index.get_loc(f2_clinecenter_01['publication_date_only'][i])

            if f2_clinecenter_01['bing_liu_net_sentiment'][i] == 1:
                f2_clinecenter_02['cc_positive'][index_match] += 1
            elif f2_clinecenter_01['bing_liu_net_sentiment'][i] == 0:
                f2_clinecenter_02['cc_neutral'][index_match] += 1
            elif f2_clinecenter_01['bing_liu_net_sentiment'][i] < 0:
                f2_clinecenter_02['cc_negative'][index_match] += 1
            else:
                pass

        f2_clinecenter_02['cc_volume'] = f2_clinecenter_02['cc_negative'] + f2_clinecenter_02['cc_neutral'] + \
                                         f2_clinecenter_02['cc_positive']

        # Part 2: Preparing BrandWatch Dataset

        f2_brandwatch_01 = pd.DataFrame(BwSentiments.objects.all().values('days', 'positive', 'neutral',
                                                              'negative', 'net_sentiment','volume', 'brand'))
        f2_brandwatch_01 = f2_brandwatch_01[f2_brandwatch_01['brand']==brand_name]
        f2_brandwatch_01.drop(columns=['net_sentiment', 'brand'], inplace=True)
        f2_brandwatch_01['days'] = pd.to_datetime(f2_brandwatch_01['days'])
        f2_brandwatch_01.sort_values(by='days', ascending=False, inplace=True)
        f2_brandwatch_01.reset_index(inplace=True, drop=True)
        f2_brandwatch_01.rename(columns={'days': 'date',
                                         'positive': 'bw_positive',
                                         'neutral': 'bw_neutral',
                                         'negative': 'bw_negative',
                                         'volume': 'bw_volume'}, inplace=True)

        # Part 3: Appending the datasets in part 1 and part 2:
        f2_cc_bw = pd.merge(f2_brandwatch_01, f2_clinecenter_02, on="date", how="inner")

        # Now filling the 3 month's moving average of all the columns

        flag = len(f2_cc_bw) - 89

        bw_3ma_positive = [None] * len(f2_cc_bw)
        bw_3ma_negative = [None] * len(f2_cc_bw)
        bw_3ma_neutral = [None] * len(f2_cc_bw)
        bw_3ma_volume = [None] * len(f2_cc_bw)

        cc_3ma_positive = [None] * len(f2_cc_bw)
        cc_3ma_negative = [None] * len(f2_cc_bw)
        cc_3ma_neutral = [None] * len(f2_cc_bw)
        cc_3ma_volume = [None] * len(f2_cc_bw)

        for i in range(len(f2_cc_bw)):
            if i != flag:

                bw_3ma_positive[i] = (sum(f2_cc_bw['bw_positive'][i:i + 90]) / 90)
                bw_3ma_negative[i] = (sum(f2_cc_bw['bw_negative'][i:i + 90]) / 90)
                bw_3ma_neutral[i] = (sum(f2_cc_bw['bw_neutral'][i:i + 90]) / 90)
                bw_3ma_volume[i] = (sum(f2_cc_bw['bw_volume'][i:i + 90]) / 90)

                cc_3ma_positive[i] = (sum(f2_cc_bw['cc_positive'][i:i + 90]) / 90)
                cc_3ma_negative[i] = (sum(f2_cc_bw['cc_negative'][i:i + 90]) / 90)
                cc_3ma_neutral[i] = (sum(f2_cc_bw['cc_neutral'][i:i + 90]) / 90)
                cc_3ma_volume[i] = (sum(f2_cc_bw['cc_volume'][i:i + 90]) / 90)

            else:
                break

        f2_cc_bw['bw_3ma_positive'] = bw_3ma_positive
        f2_cc_bw['bw_3ma_negative'] = bw_3ma_negative
        f2_cc_bw['bw_3ma_neutral'] = bw_3ma_neutral
        f2_cc_bw['bw_3ma_volume'] = bw_3ma_volume

        f2_cc_bw['cc_3ma_positive'] = cc_3ma_positive
        f2_cc_bw['cc_3ma_negative'] = cc_3ma_negative
        f2_cc_bw['cc_3ma_neutral'] = cc_3ma_neutral
        f2_cc_bw['cc_3ma_volume'] = cc_3ma_volume

        # Now normalizing all the columns on a scale of 0 to 100.
        # Then standardizing all the normalized values.

        f2_cc_bw['bw_std_positive'] = [None] * len(f2_cc_bw)
        f2_cc_bw['bw_std_negative'] = [None] * len(f2_cc_bw)
        f2_cc_bw['bw_std_neutral'] = [None] * len(f2_cc_bw)
        f2_cc_bw['bw_std_volume'] = [None] * len(f2_cc_bw)

        f2_cc_bw['cc_std_positive'] = [None] * len(f2_cc_bw)
        f2_cc_bw['cc_std_negative'] = [None] * len(f2_cc_bw)
        f2_cc_bw['cc_std_neutral'] = [None] * len(f2_cc_bw)
        f2_cc_bw['cc_std_volume'] = [None] * len(f2_cc_bw)

        columns = ['bw_positive', 'bw_neutral', 'bw_negative', 'bw_volume',
                   'cc_positive', 'cc_negative', 'cc_neutral', 'cc_volume',

                   'bw_3ma_positive', 'bw_3ma_neutral', 'bw_3ma_negative', 'bw_3ma_volume',
                   'cc_3ma_positive', 'cc_3ma_negative', 'cc_3ma_neutral', 'cc_3ma_volume',
                   ]

        # Creating columns on the go
        for i in columns:
            # 1. Standardized volume
            # x : value to be standardized
            # bw_vol_mean = mean of the range
            # bw_vol_std = standard deviation of the range

            f2_cc_bw_mean = f2_cc_bw[i].mean()
            f2_cc_bw_std = f2_cc_bw[i].std()
            f2_cc_bw[f'{i}_std_0_100'] = (f2_cc_bw[i] - f2_cc_bw_mean) / f2_cc_bw_std

            # 2. Normalizing the columns on a scale of 0 to 100.
            # Normalization: (b-a) * [(x-y)/(z-y)] + a
            # (a,b): Range of normalized score
            # (0, 100)
            # x : Value to be normalized
            # y : Min value from the range
            # z : Max value from the range

            a = 0
            b = 100
            y = f2_cc_bw[f'{i}_std_0_100'].min()
            z = f2_cc_bw[f'{i}_std_0_100'].max()
            f2_cc_bw[f'{i}_std_0_100'] = (b - a) * ((f2_cc_bw[f'{i}_std_0_100'] - y) / (z - y)) + a
            # For loop ends over here. Beware

        # Now melt all the columns to get the final dataset for the feature 2
        f2_cc_bw = pd.melt(f2_cc_bw, id_vars=["date"],
                              value_vars=['bw_positive', 'bw_neutral', 'bw_negative', 'bw_volume',
                                           'cc_positive', 'cc_negative', 'cc_neutral', 'cc_volume',
                                           'bw_3ma_positive', 'bw_3ma_negative', 'bw_3ma_neutral', 'bw_3ma_volume',
                                           'cc_3ma_positive', 'cc_3ma_negative', 'cc_3ma_neutral', 'cc_3ma_volume',
                                           'bw_std_positive', 'bw_std_negative', 'bw_std_neutral', 'bw_std_volume',
                                           'cc_std_positive', 'cc_std_negative', 'cc_std_neutral', 'cc_std_volume',
                                           'bw_positive_std_0_100', 'bw_neutral_std_0_100',
                                           'bw_negative_std_0_100', 'bw_volume_std_0_100', 'cc_positive_std_0_100',
                                           'cc_negative_std_0_100', 'cc_neutral_std_0_100', 'cc_volume_std_0_100',
                                           'bw_3ma_positive_std_0_100', 'bw_3ma_neutral_std_0_100',
                                           'bw_3ma_negative_std_0_100', 'bw_3ma_volume_std_0_100',
                                           'cc_3ma_positive_std_0_100', 'cc_3ma_negative_std_0_100',
                                           'cc_3ma_neutral_std_0_100', 'cc_3ma_volume_std_0_100'], var_name="attributes", value_name="values")

        f2_cc_bw.dropna(inplace=True)
        f2_cc_bw['brand'] = brand_name
        return f2_cc_bw

    def merged_data(self):
        final_df = pd.DataFrame()
        brands = pd.DataFrame(ClineCenter.objects.all().values('brand'))

        for brand_name in brands['brand'].unique():
            df1 = BwSentimentTrendVis.bw_cc_df(self, brand_name)
            final_df = pd.concat([final_df, df1])
            final_df.reset_index(inplace=True, drop=True)

        return final_df


    def write_data(self):
        return BwSentimentTrendVis.merged_data(self)

    def get_data(self, request, *args, **kwargs):
        return BwSentimentTrendVis.write_data(self)

# Feature 4
class BwVegaAdInvestmentVis(PandasSimpleView):

    def recovery_cost(self):

        # Part 1: Downloading the simple data
        f2_brandwatch_01 = pd.DataFrame(BwSentiments.objects.all().values('days', 'positive', 'neutral',
                                                              'negative', 'net_sentiment','volume', 'brand'))
        f2_brandwatch_01.drop(columns=['net_sentiment'], inplace=True)
        f2_brandwatch_01['days'] = pd.to_datetime(f2_brandwatch_01['days'])
        f2_brandwatch_01.sort_values(by='days', ascending=False, inplace=True)
        f2_brandwatch_01.reset_index(inplace=True, drop=True)
        f2_brandwatch_01.rename(columns={'days': 'date',
                                         'positive': 'bw_positive',
                                         'neutral': 'bw_neutral',
                                         'negative': 'bw_negative',
                                         'volume': 'bw_volume'}, inplace=True)

        # According to the research done on @anindianpoet instagram account:
        # 5784 people are reached for every USD 1 spend.
        # Out of those 5784 people, a median of 3.38 % react in terms of positive+negative reactions

        # According to negative bias theory, for every negative comment, a person has to hear five positive comments
        # to neutralize the negative effect.
        # This 'pos_reach required represents the number of reactions we will require. It is
        # 3.38 % of the total people reached.
        f2_brandwatch_01['pos_reach_req'] = f2_brandwatch_01['bw_negative'] * 5

        # Out of 100 people reached, how many people react positively or negatively
        median_reaction = 3.38
        f2_brandwatch_01['total_reach_req'] = (f2_brandwatch_01['pos_reach_req']*100)/median_reaction

        # Dividing the people reached per dollar to know the investment required per day
        people_per_usd = 5784
        f2_brandwatch_01['investment_estimate'] = f2_brandwatch_01['total_reach_req']/people_per_usd

        f2_brandwatch_01.drop(columns=['pos_reach_req', 'total_reach_req'], inplace=True)

        return f2_brandwatch_01


    def write_data(self):
        return BwVegaAdInvestmentVis.recovery_cost(self)

    def get_data(self, request, *args, **kwargs):
        return BwVegaAdInvestmentVis.write_data(self)


class FeatureWordCloud(PandasSimpleView):

    def AggregateDailyUniqueEntity(df):
        '''
        Process a dataframe to aggregate the extracted entities onto daily levels, making entities for each day unique
        '''
        # convert NaN to empty string
        df.fillna('', inplace=True)

        # aggregate entities on daily level (if one entity appears in more than one reports on a day, only count it once)
        # concatenate the string
        df_daily = df[['publication_date_only']]
        df_daily['extracted_organizations'] = df.groupby(['publication_date_only'])['extracted_organizations'].transform(lambda x: '|'.join(x))
        df_daily['extracted_people'] = df.groupby(['publication_date_only'])['extracted_people'].transform(lambda x: '|'.join(x))

        # drop duplicate data
        df_daily = df_daily.drop_duplicates()

        return (df_daily)

    def KeepUniqueEntity(string):
        with_repetition = string.split("|")
        unique_list = list(set(with_repetition))
        return ("|".join(unique_list))

    def WordCloudGenerator(aggregation="article", use_idf=False, NER_type="organization"):

        data = pd.DataFrame(ClineCenter.objects.all().values('publication_date_only', 'extracted_organizations', 'extracted_people'))

        ################################## aggregation (optional) ##########################################
        # aggregate the entities onto daily level if specified,
        # with **AggregateDailyUniqueEntity** and **KeepUniqueEntity** externally defined
        # this may take some time
        if aggregation == "daily" or use_idf:
            data = FeatureWordCloud.AggregateDailyUniqueEntity(data)
            if aggregation == "daily":  # only keep unique list of entities every day
                data['extracted_organizations'].apply(FeatureWordCloud.KeepUniqueEntity)
                data['extracted_people'].apply(FeatureWordCloud.KeepUniqueEntity)

        ################################### create word frequency dictionary #################################

        # create a dictionary for the entities and their count
        ## combine the non-null rows into a string for the selected entity type
        if NER_type == "organization":
            entity_string = "|".join(data.extracted_organizations.dropna())
            if use_idf:
                corpus = list(data.extracted_organizations.dropna())
        elif NER_type == "people":
            entity_string = "|".join(data.extracted_people.dropna())
            if use_idf:
                corpus = list(data.extracted_people.dropna())
        elif NER_type == "all":
            entity_string = "|".join(pd.concat([data.extracted_organizations.dropna(),
                                                data.extracted_people.dropna()]))
            if use_idf:
                corpus = list(data.extracted_organizations.dropna()) + list(data.extracted_people.dropna())

        else:
            print("Please check Named Entity type.")
            return

        ## split the string into a list
        entity_list = entity_string.split("|")
        ## frequency dictionary
        word_freq = dict()
        for i in entity_list:
            word_freq[i] = word_freq.get(i, 0) + 1

        ######################################## create visualization#################################
        wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white").generate_from_frequencies(word_freq)

        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.savefig("ibhi/media/wordcloud/wordcloud_test.svg", format="svg", dpi=1000)

# Remove the comment if you want to generate the word cloud
# FeatureWordCloud.WordCloudGenerator("daily", "organization")

class WordCloudView(View):

    def get(self, request):
        return render(request,
                      'ibhi/word_cloud.html',
                      {}
                      )

class AdInvestmentView(View):

    def get(self, request):
        return render(request,
                      'ibhi/ad_investment.html',
                      {}
                      )

class NewsExplorerView(View):

    def get(self, request):
        return render(request,
                      'ibhi/news_explorer.html',
                      {}
                      )

class NetSentimentExplorerView(View):

    def get(self, request):
        return render(request,
                      'ibhi/net_sentiment_explorer.html',
                      {}
                      )

class SentimentTrendView(View):

    def get(self, request):
        return render(request,
                      'ibhi/sentiment_trend.html',
                      {}
                      )

class ResearchPapersList(LoginRequiredMixin, PermissionRequiredMixin, PageLinksMixin, ListView):
    paginate_by = 2
    model = ResearchPapers
    permission_required = 'ibhi.view_researchpapers'

class APIDataDictionaryList(LoginRequiredMixin, PermissionRequiredMixin, PageLinksMixin, ListView):
    paginate_by = 2
    model = APIDataDictionary
    permission_required = 'ibhi.view_apidatadictionary'

class RawDataDictionaryList(LoginRequiredMixin, PermissionRequiredMixin, PageLinksMixin, ListView):
    paginate_by = 2
    model = RawDataDictionary
    permission_required = 'ibhi.view_rawdatadictionary'

class InternalLinksList(LoginRequiredMixin, PermissionRequiredMixin, PageLinksMixin, ListView):
    paginate_by = 2
    model = InternalLinks
    permission_required = 'ibhi.view_internallinks'

class IdeasList(LoginRequiredMixin, PermissionRequiredMixin, PageLinksMixin, ListView):
    paginate_by = 2
    model = Ideas
    permission_required = 'ibhi.view_ideas'

final_url = ''
raw_df = pd.DataFrame()
# archer_explorer_list = ''
# Archer API
def archer_explorer(request):
    global final_url
    global raw_df
    # global archer_explorer_list


    if request.method == 'POST':
        query1 = ArcherExplorerForm(request.POST)
        if query1.is_valid():
            query2 = query1.cleaned_data['api_key']
            query3 = query1.cleaned_data['query']
            query4 = query1.cleaned_data['rows']

            query3 = query3.replace(" ", "%20")
            query3 = query3.replace("\'", "%22")
            query3 = query3.replace("\"", "%22")

            query3 = query3.replace("(", "\(")
            query3 = query3.replace(")", "\)")

            query3 = query3.replace("or", "OR")
            query3 = query3.replace("and", "AND")


            url1 = f'https://archerapi.clinecenter.illinois.edu/select?fl=aid,publication_date,ingest_date,source_name,url,title,title_length,content,content_length,publisher,other_metadata,extracted_people,extracted_people_text,extracted_locations,extracted_locations_text,extracted_organizations,extracted_organizations_text,country,geolocation_original,geolocation_locations,geolocation_locations_text,geolocation,geolocation_featureids,geolocation_probabilities,anew_arousal,anew_dominance,anew_valence,bing_liu_neg,bing_liu_pos,dal_activation,dal_imagery,dal_pleasantness,inquirer_neg,inquirer_pos,lexicoder_pos,lexicoder_neg,mf_moralitygeneral,mf_authorityvice,mf_authorityvirtue,mf_fairnessvice,mf_fairnessvirtue,mf_harmvice,mf_harmvirtue,mf_ingroupvice,mf_ingroupvirtue,mf_purityvice,mf_purityvirtue,pronouns,status'
            content = '&q=content:'+query3
            rows = '&rows='+query4

            title_global = '&fq=title:global'

            api_key = '&key=' + query2

            final_url = url1 + content + rows + title_global + api_key + '&wt=csv'
            print(final_url)
            raw_df = pd.read_csv(final_url)

    query = ArcherExplorerForm()
    return render(request, 'ibhi/archer_explorer.html',
                  {'query': query,
                   'archer_explorer_list':raw_df.head(25),
                   'final_url': final_url},)


def export_csv_archer(request):
    global raw_df

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s.csv"' % str(datetime.datetime.now())

    column_names = ['aid', 'publication_date', 'ingest_date', 'source_name', 'url',

                    'title', 'title_length', 'content', 'content_length', 'publisher',

                    'other_metadata', 'extracted_people', 'extracted_people_text', 'extracted_locations',
                    'extracted_locations_text',

                    'extracted_organizations', 'extracted_organizations_text', 'country', 'geolocation_original',
                    'geolocation_locations',

                    'geolocation_locations_text', 'geolocation', 'geolocation_featureids',
                    'geolocation_probabilities', 'anew_arousal',

                    'anew_dominance', 'anew_valence', 'bing_liu_neg', 'bing_liu_pos', 'dal_activation',

                    'dal_imagery', 'dal_pleasantness', 'inquirer_neg', 'inquirer_pos', 'lexicoder_neg',
                    'lexicoder_pos',

                    'mf_moralitygeneral', 'mf_authorityvice', 'mf_authorityvirtue', 'mf_fairnessvice',
                    'mf_fairnessvirtue', 'mf_harmvice',

                    'mf_harmvirtue', 'mf_ingroupvice', 'mf_ingroupvirtue', 'mf_purityvice', 'mf_purityvirtue',
                    'pronouns', 'status']



    writer = csv.writer(response)
    writer.writerow(column_names)




    for index, row in raw_df.iterrows():
        writer.writerow([row['aid'], row['publication_date'], row['ingest_date'], row['source_name'], row['url'],

                row['title'], row['title_length'], row['content'], row['content_length'], row['publisher'],

                row['other_metadata'], row['extracted_people'], row['extracted_people_text'], row['extracted_locations'],
                row['extracted_locations_text'],

                row['extracted_organizations'], row['extracted_organizations_text'], row['country'], row['geolocation_original'],
                row['geolocation_locations'],

                row['geolocation_locations_text'], row['geolocation'], row['geolocation_featureids'],
                row['geolocation_probabilities'], row['anew_arousal'],

                row['anew_dominance'], row['anew_valence'], row['bing_liu_neg'], row['bing_liu_pos'], row['dal_activation'],

                row['dal_imagery'], row['dal_pleasantness'], row['inquirer_neg'], row['inquirer_pos'], row['lexicoder_neg'],
                row['lexicoder_pos'],

                row['mf_moralitygeneral'], row['mf_authorityvice'], row['mf_authorityvirtue'], row['mf_fairnessvice'],
                row['mf_fairnessvirtue'], row['mf_harmvice'],

                row['mf_harmvirtue'], row['mf_ingroupvice'], row['mf_ingroupvirtue'], row['mf_purityvice'], row['mf_purityvirtue'],
                row['pronouns'], row['status']])

    return response



