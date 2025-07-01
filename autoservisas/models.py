from datetime import date, datetime
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.db.models import CASCADE
from django.utils import timezone
from tinymce.models import HTMLField
from PIL import Image

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
    owner = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=True)
    l_plate = models.CharField(verbose_name="Valstybinis NR", max_length=6, help_text="Automobilio valstybinis NR")
    vin_code = models.CharField(verbose_name="VIN numeris", max_length=17, help_text="Automobilio kėbulo numeris")
    automodel = models.ForeignKey(to="AutoModel", verbose_name="Automobilio modelis", on_delete=models.SET_NULL, null=True, blank=True)
    description = HTMLField(verbose_name="Automobilio aprašymas", max_length=1000, null=True, blank=True)
    cover = models.ImageField('CarPic', upload_to='covers', null=True, blank=True)
    def __str__(self):
        return f"({self.owner}) {self.automodel}"

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
    order_date = models.DateField(verbose_name="Užsakymo data", default=date.today, null=True, blank=True)
    deadline_date = models.DateField(verbose_name="Remonto terminas (data)", null=True, blank=True)
    deadline_time = models.TimeField(verbose_name="Remonto terminals (laikas)", null=True, blank=True)
    auto = models.ForeignKey(to="Auto", verbose_name="Automobilis", on_delete=models.CASCADE, related_name='orders')


    ORDER_STATUS = (
        ('l', 'Laukiama'),
        ('v', 'Vykdoma'),
        ('n', 'Neapmokėta'),
        ('i', 'Įvykdyta'),
        ('x', 'Atšaukta'),
    )

    status = models.CharField(verbose_name='Būsena', max_length=1, choices=ORDER_STATUS, blank=True, default='l')

    def is_overdue(self):
        # if self.status == 'i':
        #     return False
        if self.deadline_date and self.deadline_time and self.status == 'v':
            deadline = datetime.combine(self.deadline_date, self.deadline_time)
            deadline = timezone.make_aware(deadline, timezone.get_current_timezone())
            return timezone.now() > deadline
        return False 


    def suma(self):
        total_suma = 0
        for line in self.lines.all():
            total_suma += line.kaina()
        total_suma = f'{total_suma:.2f}'
        return total_suma

    class Meta:
        verbose_name = "užsakymas"
        verbose_name_plural = "užsakymai"
        ordering = ['-order_date']

    def __str__(self):
        return f"Automobilio {self.auto} remonto užsakymas. Bendra suma: {self.suma()}"

class OrderLine(models.Model):
    service = models.ForeignKey(to="Service", verbose_name="Suteikta paslauga", on_delete=models.CASCADE)
    order_data = models.ForeignKey(to="OrderData", verbose_name="Užsakymas", on_delete=models.CASCADE, related_name="lines")
    qty = models.IntegerField(verbose_name="Kiekis", default=1, null=True, blank=True)

    def kaina(self):
        return self.service.price * self.qty

    kaina.short_description = "Kaina"

    def __str__(self):
        return f"{self.service.service_name} - {self.qty} vnt, kaina: {self.kaina():.2f}"

    class Meta:
        verbose_name = "užsakymo įrašas"
        verbose_name_plural = "užsakymo įrašai"

class Comment(models.Model):
    order = models.ForeignKey(to=OrderData, on_delete=models.CASCADE, null=True, blank=True, related_name="comments")
    date = models.DateTimeField(verbose_name="Data", auto_now_add=True)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True, blank=True, related_name="comments")
    content = models.TextField(verbose_name="Komentaras", max_length=500)

    class Meta:
        verbose_name = "komentaras"
        verbose_name_plural = "komentarai"
        ordering = ['-date']

class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=CASCADE)
    photo = models.ImageField(verbose_name="Nuotrauka", default="profile_pics/default.png", upload_to="profile_pics")
    is_employee = models.BooleanField(verbose_name="darbuotojas", default=False)

    def __str__(self):
        return f"{self.user.username} profilis."

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.photo.path)
        if img.height > 300 or img.width > 300:

            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.photo.path)