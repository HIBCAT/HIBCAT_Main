from django.db import models

# 1. Creating the database models over here.

class BwGeography(models.Model):
    countries = models.CharField(max_length=100, blank=False)
    hibcat_monitor = models.IntegerField(verbose_name="HIBCAT Monitor")

class Gender(models.Model):
    days = models.DateTimeField()
    male = models.IntegerField(default=0)
    female = models.IntegerField(default=0)

class BwContentSources(models.Model):
    days = models.DateTimeField()
    blogs = models.IntegerField(verbose_name="Blogs", default=0)
    twitter = models.IntegerField(verbose_name="Twitter", default=0)
    reddit = models.IntegerField(verbose_name="Reddit", default=0)

class BwNetSentiment(models.Model):
    days = models.DateTimeField()
    hibcat_monitor = models.FloatField(verbose_name="HIBCAT Monitor")

class BwEmotions(models.Model):
    days = models.DateTimeField()
    anger = models.IntegerField(verbose_name="Anger", default=0)
    fear = models.IntegerField(verbose_name="Fear", default=0)
    disgust = models.IntegerField(verbose_name="Disgust", default=0)
    joy = models.IntegerField(verbose_name="Fear", default=0)
    surprise = models.IntegerField(verbose_name="Surprise", default=0)
    sadness = models.IntegerField(verbose_name="Sadness", default=0)

class BwSentiments(models.Model):
    days = models.DateTimeField()
    positive = models.IntegerField(default=0)
    neutral = models.IntegerField(default=0)
    negative = models.IntegerField(default=0)

class BwVolume(models.Model):
    days = models.DateTimeField()
    hibcat_monitor = models.IntegerField(verbose_name="HIBCAT Monitor")

class ClineCenter(models.Model):
    publication_date = models.DateTimeField()
    article_id = models.CharField(verbose_name="_id", max_length=100)
    aid = models.IntegerField()
    source_name = models.CharField(max_length=100)
    source_location = models.CharField(max_length=100)
    url = models.URLField()
    title = models.TextField()
    source_host = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    pronouns = models.IntegerField()
    other_metadata = models.TextField()
    original_language = models.CharField(max_length=100)
    mf_harmvirtue = models.FloatField()
    mf_purityvirtue = models.FloatField()
    mf_purityvice = models.FloatField()
    mf_moralitygeneral = models.FloatField()
    mf_ingroupvirtue = models.FloatField()
    mf_ingroupvice = models.FloatField()
    mf_harmvice = models.FloatField()
    mf_fairnessvice = models.FloatField()
    mf_fairnessvirtue = models.FloatField()
    mf_authorityvirtue = models.FloatField()
    mf_authorityvice = models.FloatField()
    dal_activation = models.FloatField()
    dal_pleasantness = models.FloatField()
    dal_imagery = models.FloatField()
    lexicoder_pos = models.FloatField()
    lexicoder_neg = models.FloatField()
    inquirer_pos = models.FloatField()
    inquirer_neg = models.FloatField()
    bing_liu_neg = models.FloatField()
    bing_liu_pos = models.FloatField()
    anew_valence = models.FloatField()
    anew_arousal = models.FloatField()
    anew_dominance = models.FloatField()
    offset = models.FloatField()
    geolocation_probabilities = models.TextField()
    geolocation = models.TextField()
    geolocation_featureids = models.TextField()
    geolocation_original = models.TextField()
    extracted_organizations = models.TextField()
    geolocation_locations = models.TextField()
    extracted_people = models.TextField()
    extracted_locations = models.TextField()
    country = models.TextField()

class YahooStockData(models.Model):
    date = models.DateTimeField(verbose_name="Date")
    open = models.FloatField(verbose_name="Open")
    high = models.FloatField(verbose_name="High")
    low = models.FloatField(verbose_name="Low")
    close = models.FloatField(verbose_name="Close")
    adj_close = models.FloatField(verbose_name="Adj Close")

class ShortInterest(models.Model):
    date = models.ForeignKey(YahooStockData, related_name="shortinterests", on_delete=models.PROTECT)
    short_volume = models.IntegerField()
    total_volume = models.IntegerField()
    short_volume_ratio = models.FloatField()







