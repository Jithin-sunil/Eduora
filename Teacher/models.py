from django.db import models
from Admin.models import *
# Create your models here.
class tbl_student(models.Model):
    student_name=models.CharField(max_length=50)
    student_email=models.CharField(max_length=50)
    student_registernumber=models.CharField(max_length=50,null=True)
    student_contact=models.CharField(max_length=50)
    student_address=models.CharField(max_length=50)
    student_photo=models.FileField(upload_to="Assets/StudentDocs/")
    student_gender=models.CharField(max_length=50)
    student_dob=models.CharField(max_length=50)
    student_password=models.CharField(max_length=50)
    assignclass=models.ForeignKey(tbl_assignclass,on_delete=models.CASCADE)

class tbl_notes(models.Model):
    notes_file=models.FileField(upload_to="Assets/Notes/")
    notes_content=models.CharField(max_length=50)
    subject=models.ForeignKey(tbl_subject,on_delete=models.CASCADE)
    teacher=models.ForeignKey(tbl_teacher,on_delete=models.CASCADE)

class tbl_assignment(models.Model):
    assignment_title=models.CharField(max_length=100)
    assignment_file=models.FileField(upload_to="Assets/Assignments/")
    assignment_duedate=models.DateField()
    assignment_date=models.DateField(auto_now_add=True)
    assignment_status = models.IntegerField(default=0)
    subject=models.ForeignKey(tbl_subject,on_delete=models.CASCADE)
    teacher=models.ForeignKey(tbl_teacher,on_delete=models.CASCADE)

class tbl_internalmark(models.Model):
    student=models.ForeignKey(tbl_student,on_delete=models.CASCADE)
    subject=models.ForeignKey(tbl_subject,on_delete=models.CASCADE)
    internal_score=models.CharField(max_length=50)
    internal_date = models.DateField(auto_now_add=True)

class tbl_attendance(models.Model):
    student = models.ForeignKey(tbl_student, on_delete=models.CASCADE)
    subject = models.ForeignKey(tbl_subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(tbl_teacher, on_delete=models.CASCADE)
    course = models.ForeignKey(tbl_course, on_delete=models.CASCADE)
    semester = models.ForeignKey(tbl_semester, on_delete=models.CASCADE)
    academicyear = models.ForeignKey(tbl_academicyear, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    hour = models.CharField(max_length=2)  # 1-5
    status = models.IntegerField(default=0)

class tbl_teacherleave(models.Model):
    teacher = models.ForeignKey(tbl_teacher,on_delete=models.CASCADE)
    leave_title = models.CharField(max_length=200)
    leave_reason = models.TextField()
    leave_status = models.IntegerField(default=0)
    leave_date = models.DateField(auto_now_add=True)
    leave_fromdate = models.DateField(null=True)
    leave_todate = models.DateField(null=True)

