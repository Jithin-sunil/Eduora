from django.shortcuts import render, redirect
from Guest.models import *
from Admin.models import *
from Teacher.models import *
import random, datetime
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.

def index(request):
    return render(request,"Guest/index.html")

def Login(request):
    if request.method == "POST":
    
        email=request.POST.get("txt_mail")
        password=request.POST.get("txt_password")

        admincount = tbl_admin.objects.filter(admin_email=email,admin_password=password).count()
        teachercount = tbl_teacher.objects.filter(teacher_email=email,teacher_password=password).count()
        studentcount = tbl_student.objects.filter(student_email=email,student_password=password).count()
        if admincount > 0:
            admin=tbl_admin.objects.get(admin_email=email,admin_password=password)
            request.session['aid'] = admin.id
            return redirect("Admin:Homepage")
        elif teachercount > 0:
            teacher=tbl_teacher.objects.get(teacher_email=email,teacher_password=password)
            request.session['tid'] = teacher.id
            return redirect("Teacher:Homepage")
        elif studentcount > 0:
            student=tbl_student.objects.get(student_email=email,student_password=password)
            request.session['sid'] = student.id
            return redirect("Student:Homepage")
        else:
            return render(request,"Guest/Login.html",{"msg":"Invalid Email or Password"})
    else:
        return render(request,"Guest/Login.html")


# ── Forgot Password – Step 1: Enter Email ─────────────────────────────────────
def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("txt_email", "").strip()

        # Check the email exists in any user table
        is_admin   = tbl_admin.objects.filter(admin_email=email).exists()
        is_teacher = tbl_teacher.objects.filter(teacher_email=email).exists()
        is_student = tbl_student.objects.filter(student_email=email).exists()

        if not (is_admin or is_teacher or is_student):
            return render(request, "Guest/ForgotPassword.html", {"msg": "No account found with that email."})

        # Generate OTP
        otp_code = str(random.randint(100000, 999999))
        tbl_otp.objects.create(otp_email=email, otp_code=otp_code)

        # Send OTP Email
        try:
            send_mail(
                subject="🔐 EduSphere – Password Reset OTP",
                message=(
                    f"Your OTP for password reset is: {otp_code}\n\n"
                    "This OTP is valid for 10 minutes. Do not share it with anyone.\n\n"
                    "If you did not request this, please ignore this email.\n\n"
                    "— EduSphere College Portal"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
        except Exception as e:
            return render(request, "Guest/ForgotPassword.html", {"msg": f"Failed to send OTP: {str(e)}"})

        request.session['reset_email'] = email
        return redirect("Guest:verify_otp")
    return render(request, "Guest/ForgotPassword.html")


# ── Forgot Password – Step 2: Verify OTP ──────────────────────────────────────
def verify_otp(request):
    email = request.session.get('reset_email')
    if not email:
        return redirect("Guest:forgot_password")

    if request.method == "POST":
        entered_otp = request.POST.get("txt_otp", "").strip()

        # Get the latest unused OTP for this email (within 10 mins)
        cutoff = datetime.datetime.now() - datetime.timedelta(minutes=10)
        otp_record = tbl_otp.objects.filter(
            otp_email=email,
            otp_status=0,
            otp_time__gte=cutoff
        ).order_by('-id').first()

        if not otp_record:
            return render(request, "Guest/VerifyOTP.html", {"msg": "OTP expired. Please request a new one.", "email": email})

        if otp_record.otp_code == entered_otp:
            otp_record.otp_status = 1
            otp_record.save()
            return redirect("Guest:reset_password")
        else:
            return render(request, "Guest/VerifyOTP.html", {"msg": "Incorrect OTP. Try again.", "email": email})

    return render(request, "Guest/VerifyOTP.html", {"email": email})


# ── Forgot Password – Step 3: Set New Password ────────────────────────────────
def reset_password(request):
    email = request.session.get('reset_email')
    if not email:
        return redirect("Guest:forgot_password")

    if request.method == "POST":
        new_pass   = request.POST.get("txt_newpassword")
        conf_pass  = request.POST.get("txt_confirmpassword")

        if new_pass != conf_pass:
            return render(request, "Guest/ResetPassword.html", {"msg": "Passwords do not match."})

        # Update whichever account this email belongs to
        tbl_admin.objects.filter(admin_email=email).update(admin_password=new_pass)
        tbl_teacher.objects.filter(teacher_email=email).update(teacher_password=new_pass)
        tbl_student.objects.filter(student_email=email).update(student_password=new_pass)

        # Clean session
        if 'reset_email' in request.session:
            del request.session['reset_email']

        return render(request, "Guest/Login.html", {"msg": "Password reset successful! Please login."})

    return render(request, "Guest/ResetPassword.html")
