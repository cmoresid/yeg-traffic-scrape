"""Contains database entity models."""

from django.contrib.gis.db import models

class Site(models.Model):
    """Represents the site of a traffic event or intersection event.

    The site model represents a point of interest where traffic monitoring
    information was collected. There may be multiple types of events associated
    with a site, such as a TrafficEvent or an IntersectionEvent.
    """
    site_id = models.CharField(max_length=25, primary_key=True)
    address = models.CharField(max_length=255)
    location = models.PointField(srid=4326, null=True)
    adt = models.PositiveIntegerField(null=True)
    street_type = models.CharField(max_length=50, null=True)
    category = models.CharField(max_length=50, null=True)
    in_service = models.DateField(null=True)
    county = models.CharField(max_length=100, null=True)
    jurisdiction = models.CharField(max_length=100, null=True)
    primary_purpose = models.CharField(max_length=255, null=True)

    objects = models.GeoManager()

class TrafficVolumeEvent(models.Model):
    """Represents a traffic event occuring at a particular site.

    A traffic volume event captures the amount of traffic heading in
    a particular direction within a one hour period.
    """
    site_id = models.ForeignKey('Site')
    event_date_time = models.DateTimeField
    direction = models.CharField(max_length=3)
    count = models.PositiveIntegerField()

class IntersectionVolumeEvent(models.Model):
    """Represents an intersection event occuring at a particular site.

    An intersection volume event captures the amount of traffic changing
    directions at an intersection within a one hour period.
    """
    site_id = models.ForeignKey('Site')
    event_type = models.CharField(max_length=50)
    event_date_time = models.DateTimeField()
    direction = models.CharField(max_length=10)
    turn_direction = models.CharField(max_length=1, null=True)
    count = models.PositiveIntegerField()
