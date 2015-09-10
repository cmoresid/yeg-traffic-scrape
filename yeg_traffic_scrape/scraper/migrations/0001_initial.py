# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IntersectionVolumeEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('event_type', models.CharField(max_length=50)),
                ('event_date_time', models.DateTimeField()),
                ('direction', models.CharField(max_length=10)),
                ('turn_direction', models.CharField(max_length=1, null=True)),
                ('count', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('site_id', models.CharField(max_length=25, serialize=False, primary_key=True)),
                ('address', models.CharField(max_length=255)),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True)),
                ('adt', models.PositiveIntegerField(null=True)),
                ('street_type', models.CharField(max_length=50, null=True)),
                ('category', models.CharField(max_length=50, null=True)),
                ('in_service', models.DateField(null=True)),
                ('county', models.CharField(max_length=100, null=True)),
                ('jurisdiction', models.CharField(max_length=100, null=True)),
                ('primary_purpose', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TrafficVolumeEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('direction', models.CharField(max_length=3)),
                ('count', models.PositiveIntegerField()),
                ('site_id', models.ForeignKey(to='scraper.Site')),
            ],
        ),
        migrations.AddField(
            model_name='intersectionvolumeevent',
            name='site_id',
            field=models.ForeignKey(to='scraper.Site'),
        ),
    ]
