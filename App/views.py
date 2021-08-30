import json
import pika
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView

from .forms import BookingForm, LoginForm
from .models import Booking, Resource

TIME_FORMAT = '%d-%m-%Y %H:%M'
AMQP_QUEUE_NAME = 'booking'


class CustomLoginView(LoginView):
    form_class = LoginForm


def login_view(request):
    login(request)
    if request.user.is_authenticated:
        return redirect('/')


@login_required
def reservations_list(request):
    user = request.user
    reservations = Booking.objects.filter(user=user)
    context = {'reservations': reservations}
    return render(request, "index.html", context)


@login_required
def create_reservation(request):
    return render(request, "create_reservation.html", {'form': BookingForm})


def reservation_ajax(request):
    if request.is_ajax():
        title = request.POST.get('title', None)
        start_date = request.POST.get('start_date', None)
        end_date = request.POST.get('end_date', None)
        resource = request.POST.get('resource', None)
        user = request.user

        if start_date:
            start_date_converted = datetime.strptime(start_date, TIME_FORMAT)
        else:
            return JsonResponse({
                'msg': 'La date de début doit être définie !'
            })

        if end_date:
            end_date_converted = datetime.strptime(end_date, TIME_FORMAT)
        else:
            return JsonResponse({
                'msg': 'La date de fin doit être définie !'
            })

        if start_date_converted <= datetime.now():
            return JsonResponse({
                'msg': 'La date de début doit être postérieur à la date courante.'
            })

        if start_date_converted >= end_date_converted:
            return JsonResponse({
                'msg': 'La date de début doit être antérieure à la date de fin.'
            })

        if title and resource:
            resource = Resource.objects.get(id=resource)
            booking = Booking(title=title, start_date=start_date_converted.strftime('%Y-%m-%d %H:%M'),
                              end_date=end_date_converted.strftime('%Y-%m-%d %H:%M'), resource=resource, user=user)
            booking.save()
            
            publish_amqp_message(json.dumps({
                'object_type': 'booking',
                'action': 'create',
                'object_id': booking.id,
            }))
            
            return JsonResponse({
                'msg': 'Le formulaire a été soumis avec succès : ' + title + ' - ' + start_date + ' - ' + end_date
                       + ' - ' + str(resource)
            })
        else:
            return JsonResponse({
                'msg': 'Veuillez saisir un titre et sélectionner une ressource.'
            })


@login_required
def edit_reservation(request, pk):
    reservation = Booking.objects.get(id=pk)
    reservation.start_date = reservation.start_date.strftime(TIME_FORMAT)
    reservation.end_date = reservation.end_date.strftime(TIME_FORMAT)
    form = BookingForm(instance=reservation)
    context = {'form': form, 'reservation_id': reservation.id}
    return render(request, 'edit_reservation.html', context)


def edit_reservation_ajax(request):
    if request.is_ajax():
        title = request.POST.get('title', None)
        start_date = request.POST.get('start_date', None)
        end_date = request.POST.get('end_date', None)
        resource = request.POST.get('resource', None)
        user = request.user
        reservation_id = request.POST.get('id')

        if start_date:
            start_date_converted = datetime.strptime(start_date, TIME_FORMAT)
        else:
            return JsonResponse({
                'msg': 'La date de début doit être définie !'
            })

        if end_date:
            end_date_converted = datetime.strptime(end_date, TIME_FORMAT)
        else:
            return JsonResponse({
                'msg': 'La date de fin doit être définie !'
            })

        if start_date_converted <= datetime.now():
            return JsonResponse({
                'msg': 'La date de début doit être postérieur à la date courante.'
            })

        if start_date_converted >= end_date_converted:
            return JsonResponse({
                'msg': 'La date de début doit être antérieure à la date de fin.'
            })

        if title and resource:
            resource = Resource.objects.get(id=resource)

            booking = Booking(title=title, start_date=start_date_converted,
                              end_date=end_date_converted, resource=resource, user=user,
                              id=reservation_id)
            booking.save()

            publish_amqp_message(json.dumps({
                'object_type': 'booking',
                'action': 'edit',
                'object_id': booking.id,
            }))

            return JsonResponse({
                'msg': 'Le formulaire a été édité avec succès !'
            })
        else:
            return JsonResponse({
                'msg': 'Veuillez saisir un titre et sélectionner une ressource.'
            })


def delete_reservation(request, pk):
    reservation = Booking.objects.get(id=pk)

    # if reservation.start_date > datetime.now().datetime:

    if reservation.start_date:
        start_date_converted = datetime.strptime(str(reservation.start_date), '%Y-%m-%d %H:%M:%S')
        if start_date_converted > datetime.now():
            publish_amqp_message(json.dumps({
                'object_type': 'booking',
                'action': 'delete',
                'object_id': reservation.id,
            }))
            reservation.delete()
    return redirect('/')


def publish_amqp_message(payload):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue=AMQP_QUEUE_NAME)

    channel.basic_publish(exchange='',
                          routing_key=AMQP_QUEUE_NAME,
                          body=payload)
    connection.close()
