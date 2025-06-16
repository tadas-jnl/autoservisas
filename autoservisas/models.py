from tkinter.constants import CASCADE
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class AutoModel(models.Model):
    make = models.CharField(verbose_name="Gamintojas", max_length=200, help_text="Automobilio gamintojas")
    model = models.CharField(verbose_name="Modelis", max_length=200, help_text="Automobilio modelis")
    year = models.IntegerField(verbose_name='Pagaminimo metai',
                               validators=[MinValueValidator(1900), MaxValueValidator(2026)],
                               default=None, null=True, blank=True)
    def __str__(self):
        return f'{self.make} {self.model} ({self.year})'
    class Meta:
        verbose_name = "automobilio modelis"
        verbose_name_plural = "Automobilių modeliai"

class Auto(models.Model):
    l_plate = models.CharField(verbose_name="Valstybinis NR", max_length=6, help_text="Automobilio valstybinis NR")
    vin_code = models.CharField(verbose_name="VIN numeris", max_length=17, help_text="Automobilio kėbulo numeris")
    client = models.CharField(verbose_name="Klientas", max_length=100)
    automodel = models.ForeignKey(to="AutoModel", verbose_name="Automobilio modelis", on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return f"{self.client} - ({self.l_plate}) {self.automodel}"

    class Meta:
        verbose_name = "automobilis"
        verbose_name_plural = "automobiliai"

class Service(models.Model):
    service_name = models.CharField(verbose_name="Paslaugos pavadinimas", max_length=200, help_text="Suteiktos paslaugos aprašymas")
    price = models.FloatField(verbose_name="Paslaugos kaina", max_length=10)
    def __str__(self):
        return f"{self.service_name}: {self.price}€"
    class Meta:
        verbose_name = "paslauga"
        verbose_name_plural = "paslaugos"

class OrderData(models.Model):
    order_date = models.DateField(verbose_name="Užsakymo data", null=True, blank=True)
    auto = models.ForeignKey(to="Auto", verbose_name="Automobilis", on_delete=models.SET_NULL, null=True, blank=True)

    def suma(self):
        total_suma = 0
        for line in self.lines.all():
            total_suma += line.kaina()
        total_suma = f'{total_suma:.2f}'
        return total_suma

    class Meta:
        verbose_name = "užsakymas"
        verbose_name_plural = "užsakymai"

    def __str__(self):
        return f"Automobilio {self.auto} remonto užsakymas. Bendra suma: {self.suma()}"

class OrderLine(models.Model):
    service = models.ForeignKey(to="Service", verbose_name="Suteikta paslauga", on_delete=models.CASCADE)
    order_data = models.ForeignKey(to="OrderData", verbose_name="Užsakymas", on_delete=models.CASCADE, related_name="lines")
    qty = models.IntegerField(verbose_name="Kiekis", null=True, blank=True)

    def kaina(self):
        return self.service.price * self.qty

    kaina.short_description = "Kaina"

    def __str__(self):
        return f"{self.service.service_name} - {self.qty} vnt, kaina: {self.kaina():.2f}"

    class Meta:
        verbose_name = "užsakymo įrašas"
        verbose_name_plural = "užsakymo įrašai"
