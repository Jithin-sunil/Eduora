from django.shortcuts import redirect, render
from Teacher.models import *
from Admin.models import *
from Student.models import *
from django.db.models import Count, Q
from datetime import date,timedelta
from django.utils import timezone


# Create your views here.
def Homepage(request):
    student = tbl_student.objects.get(id=request.session['sid'])
    
    # Attendance Stats
    attendance = tbl_attendance.objects.filter(student=student)
    total_attendance = attendance.count()
    present_attendance = attendance.filter(status=1).count()
    attendance_percentage = (present_attendance / total_attendance * 100) if total_attendance > 0 else 0
    
    # Internal Marks Stats
    internal_marks = tbl_internalmark.objects.filter(student=student)
    
    # Assignment Stats
    total_assignments = tbl_assignment.objects.filter(subject__course=student.assignclass.Class.course).count()
    submitted_assignments = tbl_assignmentbody.objects.filter(student=student).count()
    assignment_percentage = (submitted_assignments / total_assignments * 100) if total_assignments > 0 else 0
    
    # Recent Activities (e.g., Notifications)
    notifications = tbl_notification.objects.all().order_by('-id')[:5]

    context = {
        'student': student,
        'attendance_percentage': round(attendance_percentage, 2),
        'total_attendance': total_attendance,
        'present_attendance': present_attendance,
        'total_assignments': total_assignments,
        'submitted_assignments': submitted_assignments,
        'assignment_percentage': round(assignment_percentage, 2),
        'internal_marks': internal_marks,
        'notifications': notifications
    }
    return render(request, "Student/Homepage.html", context)

def Myprofile(request):
  studentdata = tbl_student.objects.get(id=request.session['sid'])
  return render(request,"Student/Myprofile.html",{'student':studentdata})

def Editprofile(request):
  studentdata = tbl_student.objects.get(id=request.session['sid'])
  if request.method == "POST":
    name=request.POST.get("txt_name")
    email=request.POST.get("txt_email")
    contact=request.POST.get("txt_contact")
    address=request.POST.get("txt_address")
        
    studentdata.student_name = name
    studentdata.student_email= email
    studentdata.student_contact= contact
    studentdata.student_address= address
    studentdata.save()
    
    return render(request,"Student/Editprofile.html",{'msg':"Data Updated..."})
  else:
    return render(request,"Student/Editprofile.html",{'student':studentdata})
 

def Changepass(request):
  studentdata = tbl_student.objects.get(id=request.session['sid'])
  dbpass=studentdata.student_password
  if request.method == "POST":
    password=request.POST.get("txt_password")
    newpassword=request.POST.get("txt_newpassword")
    repassword=request.POST.get("txt_repassword")  
    if dbpass==password:
      if newpassword==repassword:
        studentdata.student_password = newpassword
        studentdata.save()
        return render(request,"Student/Changepass.html",{'msg':"Password changed..."})
      else:
        return render(request,"Student/Changepass.html",{'msg':"Password does not match..."})
    else:
      return render(request,"Student/Changepass.html",{'msg':"Invalid Old password..."})
  else:
    return render(request,"Student/Changepass.html")

def Viewnotes(request):
  semesterdata = tbl_semester.objects.all()
  return render(request,"Student/Viewnotes.html",{'semesterdata':semesterdata})

def AjaxSubject(request):
  semid = request.GET.get("semid")
  studentdata = tbl_student.objects.get(id=request.session['sid'])
  courseId = studentdata.assignclass.Class.course
  subjectdata=tbl_subject.objects.filter(course=courseId,semester=semid)
  return render(request,"Student/AjaxSubject.html",{'subjectdata':subjectdata})

def Ajaxnotes(request):
  subid = request.GET.get("subid")
  notedata = tbl_notes.objects.filter(subject=subid)
  return render(request,"Student/Ajaxnotes.html",{'notedata':notedata})

def Viewassignment(request):
    student = tbl_student.objects.get(id=request.session['sid'])
    course = student.assignclass.Class.course
    assignmentdata = tbl_assignment.objects.filter(subject__course=course).order_by('-id')
    
    # Identify which ones are already submitted
    submitted_ids = tbl_assignmentbody.objects.filter(student=student).values_list('assignment_id', flat=True)
    
    return render(request, "Student/Viewassignment.html", {
        'assignmentdata': assignmentdata,
        'submitted_ids': list(submitted_ids)
    })

def Submitassignment(request,aid):
  assignment=tbl_assignment.objects.get(id=aid)
  studentdata = tbl_student.objects.get(id=request.session['sid'])
  submitdata = tbl_assignmentbody.objects.filter(student=studentdata,assignment=assignment)
  if request.method =="POST":
    ass=request.FILES.get("file_submit")
    tbl_assignmentbody.objects.create(ass_file=ass, student=studentdata,assignment=assignment)
    return render(request,"Student/Submitassignment.html",{'msg':"Data Inserted...",'aid':aid})
  else:
    return render(request,"Student/Submitassignment.html",{'submitdata':submitdata,'aid':aid})

    
def delassign(request,did,aid):
    tbl_assignmentbody.objects.get(id=did).delete()
    return render(request,"Student/Submitassignment.html",{'msg':"Data Deleted...",'aid':aid})

def Myassignments(request):
  submitdata=tbl_assignmentbody.objects.filter(student=request.session['sid'])
  return render(request,"Student/Myassignments.html",{'submitdata':submitdata})

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

HOURS = [
    ("1", "10:00 - 10:55"),
    ("2", "10:55 - 11:50"),
    ("3", "12:05 - 01:00"),
    ("4", "02:00 - 03:00"),
    ("5", "03:00 - 04:00"),
]


import datetime

def ViewTimeTable(request):
    student = tbl_student.objects.get(id=request.session['sid'])
    assignclass = student.assignclass
    course = assignclass.Class.course
    # Get current semester for this specific class
    current_classsem = tbl_classsem.objects.filter(assignclass=assignclass).last()
    current_semester = current_classsem.semester if current_classsem else None
    academicyear = tbl_academicyear.objects.order_by('-id').first()

    today = datetime.date.today()
    
    # Regular Timetable
    timetable = tbl_timetable.objects.none()
    if current_semester and academicyear:
        timetable = tbl_timetable.objects.filter(
            course=course,
            semester=current_semester,
            academicyear=academicyear
        )

    # Special Timetable for today
    special_timetable = tbl_specialtimetable.objects.filter(
        assignclass=assignclass,
        date=today
    )

    timetable_grid = []
    for day in DAYS:
        row = []
        for hour, label in HOURS:
            # Check special timetable first for today
            special = None
            if day == today.strftime("%A"):
                special = special_timetable.filter(hour=hour).first()
            
            if special:
                row.append({'type': 'special', 'subject': special.subject.subject_name, 'teacher': special.teacher.teacher_name})
            else:
                regular = timetable.filter(day=day, hour=hour).first()
                if regular:
                    row.append({'type': 'regular', 'subject': regular.subject.subject_name, 'teacher': regular.teacher_id.teacher_name})
                else:
                    row.append(None)
        timetable_grid.append({'day': day, 'slots': row})

    return render(request, "Student/ViewTimeTable.html", {
        "student": student,
        "grid": timetable_grid,
        "special_timetable": special_timetable,
        "today_date": today,
        "days": DAYS,
        "hours": HOURS,
        "semester": current_semester,
        "course": course,
        "academicyear": academicyear
    })


def Complaint(request):
    studentdata = tbl_student.objects.get(id=request.session['sid'])
    complaintdata = tbl_complaint.objects.filter(student=studentdata)
    if request.method == "POST":
        title = request.POST.get("txt_title")
        content = request.POST.get("txt_content")
        tbl_complaint.objects.create(comp_title=title,com_content=content,
            student=studentdata)
        return render(request, "Student/Complaint.html", {'msg': "Complaint Submitted..."})
    else:
        return render(request, "Student/Complaint.html",{'complaintdata':complaintdata})

def delcomplaint(request,did):
    tbl_complaint.objects.get(id=did).delete()
    return render(request,"Student/Complaint.html",{'msg':"Data Deleted..."})




def viewattendance(request):
    studentdata = tbl_student.objects.get(id=request.session['sid'])
    semesterdata = tbl_semester.objects.all()

    today = timezone.now().date()

    attendancedata = None
    subjectwise = None
    overall_percentage = 0

    last_classsem = tbl_classsem.objects.all().order_by('-id').first()
    current_semester = last_classsem.semester if last_classsem else None

    if request.method == "POST":

        selected_semester = request.POST.get("sel_semester")
        filter_type = request.POST.get("filter_type")
        from_date = request.POST.get("from_date")
        to_date = request.POST.get("to_date")

        attendancedata = tbl_attendance.objects.filter(student=studentdata)

        if selected_semester:
            attendancedata = attendancedata.filter(semester_id=selected_semester)

        # Daily
        if filter_type == "daily":
            attendancedata = attendancedata.filter(date=today)

        # Weekly
        elif filter_type == "weekly":
            start_week = today - timedelta(days=today.weekday())
            end_week = start_week + timedelta(days=6)
            attendancedata = attendancedata.filter(date__range=[start_week, end_week])

        # Monthly
        elif filter_type == "monthly":
            attendancedata = attendancedata.filter(
                date__month=today.month,
                date__year=today.year
            )

        # Date Range
        elif filter_type == "range":
            if from_date and to_date:
                attendancedata = attendancedata.filter(date__range=[from_date, to_date])

        # ✅ Overall Percentage Calculation
        total_classes = attendancedata.count()
        present_classes = attendancedata.filter(status=1).count()

        if total_classes > 0:
            overall_percentage = (present_classes / total_classes) * 100

        # Subject-wise Attendance
        subjectwise = attendancedata.values(
            'subject__subject_name'
        ).annotate(
            total=Count('id'),
            present=Count('id', filter=Q(status=1))
        )

    else:
        attendancedata = tbl_attendance.objects.filter(
            student=studentdata,
            semester=current_semester,
            date=today
        )

        # Default percentage (today)
        total_classes = attendancedata.count()
        present_classes = attendancedata.filter(status=1).count()

        if total_classes > 0:
            overall_percentage = (present_classes / total_classes) * 100


    return render(request, "Student/ViewAttendance.html", {
        "semesterdata": semesterdata,
        "attendancedata": attendancedata,
        "subjectwise": subjectwise,
        "overall_percentage": overall_percentage,
        "selected_semester": current_semester.id if current_semester else None
    })

def leaveapplication(request):
    studentdata = tbl_student.objects.get(id=request.session['sid'])
    leavedata = tbl_leave.objects.filter(student=studentdata)
    if request.method == "POST":
        title = request.POST.get("txt_title")
        reason = request.POST.get("txt_reason")
        fromdate = request.POST.get("txt_fromdate")
        todate = request.POST.get("txt_todate")
        tbl_leave.objects.create(leave_title=title,leave_reason=reason,
            leave_fromdate=fromdate,leave_todate=todate,
            student=studentdata)
        return render(request, "Student/Leave.html", {'msg': "Leave Application Submitted..."})
    else:
        return render(request, "Student/Leave.html",{'leavedata':leavedata})
   
def delleave(request,did):
    tbl_leave.objects.get(id=did).delete()
    return render(request,"Student/Leave.html",{'msg':"Data Deleted..."})

def dutyleave(request):
   studentdata = tbl_student.objects.get(id=request.session['sid'])
   dutyleavedata = tbl_dutyleave.objects.filter(student=studentdata)
   purposedata = tbl_purpose.objects.all()
   if request.method == "POST":
      purposeid=tbl_purpose.objects.get(id=request.POST.get("sel_purpose"))
      reason = request.POST.get("txt_reason")
      hour = request.POST.get("txt_hour")
      fromdate = request.POST.get("txt_fromdate")
      todate = request.POST.get("txt_todate")
      tbl_dutyleave.objects.create(dutyleave_reason=reason,dutyleave_hour=hour,dutyleave_fromdate=fromdate,dutyleave_todate=todate,
          student=studentdata,purpose=purposeid)
      return render(request, "Student/Dutyleave.html", {'msg': "Duty Leave Submitted..."})
   else:
      return render(request, "Student/Dutyleave.html",{'dutyleavedata':dutyleavedata,'purposedata':purposedata})
          
def deldutyleave(request,did):
    tbl_dutyleave.objects.get(id=did).delete()
    return render(request,"Student/Dutyleave.html",{'msg':"Data Deleted..."})
         
         
    
def logout(request):
    del request.session['sid']
    return redirect('Guest:Login')

import json
from django.http import JsonResponse
from Student.chatbot_ml import edubot_instance

def chat(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "")
            student_id = request.session.get('sid')
            
            if not student_id:
                return JsonResponse({"reply": "Session expired. Please login again."})
            
            student = tbl_student.objects.get(id=student_id)
            
            # Use ML-based EduBot
            reply = edubot_instance.get_response(user_message, student)
            return JsonResponse({"reply": reply})
            
        except Exception as e:
            return JsonResponse({"reply": f"Ooops, I'm having a bit of trouble: {str(e)}"})
            
    return JsonResponse({"error": "Invalid request"}, status=400)

  
    
   