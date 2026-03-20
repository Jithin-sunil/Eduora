from django.db import models

# Create your models here.
class tbl_admin(models.Model):
    admin_name=models.CharField(max_length=15)
    admin_email=models.CharField(max_length=30)
    admin_password=models.CharField(max_length=10)

class tbl_department(models.Model):
    department_name=models.CharField(max_length=50)

class tbl_semester(models.Model):
    semester_name=models.CharField(max_length=50)

class tbl_academicyear(models.Model):
    academicyear_name=models.CharField(max_length=50)

class tbl_course(models.Model):
    course_name=models.CharField(max_length=60)
    department = models.ForeignKey(tbl_department,on_delete=models.CASCADE)

class tbl_subject(models.Model):
    subject_name=models.CharField(max_length=100)
    course = models.ForeignKey(tbl_course,on_delete=models.CASCADE)
    semester = models.ForeignKey(tbl_semester,on_delete=models.CASCADE)

class tbl_class(models.Model):
    class_name=models.CharField(max_length=60)
    course = models.ForeignKey(tbl_course,on_delete=models.CASCADE)

class tbl_teacher(models.Model):
    teacher_name=models.CharField(max_length=50)
    teacher_email=models.CharField(max_length=50)
    teacher_contact=models.CharField(max_length=50)
    teacher_role=models.CharField(max_length=50)
    teacher_gender=models.CharField(max_length=50)
    teacher_photo=models.FileField(upload_to="Assets/TeacherDocs/")
    teacher_password=models.CharField(max_length=50)
    department = models.ForeignKey(tbl_department,on_delete=models.CASCADE)

class tbl_assignclass(models.Model):
    Class = models.ForeignKey(tbl_class,on_delete=models.CASCADE)
    teacher = models.ForeignKey(tbl_teacher,on_delete=models.CASCADE)
    academicyear = models.ForeignKey(tbl_academicyear,on_delete=models.CASCADE)

class tbl_assignsubject(models.Model):
    teacher = models.ForeignKey(tbl_teacher,on_delete=models.CASCADE)
    academicyear = models.ForeignKey(tbl_academicyear,on_delete=models.CASCADE)
    subject=models.ForeignKey(tbl_subject,on_delete=models.CASCADE)

class tbl_classsem(models.Model):
    semester = models.ForeignKey(tbl_semester,on_delete=models.CASCADE)
    assignclass = models.ForeignKey(tbl_assignclass,on_delete=models.CASCADE)


class tbl_timetable(models.Model):
    course = models.ForeignKey(tbl_course,on_delete=models.CASCADE)
    semester = models.ForeignKey(tbl_semester,on_delete=models.CASCADE)
    academicyear = models.ForeignKey(tbl_academicyear,on_delete=models.CASCADE)
    day = models.CharField(max_length=20)
    hour = models.CharField(max_length=5)
    subject = models.ForeignKey(tbl_subject,on_delete=models.CASCADE)
    teacher_id = models.ForeignKey(tbl_teacher,on_delete=models.CASCADE)

class tbl_purpose(models.Model):
    purpose_name = models.CharField(max_length=100)

class tbl_incharge(models.Model):
    teacher = models.ForeignKey(tbl_teacher,on_delete=models.CASCADE)
    purpose = models.ForeignKey(tbl_purpose,on_delete=models.CASCADE)

class tbl_notification(models.Model):
    notification_title = models.CharField(max_length=200)
    notification_content = models.TextField()
    notification_date = models.DateField(auto_now_add=True)

class tbl_specialtimetable(models.Model):
    date = models.DateField()
    hour = models.CharField(max_length=5)
    subject = models.ForeignKey(tbl_subject,on_delete=models.CASCADE)
    teacher = models.ForeignKey(tbl_teacher,on_delete=models.CASCADE)
    assignclass = models.ForeignKey(tbl_assignclass,on_delete=models.CASCADE)

class tbl_otp(models.Model):
    otp_email = models.EmailField()
    otp_code = models.CharField(max_length=6)
    otp_time = models.DateTimeField(auto_now_add=True)
    otp_status = models.IntegerField(default=0)
