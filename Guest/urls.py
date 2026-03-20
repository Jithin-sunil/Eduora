from django.urls import path
from Guest import views
app_name="Guest"

urlpatterns = [
    path('', views.index, name="index"),
    path('Login/', views.Login, name="Login"),
    path('ForgotPassword/', views.forgot_password, name="forgot_password"),
    path('VerifyOTP/', views.verify_otp, name="verify_otp"),
    path('ResetPassword/', views.reset_password, name="reset_password"),
]