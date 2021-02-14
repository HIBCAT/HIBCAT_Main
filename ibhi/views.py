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
feature_1_cc = pd.DataFrame(ClineCenter.objects.all().values('publication_date_only', 'bing_liu_net_sentiment'))



# 1. BwActivityDay object
#day_wise_vol_main = pd.DataFrame(ClineCenter.objects.all().values('publication_date_only', 'bing_liu_net_sentiment'))
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

        return brandwatch_01

    def cline_center_df(self):
        # Feature one:
        # Part 2: Cline Center

        # As the test is successful, I will perform the analysis on the real data.
        # 1. Perform analysis on real data
        # 2. Add the columns with volume and standardized score
        # 3. Melt the columns

        # 1:
        clinecenter_01 = feature_1_cc.copy(deep=True)
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

        return clinecenter_02

    def write_data(self):
        # Now below is the full code for the part one of the Feature one:
        # Part 1: BrandWatch Dataset
        brand_watch = BwVegaVisual1.brand_watch_df(self)

        # Part 2: Cline Center Dataset
        cline_center = BwVegaVisual1.cline_center_df(self)

        # Part 3: Event Timeline Dataset

        # Part 4: Merging the three datasets
        feature_1_dataset = pd.concat([brand_watch, cline_center])
        return feature_1_dataset.shape

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


