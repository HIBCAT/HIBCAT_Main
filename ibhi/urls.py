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
from ibhi.views import (BwVegaVisual1, BwVegaVisual2, BwVegaVisual3,
                        FluidLayoutView, BwVegaVisual4)


# The name parameter (like 'report_urlpattern)
# is the reference to the path (like 'report/'
# Whenever the path is to be referenced, it can be done
# using the name parameter.

urlpatterns = [

    # API

    path('visual_3.csv', BwVegaVisual3.as_view()),

    path('visual_1.csv', BwVegaVisual1.as_view()),

    path('visual_2.csv', BwVegaVisual2.as_view()),

    path('visual_4.csv', BwVegaVisual4.as_view()),

    path('fluid_report/',
         FluidLayoutView.as_view(),
         name='fluid_report_urlpattern'),


]
