from django.db import models
from django.contrib.postgres.fields import ArrayField


class Pharmacy(models.Model):
    name = models.CharField(max_length=255, verbose_name="Pharmacy nam")
    logo = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Drug(models.Model):
    generic_name = ArrayField(models.CharField(max_length=255))
    brand_name = ArrayField(models.CharField(max_length=255))
    manufacturer = ArrayField(models.CharField(max_length=255))
    active_ingredient = ArrayField(models.CharField(max_length=255))
    dosage = ArrayField(models.CharField(max_length=255))
    route_of_administration = ArrayField(models.CharField(max_length=255))
    indications = ArrayField(models.CharField(max_length=255))
    contraindications = ArrayField(models.CharField(max_length=255))
    adverse_events = ArrayField(models.CharField(max_length=255))
    overdose = ArrayField(models.CharField(max_length=255))
    interactions = ArrayField(models.CharField(max_length=255))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"""{self.brand_name[0]} - {self.generic_name[0]}"""
