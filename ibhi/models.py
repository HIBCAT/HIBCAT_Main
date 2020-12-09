from django.db import models

# 1. Creating the database models over here.

class BwGeography(models.Model):
    countries = models.CharField(null=True, blank=True, max_length=100)
    hibcat_monitor = models.IntegerField(null=True, blank=True, verbose_name="HIBCAT Monitor")

class Gender(models.Model):
    days = models.DateField(null=True, blank=True)
    male = models.IntegerField(null=True, blank=True, default=0)
    female = models.IntegerField(null=True, blank=True, default=0)

class BwContentSources(models.Model):
    days = models.DateField(null=True, blank=True)
    blogs = models.IntegerField(null=True, blank=True, verbose_name="Blogs", default=0)
    twitter = models.IntegerField(null=True, blank=True, verbose_name="Twitter", default=0)
    reddit = models.IntegerField(null=True, blank=True, verbose_name="Reddit", default=0)

class BwNetSentiment(models.Model):
    days = models.DateField(null=True, blank=True)
    hibcat_monitor = models.FloatField(null=True, blank=True, verbose_name="HIBCAT Monitor")

class BwEmotions(models.Model):
    days = models.DateField(null=True, blank=True)
    anger = models.IntegerField(null=True, blank=True, verbose_name="Anger", default=0)
    fear = models.IntegerField(null=True, blank=True, verbose_name="Fear", default=0)
    disgust = models.IntegerField(null=True, blank=True, verbose_name="Disgust", default=0)
    joy = models.IntegerField(null=True, blank=True, verbose_name="Fear", default=0)
    surprise = models.IntegerField(null=True, blank=True, verbose_name="Surprise", default=0)
    sadness = models.IntegerField(null=True, blank=True, verbose_name="Sadness", default=0)

class BwSentiments(models.Model):
    days = models.DateField(null=True, blank=True)
    positive = models.IntegerField(null=True, blank=True, default=0)
    neutral = models.IntegerField(null=True, blank=True, default=0)
    negative = models.IntegerField(null=True, blank=True, default=0)

class BwVolume(models.Model):
    days = models.DateField(null=True, blank=True)
    hibcat_monitor = models.IntegerField(null=True, blank=True, verbose_name="HIBCAT Monitor")

class ClineCenter(models.Model):
    publication_date = models.DateTimeField(null=True, blank=True)
    article_id = models.CharField(null=True, blank=True, verbose_name="_id", max_length=100)
    aid = models.IntegerField(null=True, blank=True)
    source_name = models.CharField(null=True, blank=True, max_length=100)
    source_location = models.CharField(null=True, blank=True, max_length=100)
    url = models.URLField(null=True, blank=True)
    title = models.TextField(null=True, blank=True)
    source_host = models.CharField(null=True, blank=True, max_length=100)
    publisher = models.CharField(null=True, blank=True, max_length=100)
    pronouns = models.IntegerField(null=True, blank=True)
    other_metadata = models.TextField(null=True, blank=True)
    original_language = models.CharField(null=True, blank=True, max_length=100)
    mf_harmvirtue = models.FloatField(null=True, blank=True)
    mf_purityvirtue = models.FloatField(null=True, blank=True)
    mf_purityvice = models.FloatField(null=True, blank=True)
    mf_moralitygeneral = models.FloatField(null=True, blank=True)
    mf_ingroupvirtue = models.FloatField(null=True, blank=True)
    mf_ingroupvice = models.FloatField(null=True, blank=True)
    mf_harmvice = models.FloatField(null=True, blank=True)
    mf_fairnessvice = models.FloatField(null=True, blank=True)
    mf_fairnessvirtue = models.FloatField(null=True, blank=True)
    mf_authorityvirtue = models.FloatField(null=True, blank=True)
    mf_authorityvice = models.FloatField(null=True, blank=True)
    dal_activation = models.FloatField(null=True, blank=True)
    dal_pleasantness = models.FloatField(null=True, blank=True)
    dal_imagery = models.FloatField(null=True, blank=True)
    lexicoder_pos = models.FloatField(null=True, blank=True)
    lexicoder_neg = models.FloatField(null=True, blank=True)
    inquirer_pos = models.FloatField(null=True, blank=True)
    inquirer_neg = models.FloatField(null=True, blank=True)
    bing_liu_neg = models.FloatField(null=True, blank=True)
    bing_liu_pos = models.FloatField(null=True, blank=True)
    anew_valence = models.FloatField(null=True, blank=True)
    anew_arousal = models.FloatField(null=True, blank=True)
    anew_dominance = models.FloatField(null=True, blank=True)
    offset = models.FloatField(null=True, blank=True)
    geolocation_probabilities = models.TextField(null=True, blank=True)
    geolocation = models.TextField(null=True, blank=True)
    geolocation_featureids = models.TextField(null=True, blank=True)
    geolocation_original = models.TextField(null=True, blank=True)
    extracted_organizations = models.TextField(null=True, blank=True)
    geolocation_locations = models.TextField(null=True, blank=True)
    extracted_people = models.TextField(null=True, blank=True)
    extracted_locations = models.TextField(null=True, blank=True)
    country = models.TextField(null=True, blank=True)

class YahooStockData(models.Model):
    date = models.DateField(null=True, blank=True, verbose_name="Date")
    open = models.FloatField(null=True, blank=True, verbose_name="Open")
    high = models.FloatField(null=True, blank=True, verbose_name="High")
    low = models.FloatField(null=True, blank=True, verbose_name="Low")
    close = models.FloatField(null=True, blank=True, verbose_name="Close")
    adj_close = models.FloatField(null=True, blank=True, verbose_name="Adj Close")

class ShortInterest(models.Model):
    date = models.ForeignKey(YahooStockData, related_name="shortinterests", on_delete=models.PROTECT)
    short_volume = models.IntegerField(null=True, blank=True)
    total_volume = models.IntegerField(null=True, blank=True)
    short_volume_ratio = models.FloatField(null=True, blank=True)


