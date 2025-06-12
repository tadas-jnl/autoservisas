from tkinter.constants import CASCADE

from django.db import models

# Create your models here.
class AutoModel(models.Model):
    model = models.CharField(verbose_name="Markė", max_length=200, help_text="Automobilio modelis")
    make = models.CharField(verbose_name="Markė", max_length=200, help_text="Modelis")
    def __str__(self):
        return f'{self.model} {self.make}'

class Auto(models.Model):
    l_plate = models.CharField(verbose_name="Valstybinis NR", max_length=6, help_text="Automobilio valstybinis NR")
    vin_code = models.CharField(verbose_name="VIN numeris", max_length=17, help_text="Automobilio kėbulo numeris")
    client = models.CharField(verbose_name="Klientas", max_length=100)
    automodel = models.ForeignKey(to="AutoModel", verbose_name="Automobilio modelis", on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return f"{self.client} - ({self.l_plate}) {self.automodel}"

class Service(models.Model):
    service_name = models.CharField(verbose_name="Paslaugos pavadinimas", max_length=200, help_text="Suteiktos paslaugos aprašymas")
    price = models.FloatField(verbose_name="Paslaugos kaina", max_length=10)
    def __str__(self):
        return f"{self.service_name}: {self.price}€"

class OrderData(models.Model):
    order_date = models.DateField(verbose_name="Užsakymo data", null=True, blank=True)
    auto = models.ForeignKey(to="Auto", verbose_name="Automobilis", on_delete=models.SET_NULL, null=True, blank=True)
    #not finishd

class OrderLine(models.Model):
    service = models.ForeignKey(to="Service", verbose_name="Suteikta paslauga", on_delete=models.CASCADE)
    order_data = models.ForeignKey(to="OrderData", verbose_name="Užsakymas", on_delete=models.CASCADE)
    qty = models.IntegerField(verbose_name="Kiekis", null=True, blank=True)
    #not finishd

