from django.shortcuts import render,redirect
from Admin.models import *
from django.http import JsonResponse
from Student.models import *
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.

def Logout(request):
    del request.session['aid']
    return redirect('Guest:Login')

def AdminReg(request):
    admindata=tbl_admin.objects.all()
    if request.method=="POST":
        name=request.POST.get("txt_name")
        email=request.POST.get("txt_mail")
        password=request.POST.get("txt_password")
        tbl_admin.objects.create(admin_name=name,admin_email=email,admin_password=password)
        return render(request,"Admin/AdminRegistration.html",{'msg':"Data Inserted..."})    
    else: 
        return render(request,"Admin/AdminRegistration.html",{'admindata':admindata})

def deladmin(request,did):
    tbl_admin.objects.get(id=did).delete()
    return render(request,"Admin/AdminRegistration.html",{'msg':"Data Deleted"})

def editadmin(request,eid):
    editdata=tbl_admin.objects.get(id=eid)
    admindata=tbl_admin.objects.all()
    if request.method == "POST":
        name=request.POST.get("txt_name")
        editdata.admin_name=name
        email=request.POST.get("txt_mail")
        editdata.admin_email=email
        password=request.POST.get("txt_password")
        editdata.admin_password=password
        editdata.save()
        return render(request,"Admin/AdminRegistration.html",{'msg':"Data Updated..."})
    else:
        return render(request,"Admin/AdminRegistration.html",{'editdata':editdata,'admindata':admindata})


def Department(request):
    if "aid" not in request.session:    
        return redirect("Guest:Login")
    else:
        departmentdata = tbl_department.objects.all()
        if request.method=="POST":
            department=request.POST.get("txt_department")
            departmentcount = tbl_department.objects.filter(department_name__iexact=department).count()
            if departmentcount > 0:
                return render(request,"Admin/Department.html",{'msg':"Department Already Exists...",'departmentdata':departmentdata})
            else:
                tbl_department.objects.create(department_name=department)
            return render(request,"Admin/Department.html",{'msg':"Data Inserted..."})
        else:
            return render(request,"Admin/Department.html",{'departmentdata':departmentdata})

def deldepartment(request,did):
    tbl_department.objects.get(id=did).delete()
    return render(request,"Admin/Department.html",{'msg':"Data Deleted..."})  

def Semester(request):
    if "aid" not in request.session:    
        return redirect("Guest:Login")
    else:
        semesterdata=tbl_semester.objects.all()
        if request.method=="POST":
            semester=request.POST.get("txt_semester")
            semestercount = tbl_semester.objects.filter(semester_name__iexact=semester).count()
            if semestercount > 0:
                return render(request,"Admin/Semester.html",{'msg':"Semester Already Exists...",'semesterdata':semesterdata})
            else:
                tbl_semester.objects.create(semester_name=semester)
            return render(request,"Admin/Semester.html",{'msg':"Data Inserted..."})
        else:
            return render(request,"Admin/Semester.html",{'semesterdata':semesterdata})

def delsemester(request,did):
    tbl_semester.objects.get(id=did).delete()
    return render(request,"Admin/Semester.html",{'msg':"Data Deleted..."})

def Academicyear(request):
    if "aid" not in request.session:    
        return redirect("Guest:Login")
    else:
        academicyeardata=tbl_academicyear.objects.all()
        if request.method=="POST":
            year=request.POST.get("txt_academicyear")
            academicyearcount = tbl_academicyear.objects.filter(academicyear_name__iexact=year).count()
            if academicyearcount > 0:
                return render(request,"Admin/Academicyear.html",{'msg':"Academic Year Already Exists...",'academicyeardata':academicyeardata})
            else:
                tbl_academicyear.objects.create(academicyear_name=year)
            return render(request,"Admin/Academicyear.html",{'msg':"Data Inserted..."})
        else:
            return render(request,"Admin/Academicyear.html",{'academicyeardata':academicyeardata})

def delacademicyear(request,did):
    tbl_academicyear.objects.get(id=did).delete()
    return render(request,"Admin/Academicyear.html",{'msg':"Data Deleted..."})

def Course(request):
    if "aid" not in request.session:    
        return redirect("Guest:Login")
    else:
        coursedata=tbl_course.objects.all()
        departmentdata=tbl_department.objects.all()
        if request.method=="POST":
            course=request.POST.get("txt_course")
            department=tbl_department.objects.get(id=request.POST.get("sel_department"))
            coursecount = tbl_course.objects.filter(course_name__iexact=course).count()
            if coursecount > 0:
                return render(request,"Admin/Course.html",{'msg':"Course Already Exists...",'departmentdata':departmentdata,'coursedata':coursedata})
            else:
                tbl_course.objects.create(course_name=course,department=department)
            return render(request,"Admin/Course.html",{'msg':"Data Inserted..."})
        else:
            return render(request,"Admin/Course.html",{'departmentdata':departmentdata,'coursedata':coursedata})

def delcourse(request,did):
    tbl_course.objects.get(id=did).delete()
    return render(request,"Admin/Course.html",{'msg':"Data Deleted..."})

def Subject(request):
    if "aid" not in request.session:    
        return redirect("Guest:Login")
    else:
        subjectdata=tbl_subject.objects.all()
        departmentdata=tbl_department.objects.all()
        semesterdata=tbl_semester.objects.all()
        if request.method=="POST":
            subject=request.POST.get("txt_subject")
            course=tbl_course.objects.get(id=request.POST.get("sel_course"))
            semester=tbl_semester.objects.get(id=request.POST.get("sel_semester"))
            subjectcount = tbl_subject.objects.filter(subject_name__iexact=subject).count()
            if subjectcount > 0:
                return render(request,"Admin/Subject.html",{'msg':"Subject Already Exists...",'departmentdata':departmentdata,'semesterdata':semesterdata,'subjectdata':subjectdata})
            else:
                tbl_subject.objects.create(subject_name=subject,course=course,semester=semester)
            return render(request,"Admin/Subject.html",{'msg':"Data Inserted..."})
        else:
            return render(request,"Admin/Subject.html",{'departmentdata':departmentdata,'semesterdata':semesterdata,'subjectdata':subjectdata})

def delsubject(request,did):
    tbl_subject.objects.get(id=did).delete()
    return render(request,"Admin/Subject.html",{'msg':"Data Deleted..."})

def Class(request):
    if "aid" not in request.session:    
        return redirect("Guest:Login")
    else:
        departmentdata=tbl_department.objects.all()
        classdata=tbl_class.objects.all()
        if request.method=="POST":
            name=request.POST.get("txt_class")
            course=tbl_course.objects.get(id=request.POST.get("sel_course"))
            classcount = tbl_class.objects.filter(class_name__iexact=name).count()
            if classcount > 0:
                return render(request,"Admin/Class.html",{'msg':"Class Already Exists...",'departmentdata':departmentdata,'classdata':classdata})
            else:
                tbl_class.objects.create(class_name=name,course=course)
            return render(request,"Admin/Class.html",{'msg':"Data Inserted..."})
        else:
            return render(request,"Admin/Class.html",{'departmentdata':departmentdata,'classdata':classdata})

def delclass(request,did):
    tbl_class.objects.get(id=did).delete()
    return render(request,"Admin/Class.html",{'msg':"Data Deleted..."})


def Addteacher(request):
    if "aid" not in request.session:    
        return redirect("Guest:Login")
    else:
        departmentdata=tbl_department.objects.all()
        teacherdata=tbl_teacher.objects.all()
        if request.method=="POST":
            name=request.POST.get("txt_name")
            email=request.POST.get("txt_email")
            contact=request.POST.get("txt_contact")
            role=request.POST.get("txt_role")
            gender=request.POST.get("txt_gender")
            photo= request.FILES.get("file_photo")
            password=request.POST.get("txt_password")
            department=tbl_department.objects.get(id=request.POST.get("sel_department"))
            teachercount = tbl_teacher.objects.filter(teacher_email__iexact=email).count()
            if teachercount > 0:
                return render(request,"Admin/Addteacher.html",{'msg':"Email Already Exists...",'departmentdata': departmentdata,'teacherdata':teacherdata})
            else:
                tbl_teacher.objects.create(teacher_name=name,teacher_email=email,teacher_contact=contact,teacher_role=role,
            teacher_gender=gender,teacher_photo=photo,teacher_password=password,department=department)
            # Send welcome email with login credentials
            try:
                send_mail(
                    subject="🎓 Welcome to EduSphere – Your Faculty Account",
                    message=(
                        f"Dear {name},\n\n"
                        f"Welcome to EduSphere College Portal! Your faculty account has been created successfully.\n\n"
                        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                        f"  YOUR LOGIN CREDENTIALS\n"
                        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                        f"  Portal URL : http://localhost:8000/Guest/Login/\n"
                        f"  Email      : {email}\n"
                        f"  Password   : {password}\n"
                        f"  Role       : {role}\n"
                        f"  Department : {department.department_name}\n"
                        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                        f"Please login and change your password immediately for security.\n\n"
                        f"Best Regards,\nEduSphere Administration"
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=True,
                )
            except Exception:
                pass
            return render(request,"Admin/Addteacher.html",{'msg':"Data Inserted & Credentials Emailed!"})
        else:
            return render(request,"Admin/Addteacher.html",{'departmentdata': departmentdata,'teacherdata':teacherdata})

def Assignclass(request,id):
    departmentdata=tbl_department.objects.all()
    academicyeardata=tbl_academicyear.objects.all()
    teacherid=tbl_teacher.objects.get(id=id)
    assignclassdata=tbl_assignclass.objects.filter(teacher=teacherid)
    if request.method=="POST":
        Class=tbl_class.objects.get(id=request.POST.get("sel_class"))
        year=tbl_academicyear.objects.get(id=request.POST.get("sel_academicyear"))
        tbl_assignclass.objects.create(Class=Class,academicyear=year,teacher=teacherid)
        assignclassdata=tbl_assignclass.objects.filter(teacher=teacherid)
        return render(request,"Admin/Assignclass.html",{'msg':"Data Inserted...",'departmentdata':departmentdata,'academicyeardata':academicyeardata,
        'assignclassdata':assignclassdata})
    else:
        return render(request,"Admin/Assignclass.html",{'departmentdata':departmentdata,'academicyeardata':academicyeardata,
        'assignclassdata':assignclassdata})

def Assignsubject(request,id):
    departmentdata=tbl_department.objects.all()
    academicyeardata=tbl_academicyear.objects.all()
    semesterdata=tbl_semester.objects.all()
    teacherid=tbl_teacher.objects.get(id=id)
    assignsubjectdata=tbl_assignsubject.objects.filter(teacher=teacherid)
    if request.method=="POST":
        year=tbl_academicyear.objects.get(id=request.POST.get("sel_academicyear"))
        subjectid=tbl_subject.objects.get(id=request.POST.get("sel_subject"))
        tbl_assignsubject.objects.create(academicyear=year,teacher=teacherid,subject=subjectid)
        assignsubjectdata=tbl_assignsubject.objects.filter(teacher=teacherid)
        return render(request,"Admin/Assignsubject.html",{'msg':"Data Inserted...",'departmentdata':departmentdata,'academicyeardata':academicyeardata,
        'semesterdata':semesterdata,'assignsubjectdata':assignsubjectdata})
    else:
        return render(request,"Admin/Assignsubject.html",{'departmentdata':departmentdata,'academicyeardata':academicyeardata,
        'semesterdata':semesterdata,'assignsubjectdata':assignsubjectdata})
    
def delassignclass(request,did):
    data = tbl_assignclass.objects.get(id=did)
    tid = data.teacher.id
    data.delete()
    return redirect("Admin:Assignclass",id=tid)

def classsem(request,did):
    assignclassdata=tbl_assignclass.objects.get(id=did)
    semesterdata=tbl_semester.objects.all()
    classsemdata=tbl_classsem.objects.filter(assignclass=assignclassdata)
    if request.method=="POST":
        semester=tbl_semester.objects.get(id=request.POST.get("sel_semester"))
        tbl_classsem.objects.create(semester=semester,assignclass=assignclassdata)
        semesterdata=tbl_semester.objects.all()
        classsemdata=tbl_classsem.objects.filter(assignclass=assignclassdata)
        return render(request,"Admin/Classsem.html",{'msg':"Data Inserted...",'semesterdata':semesterdata,'classsemdata':classsemdata})
    else:
        return render(request,"Admin/Classsem.html",{'semesterdata':semesterdata,'classsemdata':classsemdata})
    
def delclasssem(request,did):
    tbl_classsem.objects.get(id=did).delete()
    return render(request,"Admin/Classsem.html",{'msg':"Data Deleted..."})




def Homepage(request):
    if "aid" not in request.session:
        return redirect("Guest:Login")
    
    # Statistics
    dept_count = tbl_department.objects.count()
    teacher_count = tbl_teacher.objects.count()
    student_count = tbl_student.objects.count()
    subject_count = tbl_subject.objects.count()
    
    # Pending Actions
    pending_leaves = tbl_teacherleave.objects.filter(leave_status=0).order_by('-id')[:5]
    pending_complaints = tbl_complaint.objects.filter(com_status=0).order_by('-id')[:5]
    
    leave_count = tbl_teacherleave.objects.filter(leave_status=0).count()
    complaint_count = tbl_complaint.objects.filter(com_status=0).count()

    return render(request, "Admin/Homepage.html", {
        'dept_count': dept_count,
        'teacher_count': teacher_count,
        'student_count': student_count,
        'subject_count': subject_count,
        'pending_leaves': pending_leaves,
        'pending_complaints': pending_complaints,
        'leave_count': leave_count,
        'complaint_count': complaint_count,
    })

def Ajaxcourse(request):
    dep=tbl_department.objects.get(id=request.GET.get('disid'))
    course=tbl_course.objects.filter(department=dep)
    return render(request,'Admin/AjaxCourse.html',{'cs':course})

def Ajaxclass(request):
    course=tbl_course.objects.get(id=request.GET.get('clsid'))
    Class=tbl_class.objects.filter(course=course)
    return render(request,'Admin/AjaxClass.html',{'cls':Class})

def Ajaxsubject(request):
    sem=tbl_semester.objects.get(id=request.GET.get('subid'))
    course=tbl_course.objects.get(id=request.GET.get('coid'))
    sub=tbl_subject.objects.filter(semester=sem,course=course)
    print(sub)
    return render(request,'Admin/AjaxSubject.html',{'sub':sub})



DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

HOURS = [
    ("1", "10:00 - 10:55"),
    ("2", "10:55 - 11:50"),
    ("3", "12:05 - 01:00"),
    ("4", "02:00 - 3:00"),
    ("5", "03:00 - 04:00"),
    
]


def timetable(request):
    department =  tbl_department.objects.all()
    courses = tbl_course.objects.all()
    semesters = tbl_semester.objects.all()

    course_id = request.GET.get("course")
    semester_id = request.GET.get("semester")

    subjects = tbl_subject.objects.none()
    timetable_data = tbl_timetable.objects.none()

    if course_id and semester_id:
        subjects = tbl_subject.objects.filter(
            course_id=course_id,
            semester_id=semester_id
        )
        timetable_data = tbl_timetable.objects.filter(
            course_id=course_id,
            semester_id=semester_id
        )

    return render(request, "Admin/Timetable.html", {
        "departmentdata":department,
        "courses": courses,
        "semesters": semesters,
        "subjects": subjects,
        "timetable": timetable_data,
        "days": DAYS,
        "hours": HOURS,
        "course_id": course_id,
        "semester_id": semester_id
    })

def save_timetable(request):
    academicyear = tbl_academicyear.objects.order_by('-id').first()
    tbl_timetable.objects.update_or_create(
        course_id=request.GET["course"],
        semester_id=request.GET["semester"],
        day=request.GET["day"],
        hour=request.GET["hour"],
        academicyear= academicyear,
        defaults={
            "subject_id": request.GET["subject"],
            "teacher_id": tbl_assignsubject.objects.get(
                subject_id=request.GET["subject"]
            ).teacher
        }
    )
    return JsonResponse({"status": "success"})

def admin_view_timetable(request):
    departmentdata = tbl_department.objects.all()
    semesters = tbl_semester.objects.all()
    courses = tbl_course.objects.all()

    course_id = request.GET.get("course")
    semester_id = request.GET.get("semester")
    edit = request.GET.get("edit")  # Edit mode flag

    academicyear = tbl_academicyear.objects.order_by('-id').first()

    timetable = tbl_timetable.objects.none()
    subjects = tbl_subject.objects.none()

    if course_id and semester_id and academicyear:
        timetable = tbl_timetable.objects.filter(
            course_id=course_id,
            semester_id=semester_id,
            academicyear=academicyear
        )

        subjects = tbl_subject.objects.filter(
            course_id=course_id,
            semester_id=semester_id
        )

    return render(request, "Admin/ViewTimeTable.html", {
        "departmentdata": departmentdata,
        "semesters": semesters,
        "courses": courses,
        "timetable": timetable,
        "subjects": subjects,
        "days": DAYS,
        "hours": HOURS,
        "course_id": course_id,
        "semester_id": semester_id,
        "academicyear": academicyear,
        "edit": edit
    })

def  Viewcomplaint(request):
    complaintdata=tbl_complaint.objects.all()
    return render(request,"Admin/Viewcomplaint.html",{'complaintdata':complaintdata})

def Replycomplaint(request,did):
    complaintdata=tbl_complaint.objects.get(id=did)
    if request.method=="POST":
        reply=request.POST.get("txt_reply")
        complaintdata.com_reply=reply
        complaintdata.com_status=1
        complaintdata.save()
        return render(request,"Admin/Viewcomplaint.html",{'msg':"Replied Successfully..."})
    else:
        return render(request,"Admin/Replycomplaint.html",{'complaintdata':complaintdata})
    
def Purpose(request):
    purposedata = tbl_purpose.objects.all()
    if request.method=="POST":
        purpose=request.POST.get("txt_purpose")
        purposecount = tbl_purpose.objects.filter(purpose_name__iexact=purpose).count()
        if purposecount > 0:
            return render(request,"Admin/Purpose.html",{'msg':"Purpose Already Exists...",'purposedata':purposedata})
        else:
            tbl_purpose.objects.create(purpose_name=purpose)
            return render(request,"Admin/Purpose.html",{'msg':"Data Inserted..."})
    else:
        return render(request,"Admin/Purpose.html",{'purposedata':purposedata})
    
def delpurpose(request,did):
    tbl_purpose.objects.get(id=did).delete()
    return render(request,"Admin/Purpose.html",{'msg':"Data Deleted..."})

def Assignincharge(request,id):
    purposedata=tbl_purpose.objects.all()
    teacherid=tbl_teacher.objects.get(id=id)
    if request.method=="POST":
        purposeid=tbl_purpose.objects.get(id=request.POST.get("sel_purpose"))
        tbl_incharge.objects.create(teacher=teacherid,purpose=purposeid)
        return redirect("Admin:Addteacher")
    else:
        return render(request,"Admin/Assignincharge.html",{'purposedata':purposedata})

def Notification(request):
    notifications = tbl_notification.objects.all().order_by('-id')
    if request.method == "POST":
        title = request.POST.get("txt_title")
        content = request.POST.get("txt_content")
        tbl_notification.objects.create(notification_title=title, notification_content=content)
        return render(request, "Admin/Notification.html", {'msg': "Notification Posted", 'notifications': notifications})
    return render(request, "Admin/Notification.html", {'notifications': notifications})

def delnotification(request, did):
    tbl_notification.objects.get(id=did).delete()
    return redirect("Admin:Notification")

def AdminViewTeacherLeave(request):
    leavedata = tbl_teacherleave.objects.all().order_by('-id')
    return render(request, "Admin/ViewTeacherLeave.html", {'leavedata': leavedata})

def AcceptTeacherLeave(request, aid):
    leave = tbl_teacherleave.objects.get(id=aid)
    leave.leave_status = 1
    leave.save()
    return redirect("Admin:AdminViewTeacherLeave")

def RejectTeacherLeave(request, rid):
    leave = tbl_teacherleave.objects.get(id=rid)
    leave.leave_status = 2
    leave.save()
    return redirect("Admin:AdminViewTeacherLeave")

def SpecialTimetable(request):
    classes = tbl_assignclass.objects.all()
    teachers = tbl_teacher.objects.all()
    subjects = tbl_subject.objects.all()
    special_timetable = tbl_specialtimetable.objects.all().order_by('-date')

    if request.method == "POST":
        date = request.POST.get("txt_date")
        hour = request.POST.get("sel_hour")
        teacher = tbl_teacher.objects.get(id=request.POST.get("sel_teacher"))
        subject = tbl_subject.objects.get(id=request.POST.get("sel_subject"))
        assignclass = tbl_assignclass.objects.get(id=request.POST.get("sel_class"))
        
        tbl_specialtimetable.objects.create(
            date=date, hour=hour, teacher=teacher, subject=subject, assignclass=assignclass
        )
        return render(request, "Admin/SpecialTimetable.html", {
            'msg': "Special Timetable set",
            'classes': classes, 'teachers': teachers, 'subjects': subjects, 'special_timetable': special_timetable, 'hours': HOURS
        })
    
    return render(request, "Admin/SpecialTimetable.html", {
        'classes': classes, 'teachers': teachers, 'subjects': subjects, 'special_timetable': special_timetable, 'hours': HOURS
    })

def delspecialtimetable(request, did):
    tbl_specialtimetable.objects.get(id=did).delete()
    return redirect("Admin:SpecialTimetable")
    
