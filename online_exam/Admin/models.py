from django.db import models
from register_login.models import *

# Create your models here.


class Exams(models.Model):
    exam_name = models.CharField(max_length=100,null=True,blank=True) 
    exam_date = models.DateField(max_length=255,null=True,blank=True)
    no_of_questions = models.IntegerField(null=True,default=0)
    total_score = models.IntegerField(null=True,default=0)
    passing_score = models.IntegerField(null=True,default=0)
    duration = models.IntegerField(null=True, default=0)


class Questions(models.Model):
    exam = models.ForeignKey(Exams, on_delete=models.CASCADE,null=True,blank=True)
    question = models.CharField(max_length=255,null=True,blank=True)
    answer = models.CharField(max_length=255,null=True,blank=True)
    choice1 = models.CharField(max_length=255,null=True,blank=True)
    choice2 = models.CharField(max_length=255,null=True,blank=True)
    choice3 = models.CharField(max_length=255,null=True,blank=True) 


class QuestionsAttended(models.Model):
    exam = models.ForeignKey(Exams, on_delete=models.CASCADE,null=True,blank=True)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE,null=True,blank=True)
    student = models.ForeignKey(StudentDetails, on_delete=models.CASCADE,null=True,blank=True)
    answer = models.CharField(max_length=255,null=True,blank=True)
    answer_status = models.CharField(max_length=100,null=True,blank=True)

class ExamResults(models.Model):
    exam = models.ForeignKey(Exams, on_delete=models.CASCADE,null=True,blank=True)
    student = models.ForeignKey(StudentDetails, on_delete=models.CASCADE,null=True,blank=True)
    questions_attempted = models.IntegerField(null=True,default=0)
    score = models.IntegerField(null=True,default=0)
    exam_status = models.CharField(max_length=100,null=True,blank=True)


class ExamFeedback(models.Model):
    exam = models.ForeignKey(Exams, on_delete=models.CASCADE,null=True,blank=True)
    student = models.ForeignKey(StudentDetails, on_delete=models.CASCADE,null=True,blank=True)
    feedback = models.CharField(max_length=255,null=True,blank=True) 
    date = models.DateField( max_length=255,null=True,blank=True)





