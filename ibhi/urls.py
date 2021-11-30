"""HIBCAT_Main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ibhi.views import (BwVegaAdInvestmentVis, AdInvestmentView,
                        BwNewsExplorerVis, NewsExplorerView,
                        BwNetSentimentExplorerVis, NetSentimentExplorerView,
                        BwSentimentTrendVis, SentimentTrendView, WordCloudView,
                        archer_explorer,

                        ResearchPapersList, APIDataDictionaryList,
                        RawDataDictionaryList, InternalLinksList, IdeasList
                        )


# The name parameter (like 'report_urlpattern)
# is the reference to the path (like 'report/'
# Whenever the path is to be referenced, it can be done
# using the name parameter.

urlpatterns = [

    # Amazon Web Services API urls

    path('ad_investment.csv',
         BwVegaAdInvestmentVis.as_view(),
         name='ad_investment_api'),

    path('news_explorer.csv',
         BwNewsExplorerVis.as_view(),
         name='news_explorer_api'),

    path('net_sentiment_explorer.csv',
         BwNetSentimentExplorerVis.as_view(),
         name='net_sentiment_explorer_api'),

    path('sentiment_trend.csv',
         BwSentimentTrendVis.as_view(),
         name='sentiment_trend_api'),

    # Visualization urls

    path('ad_investment/',
         AdInvestmentView.as_view(),
         name='ad_investment_urlpattern'),

    path('news_explorer/',
         NewsExplorerView.as_view(),
         name='news_explorer_urlpattern'),

    path('net_sentiment_explorer/',
         NetSentimentExplorerView.as_view(),
         name='net_sentiment_explorer_urlpattern'),

    path('sentiment_trend/',
         SentimentTrendView.as_view(),
         name='sentiment_trend_urlpattern'),

    path('word_cloud/',
         WordCloudView.as_view(),
         name='word_cloud_urlpattern'),

    # Archer API
    path('archer/',
         archer_explorer,
         name='archer_explorer_urlpattern'),

    # Reserach Tab Urls

    path('researchpapers/', ResearchPapersList.as_view(),
         name='ibhi_researchpapers_list_urlpattern'),

    path('apidatadictionary/', APIDataDictionaryList.as_view(),
         name='ibhi_apidatadictionary_list_urlpattern'),

    path('rawdatadictionary/', RawDataDictionaryList.as_view(),
         name='ibhi_rawdatadictionary_list_urlpattern'),

    path('internallinks/', InternalLinksList.as_view(),
         name='ibhi_internallinks_list_urlpattern'),

    path('ideas/', IdeasList.as_view(),
         name='ibhi_ideas_list_urlpattern'),


]
