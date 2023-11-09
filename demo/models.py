from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    
    def get_current_manager(user):
        return Manager.objects.get(user=user)

    def __str__(self):
        return self.user.username


class UserPreference(models.Model):
    user = models.OneToOneField(Manager, on_delete=models.CASCADE, primary_key=True)
    preferred_theme = models.CharField(
        max_length=8, 
        choices=[
            ("dark", "dark"),
            ("light", "light"),
        ],
        blank=True,
    )

    def get_user_preferences(user):
        return UserPreference.objects.get(user=user) 

    def set_user_preferred_theme(user, theme):
        UserPreference.objects.filter(user=user).update(preferred_theme=theme)

    def __str__(self):
        return f"""{self.user}: {self.preferred_theme}"""


class OpenFDADrug(models.Model):
    application_number = ArrayField(models.CharField(max_length=255))
    brand_name = ArrayField(models.CharField(max_length=255))
    generic_name = ArrayField(models.CharField(max_length=255))
    manufacturer_name = ArrayField(models.CharField(max_length=255))
    product_ndc = ArrayField(models.CharField(max_length=255))
    product_type = ArrayField(models.CharField(max_length=255))
    route = ArrayField(models.CharField(max_length=255))
    substance_name = ArrayField(models.CharField(max_length=255))
    rxcui = ArrayField(models.CharField(max_length=255))
    spl_id = ArrayField(models.CharField(max_length=255))
    spl_set_id = ArrayField(models.CharField(max_length=255))
    package_ndc = ArrayField(models.CharField(max_length=255))
    is_original_packager = ArrayField(models.CharField(max_length=255))
    upc = ArrayField(models.CharField(max_length=255))
    unii = ArrayField(models.CharField(max_length=255))

    def __str__(self):
        return f"""{self.generic_name} - {self.brand_name}"""

class Drug(models.Model):
    drug_id = models.CharField(max_length=255, primary_key=True)
    set_id = models.CharField(max_length=255)
    effective_time = models.CharField(max_length=255)
    version = models.CharField(max_length=255)

    spl_product_data_elements = ArrayField(models.TextField())
    active_ingredient = ArrayField(models.TextField())
    purpose = ArrayField(models.TextField())
    indications_and_usage = ArrayField(models.TextField())
    warnings = ArrayField(models.TextField())
    do_not_use = ArrayField(models.TextField())
    ask_doctor = ArrayField(models.TextField())
    ask_doctor_or_pharmacist = ArrayField(models.TextField())
    stop_use = ArrayField(models.TextField())
    pregnancy_or_breast_feeding = ArrayField(models.TextField())
    keep_out_of_reach_of_children = ArrayField(models.TextField())
    dosage_and_administration = ArrayField(models.TextField())
    storage_and_handling = ArrayField(models.TextField())
    inactive_ingredient = ArrayField(models.TextField())
    questions = ArrayField(models.TextField())
    package_label_principal_display_panel = ArrayField(models.TextField())

    open_fda = models.OneToOneField(
        OpenFDADrug, on_delete=models.CASCADE, verbose_name="OpenFDA label")

    def __str__(self):
        return f"""{self.open_fda.generic_name} - {self.open_fda.brand_name}"""


class Pharmacy(models.Model):
    name = models.CharField(max_length=255, verbose_name="Pharmacy name", unique=True)
    logo = models.ImageField(blank=True)
    drugs = models.ManyToManyField(Drug, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)

    def filter_managed_pharmacies(user):
        return Pharmacy.objects.filter(manager=user)

    def filter_pharmacy_drugs(user, pharmacy_id):
        return Pharmacy.filter_managed_pharmacies(user).get(id=pharmacy_id).drugs.all()
        
    def __str__(self):
        return self.name
