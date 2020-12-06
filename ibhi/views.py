from django.shortcuts import render
from django.http.response import HttpResponse
from django.template import loader
from django.views import View

from .models import (BwGeography, Gender, BwContentSources,
                     BwNetSentiment, BwEmotions, BwSentiments, BwVolume,
                     ClineCenter, YahooStockData, ShortInterest,)

# Create your views here.

class IBHIReportView(View):

    def get(self, request):
        bw_geography = BwGeography.objects.all().values()
        gender = Gender.objects.all().values()
        bw_content_sources = BwContentSources.objects.all().values()
        bw_net_sentiment = BwNetSentiment.objects.all().values()
        bw_emotions = BwEmotions.objects.all().values()
        bw_sentiments = BwSentiments.objects.all().values()
        bw_volume = BwVolume.objects.all().values()
        cline_center = ClineCenter.objects.all().values()
        yahoo_stock_data = YahooStockData.objects.all().values()
        short_interest = ShortInterest.objects.all().values()

        return render(request,
                      'ibhi/report.html',
                      {'bw_geography' : bw_geography,
                       'gender' : gender,
                       'bw_content_sources' : bw_content_sources,
                       'bw_net_sentiment' : bw_net_sentiment,
                       'bw_emotions' : bw_emotions,
                       'bw_sentiments' : bw_sentiments,
                       'bw_volume' : bw_volume,
                       'cline_center' : cline_center,
                       'yahoo_stock_data' : yahoo_stock_data,
                       'short_interest' : short_interest
                       }
                      )

class IBHIInsightsView(View):

    def get(self, request):
        bw_geography = BwGeography.objects.all().values()
        gender = Gender.objects.all().values()
        bw_content_sources = BwContentSources.objects.all().values()
        bw_net_sentiment = BwNetSentiment.objects.all().values()
        bw_emotions = BwEmotions.objects.all().values()
        bw_sentiments = BwSentiments.objects.all().values()
        bw_volume = BwVolume.objects.all().values()
        cline_center = ClineCenter.objects.all().values()
        yahoo_stock_data = YahooStockData.objects.all().values()
        short_interest = ShortInterest.objects.all().values()

        return render(request,
                      'ibhi/insights.html',
                      {'bw_geography' : bw_geography,
                       'gender' : gender,
                       'bw_content_sources' : bw_content_sources,
                       'bw_net_sentiment' : bw_net_sentiment,
                       'bw_emotions' : bw_emotions,
                       'bw_sentiments' : bw_sentiments,
                       'bw_volume' : bw_volume,
                       'cline_center' : cline_center,
                       'yahoo_stock_data' : yahoo_stock_data,
                       'short_interest' : short_interest
                       }
                      )

class IBHIBeliefsView(View):

    def get(self, request):
        bw_geography = BwGeography.objects.all().values()
        gender = Gender.objects.all().values()
        bw_content_sources = BwContentSources.objects.all().values()
        bw_net_sentiment = BwNetSentiment.objects.all().values()
        bw_emotions = BwEmotions.objects.all().values()
        bw_sentiments = BwSentiments.objects.all().values()
        bw_volume = BwVolume.objects.all().values()
        cline_center = ClineCenter.objects.all().values()
        yahoo_stock_data = YahooStockData.objects.all().values()
        short_interest = ShortInterest.objects.all().values()

        return render(request,
                      'ibhi/beliefs.html',
                      {'bw_geography' : bw_geography,
                       'gender' : gender,
                       'bw_content_sources' : bw_content_sources,
                       'bw_net_sentiment' : bw_net_sentiment,
                       'bw_emotions' : bw_emotions,
                       'bw_sentiments' : bw_sentiments,
                       'bw_volume' : bw_volume,
                       'cline_center' : cline_center,
                       'yahoo_stock_data' : yahoo_stock_data,
                       'short_interest' : short_interest
                       }
                      )

class IBHIPitchView(View):

    def get(self, request):
        bw_geography = BwGeography.objects.all().values()
        gender = Gender.objects.all().values()
        bw_content_sources = BwContentSources.objects.all().values()
        bw_net_sentiment = BwNetSentiment.objects.all().values()
        bw_emotions = BwEmotions.objects.all().values()
        bw_sentiments = BwSentiments.objects.all().values()
        bw_volume = BwVolume.objects.all().values()
        cline_center = ClineCenter.objects.all().values()
        yahoo_stock_data = YahooStockData.objects.all().values()
        short_interest = ShortInterest.objects.all().values()

        return render(request,
                      'ibhi/pitch.html',
                      {'bw_geography' : bw_geography,
                       'gender' : gender,
                       'bw_content_sources' : bw_content_sources,
                       'bw_net_sentiment' : bw_net_sentiment,
                       'bw_emotions' : bw_emotions,
                       'bw_sentiments' : bw_sentiments,
                       'bw_volume' : bw_volume,
                       'cline_center' : cline_center,
                       'yahoo_stock_data' : yahoo_stock_data,
                       'short_interest' : short_interest
                       }
                      )
