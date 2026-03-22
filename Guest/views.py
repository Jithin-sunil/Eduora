from django.shortcuts import render, redirect
from Guest.models import *
from Admin.models import *
from Teacher.models import *
import random, datetime
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


# Create your views here.

def index(request):
    return render(request,"Guest/index.html")

def Login(request):
    if request.method == "POST":
    
        email=request.POST.get("txt_mail").strip()
        password=request.POST.get("txt_password")

        admincount = tbl_admin.objects.filter(admin_email__iexact=email,admin_password=password).count()
        teachercount = tbl_teacher.objects.filter(teacher_email__iexact=email,teacher_password=password).count()
        studentcount = tbl_student.objects.filter(student_email__iexact=email,student_password=password).count()
        if admincount > 0:
            admin=tbl_admin.objects.get(admin_email__iexact=email,admin_password=password)
            request.session['aid'] = admin.id
            return redirect("Admin:Homepage")
        elif teachercount > 0:
            teacher=tbl_teacher.objects.get(teacher_email__iexact=email,teacher_password=password)
            request.session['tid'] = teacher.id
            return redirect("Teacher:Homepage")
        elif studentcount > 0:
            student=tbl_student.objects.get(student_email__iexact=email,student_password=password)
            request.session['sid'] = student.id
            return redirect("Student:Homepage")
        else:
            return render(request,"Guest/Login.html",{"msg":"Invalid Email or Password"})
    else:
        return render(request,"Guest/Login.html")

def forgotpassword(request):
    if request.method == "POST":
        email = request.POST.get("txt_email")

        user_id = None
        role = None

        # Check Admin
        try:
            admin = tbl_admin.objects.get(admin_email=email)
            user_id = admin.id
            role = "admin"
        except tbl_admin.DoesNotExist:
            pass

        # Check Teacher
        if not role:
            try:
                teacher = tbl_teacher.objects.get(teacher_email=email)
                user_id = teacher.id
                role = "teacher"
            except tbl_teacher.DoesNotExist:
                pass

        # Check Student
        if not role:
            try:
                student = tbl_student.objects.get(student_email=email)
                user_id = student.id
                role = "student"
            except tbl_student.DoesNotExist:
                pass

        if not role:
            return render(request, "Guest/ForgotPassword.html", {"msg": "Email not found"})

        # Generate OTP
        otp = random.randint(111111, 999999)

        # Store in session
        request.session["otp"] = otp
        request.session["uid"] = user_id
        request.session["role"] = role

        # Send Mail
        send_mail(
            'Password Reset OTP',
            f"Your OTP is {otp}",
            settings.EMAIL_HOST_USER,
            [email],
        )

        return redirect("Guest:otp")

    return render(request, "Guest/ForgotPassword.html")

def otp(request):
    if request.method == "POST":
        inp_otp = request.POST.get("txt_otp")

        if "otp" not in request.session:
            return redirect("Guest:forgotpassword")

        if inp_otp == str(request.session["otp"]):
            return redirect("Guest:newpass")
        else:
            return render(request, "Guest/OTP.html", {"msg": "OTP does not match!"})

    return render(request, "Guest/OTP.html")



def newpass(request):
    if request.method == "POST":

        if "uid" not in request.session or "role" not in request.session:
            return redirect("Guest:forgotpassword")

        uid = request.session["uid"]
        role = request.session["role"]

        new_pass = request.POST.get("txt_newpassword")
        con_pass = request.POST.get("txt_confirmpassword")

        if new_pass != con_pass:
            return render(request, "Guest/NewPassword.html", {
                "msg": "Passwords do not match!"
            })

        # Update based on role
        if role == "admin":
            user = tbl_admin.objects.get(id=uid)
            user.admin_password = new_pass
            user.save()

        elif role == "teacher":
            user = tbl_teacher.objects.get(id=uid)
            user.teacher_password = new_pass
            user.save()

        elif role == "student":
            user = tbl_student.objects.get(id=uid)
            user.student_password = new_pass
            user.save()

        # Clear session
        request.session.flush()

        return render(request, "Guest/Login.html", {
            "msg": "Password updated successfully! Please login."
        })

    return render(request, "Guest/NewPassword.html")