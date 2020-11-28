from django.contrib import admin
from .models import BwGeography, Gender, BwContentSources, BwNetSentiment, BwEmotions, BwSentiments, BwVolume, ClineCenter, YahooStockData, ShortInterest

# Register your models here.

admin.site.register(BwGeography)
admin.site.register(Gender)
admin.site.register(BwContentSources)
admin.site.register(BwNetSentiment)
admin.site.register(BwEmotions)
admin.site.register(BwSentiments)
admin.site.register(BwVolume)
admin.site.register(ClineCenter)
admin.site.register(YahooStockData)
admin.site.register(ShortInterest)