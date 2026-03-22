from django.urls import path
from Guest import views
app_name="Guest"

urlpatterns = [
    path('', views.index, name="index"),
    path('Login/', views.Login, name="Login"),
  path('forgot-password/', views.forgotpassword, name="forgotpassword"),
path('verify-otp/', views.otp, name="otp"),
path('reset-password/', views.newpass, name="newpass"),
]