from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    #path("appointment", views.appointment, name="appointment"),
    path('booking', views.booking, name='booking'),
    path('booking-submit', views.bookingSubmit, name='bookingSubmit'),
    path('user-panel', views.userPanel, name='userPanel'),
    path("login", views.login_view, name="login"),
    #path('logout/',views.logoutUser,name="logout"),
]
