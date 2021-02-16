# Generated by Django 3.1.5 on 2021-02-16 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ibhi', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BwActivityDay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dayOfWeek', models.IntegerField(blank=True, null=True)),
                ('day_vol', models.BigIntegerField(blank=True, null=True, verbose_name='Volume by Day')),
            ],
        ),
        migrations.CreateModel(
            name='BwActivityTime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hourOfDay', models.TimeField(blank=True, null=True, verbose_name='Time')),
                ('time_vol', models.BigIntegerField(blank=True, null=True, verbose_name='Volume by Time')),
            ],
        ),
        migrations.CreateModel(
            name='CCEventTimeline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True, verbose_name="Event's Start Date")),
                ('end_date', models.DateField(blank=True, null=True, verbose_name="Event's End Date")),
                ('event_type', models.CharField(choices=[('Positive Shock - Planned Activity', 'Positive Shock - Planned Activity'), ('Positive Shock - Unplanned Activity', 'Positive Shock - Unplanned Activity'), ('Negative Shock - Planned Activity', 'Negative Shock - Planned Activity'), ('Negative Shock - Unplanned Activity', 'Negative Shock - Unplanned Activity')], default='Positive Shock - Planned Activity', max_length=50, verbose_name='Event Type')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Event Description')),
            ],
        ),
        migrations.RemoveField(
            model_name='bwgeography',
            name='hibcat_monitor',
        ),
        migrations.RemoveField(
            model_name='bwnetsentiment',
            name='hibcat_monitor',
        ),
        migrations.RemoveField(
            model_name='bwvolume',
            name='hibcat_monitor',
        ),
        migrations.AddField(
            model_name='bwgeography',
            name='geo_vol',
            field=models.IntegerField(blank=True, null=True, verbose_name='Geographic Volume'),
        ),
        migrations.AddField(
            model_name='bwnetsentiment',
            name='net_sent_vol',
            field=models.FloatField(blank=True, null=True, verbose_name='Net Sentiment Volume'),
        ),
        migrations.AddField(
            model_name='bwsentiments',
            name='net_sentiment',
            field=models.FloatField(blank=True, null=True, verbose_name='Net Sentiment'),
        ),
        migrations.AddField(
            model_name='bwsentiments',
            name='volume',
            field=models.IntegerField(blank=True, null=True, verbose_name='Volume (Pos+Neg)'),
        ),
        migrations.AddField(
            model_name='bwvolume',
            name='volume',
            field=models.IntegerField(blank=True, null=True, verbose_name='Activity Volume'),
        ),
        migrations.AddField(
            model_name='clinecenter',
            name='bing_liu_net_sentiment',
            field=models.FloatField(blank=True, null=True, verbose_name='Bing Liu Net Sentiment'),
        ),
        migrations.AddField(
            model_name='clinecenter',
            name='publication_date_only',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='clinecenter',
            name='publication_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bwcontentsources',
            name='blogs',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Blogs'),
        ),
        migrations.AlterField(
            model_name='bwcontentsources',
            name='days',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bwcontentsources',
            name='reddit',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Reddit'),
        ),
        migrations.AlterField(
            model_name='bwcontentsources',
            name='twitter',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Twitter'),
        ),
        migrations.AlterField(
            model_name='bwemotions',
            name='anger',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Anger'),
        ),
        migrations.AlterField(
            model_name='bwemotions',
            name='days',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bwemotions',
            name='disgust',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Disgust'),
        ),
        migrations.AlterField(
            model_name='bwemotions',
            name='fear',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Fear'),
        ),
        migrations.AlterField(
            model_name='bwemotions',
            name='joy',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Fear'),
        ),
        migrations.AlterField(
            model_name='bwemotions',
            name='sadness',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Sadness'),
        ),
        migrations.AlterField(
            model_name='bwemotions',
            name='surprise',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Surprise'),
        ),
        migrations.AlterField(
            model_name='bwgeography',
            name='countries',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bwnetsentiment',
            name='days',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bwsentiments',
            name='days',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bwsentiments',
            name='negative',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='bwsentiments',
            name='neutral',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='bwsentiments',
            name='positive',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='bwvolume',
            name='days',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='clinecenter',
            name='aid',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='clinecenter',
            name='anew_arousal',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='clinecenter',
            name='anew_dominance',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='clinecenter',
            name='anew_valence',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='clinecenter',
            name='article_id',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='_id'),
        ),
        migrations.AlterField(
            model_name='clinecenter',
            name='bing_liu_neg',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='clinecenter',
            name='bing_liu_pos',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='clinecenter',
            name='country',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='clinecenter',
            name='dal_activation',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='clinecenter',
            name='dal_imagery',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='clinecenter',
            name='dal_pleasantness',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='clinecenter',
            name='extracted_locations',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='clinecenter',
            name='extracted_organizations',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='clinecenter',
            name='extracted_people',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='clinecenter',
            name='geolocation',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='clinecenter',
            name='geolocation_featureids',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='clinecenter',
            name='geolocation_locations',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='clinecenter',
            name='geolocation_original',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='clinecenter',
            name='geolocation_probabilities',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='clinecenter',
            name='inquirer_neg',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='clinecenter',
            name='inquirer_pos',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='clinecenter',
            name='lexicoder_neg',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='clinecenter',
            name='lexicoder_pos',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='clinecenter',
            name='mf_authorityvice',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='clinecenter',
            name='mf_authorityvirtue',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='clinecenter',
            name='mf_fairnessvice',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='clinecenter',
            name='mf_fairnessvirtue',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='clinecenter',
            name='mf_harmvice',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='clinecenter',
            name='mf_harmvirtue',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='clinecenter',
            name='mf_ingroupvice',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='clinecenter',
            name='mf_ingroupvirtue',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='clinecenter',
            name='mf_moralitygeneral',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='clinecenter',
            name='mf_purityvice',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='clinecenter',
            name='mf_purityvirtue',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='clinecenter',
            name='offset',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='clinecenter',
            name='original_language',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='clinecenter',
            name='other_metadata',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='clinecenter',
            name='pronouns',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='clinecenter',
            name='publication_date',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='clinecenter',
            name='publisher',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='clinecenter',
            name='source_host',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='clinecenter',
            name='source_location',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='clinecenter',
            name='source_name',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='clinecenter',
            name='title',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='clinecenter',
            name='url',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='gender',
            name='days',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='gender',
            name='female',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='gender',
            name='male',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='shortinterest',
            name='short_volume',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='shortinterest',
            name='short_volume_ratio',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='shortinterest',
            name='total_volume',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='yahoostockdata',
            name='adj_close',
            field=models.FloatField(blank=True, null=True, verbose_name='Adj Close'),
        ),
        migrations.AlterField(
            model_name='yahoostockdata',
            name='close',
            field=models.FloatField(blank=True, null=True, verbose_name='Close'),
        ),
        migrations.AlterField(
            model_name='yahoostockdata',
            name='date',
            field=models.DateField(blank=True, null=True, verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='yahoostockdata',
            name='high',
            field=models.FloatField(blank=True, null=True, verbose_name='High'),
        ),
        migrations.AlterField(
            model_name='yahoostockdata',
            name='low',
            field=models.FloatField(blank=True, null=True, verbose_name='Low'),
        ),
        migrations.AlterField(
            model_name='yahoostockdata',
            name='open',
            field=models.FloatField(blank=True, null=True, verbose_name='Open'),
        ),
    ]
