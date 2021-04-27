from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .models import BwGeography, Gender, BwContentSources, \
    BwNetSentiment, BwEmotions, BwSentiments, \
    BwVolume, BwActivityDay, BwActivityTime, \
    ClineCenter, YahooStockData, ShortInterest, \
    CCEventTimeline

admin.site.site_header = "HIBCAT Admin"
admin.site.site_title = "HIBCAT Admin Portal"
admin.site.index_title = "Welcome to HIBCAT Researcher Portal"

# Register your models here.
# 1
class BwGeographyResource(resources.ModelResource):

    class Meta:
        model = BwGeography

class BwGeographyAdmin(ImportExportModelAdmin):
    list_display = ('countries', 'brand', 'geo_vol')
    resource_class = BwGeographyResource

admin.site.register(BwGeography, BwGeographyAdmin)

# 2
class GenderResource(resources.ModelResource):
    class Meta:
        model = Gender


class GenderAdmin(ImportExportModelAdmin):
    list_display = ('days', 'male','brand', 'female')
    resource_class = GenderResource

admin.site.register(Gender, GenderAdmin)

# 3
class BwContentSourcesResource(resources.ModelResource):
    class Meta:
        model = BwContentSources


class BwContentSourcesAdmin(ImportExportModelAdmin):
    list_display = ('days','brand', 'blogs', 'twitter', 'reddit')
    resource_class = BwContentSourcesResource

admin.site.register(BwContentSources, BwContentSourcesAdmin)

# 4
class BwNetSentimentResource(resources.ModelResource):
    class Meta:
        model = BwNetSentiment


class BwNetSentimentAdmin(ImportExportModelAdmin):
    list_display = ('days', 'brand','net_sent_vol')
    resource_class = BwNetSentimentResource

admin.site.register(BwNetSentiment, BwNetSentimentAdmin)

# 5
class BwEmotionsResource(resources.ModelResource):
    class Meta:
        model = BwEmotions


class BwEmotionsAdmin(ImportExportModelAdmin):
    list_display = ('days','brand', 'anger', 'fear',
                    'disgust', 'joy', 'surprise', 'sadness')
    resource_class = BwEmotionsResource

admin.site.register(BwEmotions, BwEmotionsAdmin)

# 6
class BwSentimentsResource(resources.ModelResource):
    class Meta:
        model = BwSentiments


class BwSentimentsAdmin(ImportExportModelAdmin):
    list_display = ('days', 'brand','net_sentiment', 'positive', 'neutral', 'negative', 'volume')
    resource_class = BwSentimentsResource

admin.site.register(BwSentiments, BwSentimentsAdmin)

# 7
class BwVolumeResource(resources.ModelResource):
    class Meta:
        model = BwVolume


class BwVolumeAdmin(ImportExportModelAdmin):
    list_display = ('days', 'brand','volume')
    resource_class = BwVolumeResource

admin.site.register(BwVolume, BwVolumeAdmin)

# 8
class BwActivityDayResource(resources.ModelResource):
    class Meta:
        model = BwActivityDay

class BwActivityDayAdmin(ImportExportModelAdmin):
    list_display = ('dayOfWeek' ,'brand', 'day_vol')
    resource_class = BwActivityDayResource

admin.site.register(BwActivityDay, BwActivityDayAdmin)

# 9
class BwActivityTimeResource(resources.ModelResource):
    class Meta:
        model = BwActivityTime

class BwActivityTimeAdmin(ImportExportModelAdmin):
    list_display = ('hourOfDay' , 'brand','time_vol')
    resource_class = BwActivityTimeResource

admin.site.register(BwActivityTime, BwActivityTimeAdmin)

# 10
class ClineCenterResource(resources.ModelResource):
    class Meta:
        model = ClineCenter


class ClineCenterAdmin(ImportExportModelAdmin):
    list_display = ('publication_date', 'brand','publication_date_only', 'publication_time',
                    'bing_liu_net_sentiment', 'article_id', 'aid',
                    'source_name', 'source_location', 'url',
                    'title', 'source_host', 'publisher',
                    'pronouns', 'other_metadata', 'original_language',
                    'mf_harmvirtue', 'mf_purityvirtue', 'mf_purityvice',
                    'mf_moralitygeneral', 'mf_ingroupvirtue', 'mf_ingroupvice',
                    'mf_harmvice', 'mf_fairnessvice', 'mf_fairnessvirtue',
                    'mf_authorityvirtue', 'mf_authorityvice', 'dal_activation',
                    'dal_pleasantness', 'dal_imagery', 'lexicoder_pos',
                    'lexicoder_neg', 'inquirer_pos', 'inquirer_neg', 'bing_liu_neg',
                    'bing_liu_pos', 'anew_valence', 'anew_arousal',
                    'anew_dominance', 'offset', 'geolocation_probabilities',
                    'geolocation', 'geolocation_featureids', 'geolocation_original',
                    'extracted_organizations', 'geolocation_locations', 'extracted_people',
                    'extracted_locations', 'country')
    resource_class = ClineCenterResource

admin.site.register(ClineCenter, ClineCenterAdmin)

# 11
class YahooStockDataResource(resources.ModelResource):
    class Meta:
        model = YahooStockData


class YahooStockDataAdmin(ImportExportModelAdmin):
    list_display = ('date', 'brand','open', 'high', 'low',
                    'close', 'adj_close')
    resource_class = YahooStockDataResource

admin.site.register(YahooStockData, YahooStockDataAdmin)

# 12
class ShortInterestResource(resources.ModelResource):
    class Meta:
        model = ShortInterest


class ShortInterestAdmin(ImportExportModelAdmin):
    list_display = ('date', 'brand','short_volume',
                    'total_volume', 'short_volume_ratio')
    resource_class = ShortInterestResource

admin.site.register(ShortInterest, ShortInterestAdmin)

# 13
class CCEventTimelineResource(resources.ModelResource):
    class Meta:
        model = CCEventTimeline

class CCEventTimelineAdmin(ImportExportModelAdmin):
    list_display = ('date', 'brand','end_date',
                    'event_type', 'description')
    resource_class = CCEventTimelineResource

admin.site.register(CCEventTimeline, CCEventTimelineAdmin)
