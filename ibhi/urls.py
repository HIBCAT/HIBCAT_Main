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
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from ibhi.views import (IBHIReportView, IBHIInsightsView, IBHIBeliefsView,
                        IBHIPitchView, SMOperations)


# 1.
# The name parameter (like 'report_urlpattern)
# is the reference to the path (like 'report/'
# Whenever the path is to be referenced, it can be done
# using the name parameter.


# 2. REST api
# Step 1. serializers.py
# Step 2. views.py : Run the desired python data analysis operations.
# Step 3. urls.py : Register the link you want to broadcast your data on.


urlpatterns = [

    path('report/',
         IBHIReportView.as_view(),
         name='report_urlpattern'),

    path('insights/',
         IBHIInsightsView.as_view(),
         name='insights_urlpattern'),

    path('beliefs/',
         IBHIBeliefsView.as_view(),
         name='beliefs_urlpattern'),

    path('pitch/',
         IBHIPitchView.as_view(),
         name='pitch_urlpattern'),

    path('stock_api', SMOperations.as_view())

]

urlpatterns = format_suffix_patterns(urlpatterns)
