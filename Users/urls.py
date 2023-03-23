from django.urls import path
from django.contrib.auth import views as auth_views
from.import views
from.views import CompletePasswordReset,RequestPasswordReset
urlpatterns = [
   path('request-password-reset-link',RequestPasswordReset.as_view(),name="request-password"),
   path('set-new-password/<uidb64>/<token>',CompletePasswordReset.as_view(), name='reset-user-password'),
   path("register", views.register_user, name="register"),
   path('logout_user', views.logout_user, name='logout'),
   ]