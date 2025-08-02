from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Candidate(models.Model):      #candidate table contain student or employee who is going to attempt the test
    username=models.CharField(max_length=40)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=8)
 

def __str__(self):
    return self.username +" "+ self.email+" "+self.password+" "+self.country

#below is the model of subject which stores subject name

class Subject(models.Model):
    name=models.CharField(max_length=100)

#below is the model of question which is used to store questions

class Question(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    text = models.TextField()
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)
    correct_option = models.CharField(max_length=200)

#below is the model of result which is used to store result of user 

class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    score = models.IntegerField()
    total_questions = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)


#to make profile module responsive we have to make models to store user details
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username