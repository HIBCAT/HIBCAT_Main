from django.db import models
import pandas as pd

# 1. Creating the database models over here.

class BwGeography(models.Model):
    countries = models.TextField(null=True, blank=True)
    geo_vol = models.IntegerField(null=True, blank=True, verbose_name="Geographic Volume")

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
    net_sent_vol = models.FloatField(null=True, blank=True, verbose_name="Net Sentiment Volume")

class BwEmotions(models.Model):
    days = models.DateField(null=True, blank=True)
    anger = models.IntegerField(null=True, blank=True, verbose_name="Anger", default=0)
    fear = models.IntegerField(null=True, blank=True, verbose_name="Fear", default=0)
    disgust = models.IntegerField(null=True, blank=True, verbose_name="Disgust", default=0)
    joy = models.IntegerField(null=True, blank=True, verbose_name="Fear", default=0)
    surprise = models.IntegerField(null=True, blank=True, verbose_name="Surprise", default=0)
    sadness = models.IntegerField(null=True, blank=True, verbose_name="Sadness", default=0)

class BwSentiments(models.Model):
    """
    The net sentiment is not normalized here.
    Normalize it on the scale of 0 to 100.
    """
    days = models.DateField(null=True, blank=True)
    positive = models.IntegerField(null=True, blank=True, default=0)
    neutral = models.IntegerField(null=True, blank=True, default=0)
    negative = models.IntegerField(null=True, blank=True, default=0)
    net_sentiment = models.FloatField(null=True, blank=True, verbose_name="Net Sentiment")
    volume = models.IntegerField(null=True, blank=True, verbose_name="Volume (Pos+Neg)")

    def save(self):
        """
        Avoid the error:
        ZeroDivisionError: division by zero
        :return:
        """
        difference = self.positive - self.negative
        self.volume = self.positive + self.negative
        if difference != 0:
            self.net_sentiment = difference/self.volume
        else:
            self.net_sentiment = 0

        super(BwSentiments, self).save()



class BwVolume(models.Model):
    days = models.DateField(null=True, blank=True)
    volume = models.IntegerField(null=True, blank=True, verbose_name="Activity Volume")

class BwActivityDay(models.Model):
    dayOfWeek = models.IntegerField(null=True, blank=True)
    day_vol = models.BigIntegerField("Volume by Day", null=True, blank=True)

class BwActivityTime(models.Model):
    hourOfDay = models.TimeField("Time", null=True, blank=True)
    time_vol = models.BigIntegerField("Volume by Time", null=True, blank=True)

class ClineCenter(models.Model):
    """
    The net sentiment is not normalized over here.
    Do it on a scale of 0 to 100.
    """
    publication_date = models.TextField(null=True, blank=True)
    publication_date_only = models.DateField(null=True, blank=True)
    publication_time = models.TimeField(null=True, blank=True)
    article_id = models.CharField(null=True, blank=True, verbose_name="_id", max_length=100)
    aid = models.TextField(null=True, blank=True)
    source_name = models.TextField(null=True, blank=True)
    source_location = models.TextField(null=True, blank=True)
    url = models.TextField(null=True, blank=True)
    title = models.TextField(null=True, blank=True)
    source_host = models.TextField(null=True, blank=True)
    publisher = models.TextField(null=True, blank=True)
    pronouns = models.IntegerField(null=True, blank=True)
    other_metadata = models.TextField(null=True, blank=True)
    original_language = models.TextField(null=True, blank=True)
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
    bing_liu_net_sentiment = models.FloatField(null=True, blank=True, verbose_name="Bing Liu Net Sentiment")
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

    def save(self):
        """
        Avoid:
        ZeroDivisionError: division by zero

        As some rows are having no values, they are NoneType,
        thus I'm ignoring them by putting != None clause.
        :return:
        """
        date = pd.to_datetime(self.publication_date)
        self.publication_date_only = date.date()
        self.publication_time = date.time()

        if self.bing_liu_pos != None:
            if self.bing_liu_pos > self.bing_liu_neg:
                self.bing_liu_net_sentiment = 1
            elif self.bing_liu_neg > self.bing_liu_pos:
                self.bing_liu_net_sentiment = -1
            else:
                self.bing_liu_net_sentiment = 0
        else:
            pass

        super(ClineCenter, self).save()


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

class CCEventTimeline(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('Positive Shock - Planned Activity', 'Positive Shock - Planned Activity'),
        ('Positive Shock - Unplanned Activity', 'Positive Shock - Unplanned Activity'),
        ('Negative Shock - Planned Activity', 'Negative Shock - Planned Activity'),
        ('Negative Shock - Unplanned Activity', 'Negative Shock - Unplanned Activity'),
    ]
    date = models.DateField(null=True, blank=True, verbose_name="Event's Start Date")
    end_date = models.DateField(null=True, blank=True, verbose_name="Event's End Date")
    event_type = models.CharField(max_length=50, choices=MEDIA_TYPE_CHOICES, default='Positive Shock - Planned Activity', verbose_name="Event Type")
    description = models.TextField(null=True, blank=True, verbose_name="Event Description")


