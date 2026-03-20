from django.shortcuts import render,redirect
from Admin.models import *
from Teacher.models import *
from Student.models import *
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
def Homepage(request):
    sc=tbl_student.objects.filter(assignclass__teacher=request.session['tid']).count()
    ac=tbl_assignment.objects.filter(teacher=request.session['tid']).count()
    lc=tbl_leave.objects.filter(student__assignclass__teacher=request.session['tid'],leave_status=0).count()
    asup=tbl_assignmentbody.objects.filter(assignment__teacher=request.session['tid']).count()
    std=tbl_student.objects.filter(assignclass__teacher=request.session['tid'])
    data = []

    for i in std:
        total = tbl_attendance.objects.filter(student=i).count()
        present = tbl_attendance.objects.filter(student=i, status=1).count()

        if total > 0:
            percentage = (present / total) * 100
        else:
            percentage = 0

        data.append({
            'student': i,
            'percentage': round(percentage, 2)
        })
    teacher = tbl_teacher.objects.get(id=request.session['tid'])
    assign=tbl_assignment.objects.filter(teacher=teacher).order_by('-id')[:5]
    notifications = tbl_notification.objects.all().order_by('-id')[:5]
    return render(request,"Teacher/Homepage.html",{'student_count':sc,'assignment_count':ac,'leave_count':lc,'assignment_submission_count':asup,'data':data,'teacher':teacher,'assign':assign, 'notifications': notifications})


def Myprofile(request):
  teacherdata = tbl_teacher.objects.get(id=request.session['tid'])
  assignclass = tbl_assignclass.objects.filter(teacher=teacherdata).first()
  incharge = tbl_incharge.objects.filter(teacher=teacherdata)
  return render(request,"Teacher/Myprofile.html",{'teacher':teacherdata, 'assignclass': assignclass, 'incharge': incharge})

def Editprofile(request):
  teacherdata = tbl_teacher.objects.get(id=request.session['tid'])
  if request.method == "POST":
    name=request.POST.get("txt_name")
    email=request.POST.get("txt_email")
    contact=request.POST.get("txt_contact")

    teacherdata.teacher_name = name
    teacherdata.teacher_email= email
    teacherdata.teacher_contact= contact
    teacherdata.save()
    return render(request,"Teacher/Editprofile.html",{'msg':"Data Updated..."})
  else:
    return render(request,"Teacher/Editprofile.html",{'teacher':teacherdata})

def Changepass(request):
  teacherdata = tbl_teacher.objects.get(id=request.session['tid'])
  dbpass=teacherdata.teacher_password
  if request.method == "POST":
    password=request.POST.get("txt_password")
    newpassword=request.POST.get("txt_newpassword")
    repassword=request.POST.get("txt_repassword")  
    if dbpass==password:
      if newpassword==repassword:
        teacherdata.teacher_password = newpassword
        teacherdata.save()
        return render(request,"Teacher/Changepass.html",{'msg':"Password changed..."})
      else:
        return render(request,"Teacher/Changepass.html",{'msg':"Password does not match..."})
    else:
      return render(request,"Teacher/Changepass.html",{'msg':"Invalid Old password..."})
  else:
    return render(request,"Teacher/Changepass.html")

def Addstudent(request):
    teacher = tbl_teacher.objects.get(id=request.session['tid'])
    assignclid = tbl_assignclass.objects.filter(teacher=teacher).last()
    is_ct = assignclid is not None
    
    if request.method == "POST":
        if not is_ct:
             return render(request,"Teacher/Addstudent.html",{'msg':"Access Denied: Not a Class Teacher",'is_class_teacher': is_ct})
        
        name=request.POST.get("txt_name")
        email=request.POST.get("txt_email")
        contact=request.POST.get("txt_contact")
        address=request.POST.get("txt_address")
        photo= request.FILES.get("file_photo")
        gender=request.POST.get("txt_gender")
        regno = request.POST.get("txt_number")
        dob=request.POST.get("txt_date")
        password=request.POST.get("txt_password")
        
        tbl_student.objects.create(
            student_name=name, student_email=email, student_contact=contact, 
            student_address=address, student_photo=photo, student_gender=gender, 
            student_dob=dob, student_password=password, assignclass=assignclid, 
            student_registernumber=regno
        )
        # Send welcome email with login credentials
        try:
            send_mail(
                subject="🎓 Welcome to EduSphere – Your Student Account",
                message=(
                    f"Dear {name},\n\n"
                    f"Welcome to EduSphere College Portal! Your student account has been created.\n\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"  YOUR LOGIN CREDENTIALS\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"  Portal URL      : http://localhost:8000/Guest/Login/\n"
                    f"  Email           : {email}\n"
                    f"  Password        : {password}\n"
                    f"  Register Number : {regno}\n"
                    f"  Class           : {assignclid.Class.class_name}\n"
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
        studentdata = tbl_student.objects.filter(assignclass=assignclid)
        return render(request, "Teacher/Addstudent.html", {'msg': "Student Added & Credentials Emailed!", 'studentdata': studentdata, 'is_class_teacher': is_ct})
    else:
        studentdata = tbl_student.objects.filter(assignclass=assignclid) if is_ct else []
        return render(request, "Teacher/Addstudent.html", {'studentdata': studentdata, 'is_class_teacher': is_ct})

def delstudent(request,did):
    tbl_student.objects.get(id=did).delete()
    return render(request,"Teacher/Addstudent.html",{'msg':"Data Deleted..."})

def Addnotes(request):
  teacher =  tbl_teacher.objects.get(id=request.session['tid'])
  department = teacher.department
  coursedata=tbl_course.objects.filter(department=department)
  semesterdata=tbl_semester.objects.all()
  addnotesdata=tbl_notes.objects.filter(teacher=teacher)
  if request.method=="POST":
    file = request.FILES.get("file_note")
    content = request.POST.get("txt_content")
    subject = tbl_subject.objects.get(id=request.POST.get("sel_subject"))
    tbl_notes.objects.create(notes_file=file,notes_content=content,teacher=teacher,subject=subject)
    return render(request,"Teacher/Addnotes.html",{'msg':"Data Inserted..."})
  else:
    return render(request,"Teacher/Addnotes.html",{'coursedata':coursedata,'semesterdata':semesterdata,'addnotesdata':addnotesdata})

def delnotes(request,did):
    tbl_notes.objects.get(id=did).delete()
    return render(request,"Teacher/Addnotes.html",{'msg':"Data Deleted..."})

 

def Ajaxassignsubject(request):
  courseId = request.GET.get("courseId")
  semId = request.GET.get("semId")
  teacher = tbl_teacher.objects.get(id=request.session['tid'])
  subjectdata = tbl_assignsubject.objects.filter(subject__course=courseId,subject__semester=semId,teacher=teacher)
  return render(request,"Teacher/AjaxAssignSubject.html",{'subjectdata':subjectdata})


def Assignment(request):
  teacher =  tbl_teacher.objects.get(id=request.session['tid'])
  department = teacher.department
  coursedata=tbl_course.objects.filter(department=department)
  semesterdata=tbl_semester.objects.all()
  assignmentdata=tbl_assignment.objects.filter(teacher=teacher)
  if request.method=="POST":
    title = request.POST.get("txt_title")
    file = request.FILES.get("file_assignment")
    duedate = request.POST.get("txt_date")
    subject = tbl_subject.objects.get(id=request.POST.get("sel_subject"))
    tbl_assignment.objects.create(assignment_title=title,assignment_file=file,assignment_duedate=duedate,teacher=teacher,subject=subject)
    return render(request,"Teacher/Assignment.html",{'msg':"Data Inserted..."})
  else:
    return render(request,"Teacher/Assignment.html",{'coursedata':coursedata,'semesterdata':semesterdata,'assignmentdata':assignmentdata})
  

def delassignment(request,did):
    tbl_assignment.objects.get(id=did).delete()
    return render(request,"Teacher/Assignment.html",{'msg':"Data Deleted..."})

def Viewuploads(request,aid):
   submitdata=tbl_assignmentbody.objects.filter(assignment=aid)
   return render(request,"Teacher/Viewuploads.html",{'submitdata':submitdata,})

def Addmark(request,aid):
    subassignment=tbl_assignmentbody.objects.get(id=aid)
    if request.method == "POST":
      mark=request.POST.get("txt_mark")
      subassignment.ass_score=mark
      subassignment.ass_status=1
      subassignment.save()
      return render(request,"Teacher/Addmark.html",{'msg':"Score Updated...",'aid':aid})
    else:
      return render(request,"Teacher/Addmark.html")

def Viewstudents(request):
  teacher = tbl_teacher.objects.get(id=request.session['tid'])
  assignclid = tbl_assignclass.objects.filter(teacher=teacher).last()
  is_ct = assignclid is not None
  
  if not is_ct:
      return render(request, "Teacher/Viewstudents.html", {'msg': "Access Denied: Only Class Teachers can view global student data", 'is_class_teacher': False})

  semesterdata = tbl_semester.objects.all()
  coursedata = tbl_course.objects.filter(id=assignclid.Class.course.id)
  
  if request.method == "POST":
    semester = request.POST.get("sel_semester")
    studentdata = tbl_student.objects.filter(assignclass=assignclid)
    return render(request, "Teacher/Viewstudents.html", {'semesterdata': semesterdata, 'coursedata': coursedata, 'studentdata': studentdata, 'is_class_teacher': True})
  else:
    studentdata = tbl_student.objects.filter(assignclass=assignclid)
    return render(request, "Teacher/Viewstudents.html", {'semesterdata': semesterdata, 'coursedata': coursedata, 'studentdata': studentdata, 'is_class_teacher': True})
  
def Addinternalmark(request,aid):
   semesterdata=tbl_semester.objects.all()
   internaldata=tbl_internalmark.objects.filter(student=aid)
   if request.method == "POST":
    score=request.POST.get("txt_internal")   
    subject = tbl_subject.objects.get(id=request.POST.get("sel_subject"))
    tbl_internalmark.objects.create(internal_score=score,subject=subject,student=tbl_student.objects.get(id=aid))
    return render(request,"Teacher/Internalmarks.html",{'msg':"Internal Marks added...",'aid':aid})
   else:
    return render(request,"Teacher/Internalmarks.html",{'semesterdata':semesterdata,'internaldata':internaldata})


   
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

HOURS = [
    ("1", "10:00 - 10:55"),
    ("2", "10:55 - 11:50"),
    ("3", "12:05 - 01:00"),
    ("4", "02:00 - 03:00"),
    ("5", "03:00 - 04:00"),
]

def ViewTimeTable(request):
    teacher = tbl_teacher.objects.get(id=request.session["tid"])
    academicyear = tbl_academicyear.objects.order_by('-id').first()
    today = timezone.now().date()
    
    timetable = tbl_timetable.objects.none()
    if academicyear:
        timetable = tbl_timetable.objects.filter(
            teacher_id=teacher,
            academicyear=academicyear
        )
    
    special_timetable = tbl_specialtimetable.objects.filter(teacher=teacher, date=today)

    return render(request, "Teacher/ViewTimeTable.html", {
        "teacher": teacher,
        "timetable": timetable,
        "special_timetable": special_timetable,
        "today_date": today,
        "days": DAYS,
        "hours": HOURS,
        "academicyear": academicyear
    })

def student_attendance(request):
    teacher = tbl_teacher.objects.get(id=request.session["tid"])
    academicyear = tbl_academicyear.objects.order_by('-id').first()

    departments = tbl_department.objects.all()
    semesters = tbl_semester.objects.all()
    courses = tbl_course.objects.none()

    selected_students = []

    selected_department = request.GET.get("department")
    selected_course = request.GET.get("course")
    selected_semester = request.GET.get("semester")
    selected_hour = request.GET.get("hour")
    selected_day = request.GET.get("day")

    # Filter courses by department
    if selected_department:
        courses = tbl_course.objects.filter(department_id=selected_department)

    # Load students only if all required selections exist
    if all([selected_course, selected_semester, selected_hour, selected_day]):

        timetable_entries = tbl_timetable.objects.filter(
            teacher_id=teacher,
            course_id=selected_course,
            semester_id=selected_semester,
            hour=selected_hour,
            day=selected_day,
            academicyear=academicyear
        )

        for tt in timetable_entries:
            students = tbl_student.objects.filter(
                assignclass__Class__course=tt.course
            )

            for student in students:
                attendance = tbl_attendance.objects.filter(
                    student=student,
                    subject=tt.subject,
                    teacher=teacher,
                    course=tt.course,
                    semester=tt.semester,
                    academicyear=academicyear,
                    date=timezone.now().date(),
                    hour=selected_hour
                ).first()

                selected_students.append({
                    "student": student,
                    "subject": tt.subject,
                    "attendance": attendance.status if attendance else 0
                })

    return render(request, "Teacher/MarkAttendance.html", {
        "teacher": teacher,
        "departments": departments,
        "courses": courses,
        "semesters": semesters,
        "days": DAYS,
        "hours": HOURS,

        "selected_students": selected_students,
        "selected_department": selected_department,
        "selected_course": selected_course,
        "selected_semester": selected_semester,
        "selected_hour": selected_hour,
        "selected_day": selected_day,
    })


def save_attendance_selection(request):
    if request.method == "POST":

        teacher = tbl_teacher.objects.get(id=request.session["tid"])
        academicyear = tbl_academicyear.objects.order_by('-id').first()

        hour = request.POST.get("hour")
        day = request.POST.get("day")
        course_id = request.POST.get("course")
        semester_id = request.POST.get("semester")
        today = timezone.now().date()

        timetable_entries = tbl_timetable.objects.filter(
            teacher_id=teacher,
            course_id=course_id,
            semester_id=semester_id,
            hour=hour,
            day=day,
            academicyear=academicyear
        )

        for tt in timetable_entries:
            students = tbl_student.objects.filter(
                assignclass__Class__course=tt.course
            )

            for student in students:
                # ✅ FIXED NAME
                status = request.POST.get(
                    f"attendance_{student.id}", "0"
                )

                tbl_attendance.objects.update_or_create(
                    student=student,
                    subject=tt.subject,
                    teacher=teacher,
                    course=tt.course,
                    semester=tt.semester,
                    academicyear=academicyear,
                    date=today,
                    hour=hour,
                    defaults={"status": int(status)}
                )

        return redirect("Teacher:student_attendance")
def viewattendance(request, sid):

    studentdata = tbl_student.objects.get(id=sid)
    semesterdata = tbl_semester.objects.all()

    attendancedata = None
    selected_semester = None
    selected_date = None

    if request.method == "POST":

        selected_semester = request.POST.get("sel_semester")
        selected_date = request.POST.get("sel_date")

        attendancedata = tbl_attendance.objects.filter(
            student=studentdata
        )

        if selected_semester:
            attendancedata = attendancedata.filter(semester_id=selected_semester)

        if selected_date:
            attendancedata = attendancedata.filter(date=selected_date)

    return render(request, "Teacher/ViewAttendance.html", {
        "semesterdata": semesterdata,
        "attendancedata": attendancedata,
        "selected_semester": selected_semester,
        "selected_date": selected_date
    })

def Logout(request):
    del request.session['tid']
    return redirect('Guest:Login')

def updateattendance(request):

    if request.method == "POST":

        attendance_ids = request.POST.getlist("attendance_id")

        for aid in attendance_ids:

            status = request.POST.get(f"status_{aid}")

            tbl_attendance.objects.filter(id=aid).update(status=status)

    return redirect(request.META.get('HTTP_REFERER'))

def viewleave(request):
    teacher = tbl_teacher.objects.get(id=request.session['tid'])
    
    # Teachers can oversee student leaves of their assigned classes
    leavedata = tbl_leave.objects.filter(student__assignclass__teacher=teacher)
    
    # HOD override: HODs can perceive all leaves in their department
    if teacher.teacher_role == 'HOD':
        dept_leaves = tbl_leave.objects.filter(student__assignclass__Class__course__department=teacher.department)
        leavedata = (leavedata | dept_leaves).distinct()

    return render(request, "Teacher/Viewleave.html", {'leavedata': leavedata.order_by('-id')})

def accept(request,aid):
    leave = tbl_leave.objects.get(id=aid)
    leave.leave_status = 1
    leave.save()
    return render(request,"Teacher/Viewleave.html",{'msg':"Leave Accepted..."})

def reject(request,rid):
    leave = tbl_leave.objects.get(id=rid)
    leave.leave_status = 2
    leave.save()
    return render(request,"Teacher/Viewleave.html",{'msg':"Leave Rejected..."})

def viewdutyleave(request):
    teacher = tbl_teacher.objects.get(id=request.session['tid'])
    assigned_purposes = tbl_incharge.objects.filter(
        teacher=teacher
    ).values_list('purpose', flat=True)

    dutyleavedata = tbl_dutyleave.objects.filter(
        purpose__in=assigned_purposes
    )
    
    # HODs can also oversee all duty leaves in their department
    if teacher.teacher_role == 'HOD':
        dept_duty = tbl_dutyleave.objects.filter(student__assignclass__Class__course__department=teacher.department)
        dutyleavedata = (dutyleavedata | dept_duty).distinct()

    return render(request, "Teacher/Viewdutyleave.html", {
        'dutyleavedata': dutyleavedata.order_by('-id')
    })

def acceptduty(request,aid):
    dutyleave = tbl_dutyleave.objects.get(id=aid)
    dutyleave.dutyleave_status = 1
    dutyleave.save()
    return render(request,"Teacher/Viewdutyleave.html",{'msg':"Duty Leave Accepted..."})

def rejectduty(request,rid):
    dutyleave = tbl_dutyleave.objects.get(id=rid)
    dutyleave.dutyleave_status = 2
    dutyleave.save()
    return render(request,"Teacher/Viewdutyleave.html",{'msg':"Duty Leave Rejected..."})

def myassignedsubject(request):
    teacher = tbl_teacher.objects.get(id=request.session['tid'])
    assignsubject = tbl_assignsubject.objects.filter(teacher=teacher)
    return render(request, "Teacher/MyAssignedSubjects.html", {'assignsubject': assignsubject})

def ApplyLeave(request):
    teacher = tbl_teacher.objects.get(id=request.session['tid'])
    leavedata = tbl_teacherleave.objects.filter(teacher=teacher).order_by('-id')
    if request.method == "POST":
        title = request.POST.get("txt_title")
        reason = request.POST.get("txt_reason")
        fromdate = request.POST.get("txt_fromdate")
        todate = request.POST.get("txt_todate")
        tbl_teacherleave.objects.create(
            teacher=teacher, leave_title=title, leave_reason=reason,
            leave_fromdate=fromdate, leave_todate=todate
        )
        return render(request, "Teacher/ApplyLeave.html", {'msg': "Leave Applied Successfully", 'leavedata': leavedata})
    return render(request, "Teacher/ApplyLeave.html", {'leavedata': leavedata})

def delteacherleave(request, did):
    tbl_teacherleave.objects.get(id=did).delete()
    return redirect("Teacher:ApplyLeave")
   