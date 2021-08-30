from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Resource(models.Model):
    REUNION = 'RE'
    VISIO = 'VI'
    ROOM_CHOICES = [
        (REUNION, 'Salle de réunion'),
        (VISIO, 'Salle de visioconférence'),

    ]
    label = models.CharField(max_length=100, verbose_name='Libellé')
    type_resource = models.TextField(max_length=2, choices=ROOM_CHOICES, default=REUNION,
                                     verbose_name='Type de ressource')
    location = models.CharField(max_length=100, verbose_name='Localisation')
    capacity = models.IntegerField(verbose_name='Capacité')

    def __str__(self):
        return self.label


class Booking(models.Model):
    title = models.CharField(max_length=100, verbose_name='Titre')
    start_date = models.DateTimeField(verbose_name='Date de début')
    end_date = models.DateTimeField(verbose_name='Date de fin')
    resource = models.ForeignKey('Resource', on_delete=models.CASCADE, verbose_name='Ressource')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
