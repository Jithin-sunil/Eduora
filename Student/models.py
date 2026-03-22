from django.db import models
from Teacher.models import *
from django.core.exceptions import ValidationError
from django.utils import timezone

def validate_future_date(value):
    if value < timezone.now().date():
        raise ValidationError('Date cannot be in the past.')

# Create your models here.
class tbl_complaint(models.Model):
    comp_title = models.CharField(max_length=200)
    com_content =  models.TextField()
    com_date =  models.DateField(auto_now_add=True)
    com_status = models.IntegerField(default=0)
    com_reply = models.TextField()
    student= models.ForeignKey(tbl_student,on_delete=models.CASCADE)

class tbl_assignmentbody(models.Model):
    ass_date = models.DateField(auto_now_add=True)
    ass_status = models.IntegerField(default=0)
    ass_score = models.CharField(max_length=200)
    ass_file = models.FileField(upload_to="Assets/Assignment/Files/")
    student =  models.ForeignKey(tbl_student,on_delete=models.CASCADE)
    assignment = models.ForeignKey(tbl_assignment,on_delete=models.CASCADE)

class tbl_leave(models.Model):
    leave_title = models.CharField(max_length=200)
    leave_reason = models.TextField()
    leave_status = models.IntegerField(default=0)
    leave_fromdate = models.DateField(null=True, validators=[validate_future_date])
    leave_todate = models.DateField(null=True, validators=[validate_future_date])
    leave_date =  models.DateField(auto_now_add=True)
    student = models.ForeignKey(tbl_student,on_delete=models.CASCADE)

    def clean(self):
        if self.leave_fromdate and self.leave_todate and self.leave_todate < self.leave_fromdate:
            raise ValidationError('To date must be after or equal to from date.')

class tbl_dutyleave(models.Model):
    dutyleave_date = models.DateField(auto_now_add=True)
    dutyleave_status = models.IntegerField(default=0)
    dutyleave_reason = models.TextField()
    dutyleave_hour = models.CharField(max_length=100)
    dutyleave_fromdate = models.DateField(null=True, validators=[validate_future_date])
    dutyleave_todate = models.DateField(null=True, validators=[validate_future_date])
    student = models.ForeignKey(tbl_student,on_delete=models.CASCADE)
    purpose = models.ForeignKey(tbl_purpose,on_delete=models.CASCADE)

    def clean(self):
        if self.dutyleave_fromdate and self.dutyleave_todate and self.dutyleave_todate < self.dutyleave_fromdate:
            raise ValidationError('To date must be after or equal to from date.')
    