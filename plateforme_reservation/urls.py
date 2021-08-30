"""plateforme_reservation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from App import views

urlpatterns = [
    path('', views.reservations_list, name='reservations_list'),
    path('create_reservation/', views.create_reservation, name='create_reservation'),
    path('reservation_ajax/', views.reservation_ajax, name='reservation_ajax'),
    path('delete_reservation/<str:pk>/', views.delete_reservation, name="delete_reservation"),
    path('edit_reservation/<str:pk>/', views.edit_reservation, name="edit_reservation"),
    path('edit_reservation_ajax/', views.edit_reservation_ajax, name="edit_reservation_ajax"),
    # path('edit_reservation_ajax/<str:pk>/', views.edit_reservation_ajax, name="edit_reservation_ajax"),
    path('login/', views.CustomLoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
