from django.contrib import admin
from .models import Resource, Booking

admin.site.register(Resource)  # Ajoute le formulaire de gestion des ressources dans le backoffice
admin.site.register(Booking)  # Ajoute le formulaire de gestion des réservations dans le backoffice
