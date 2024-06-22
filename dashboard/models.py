from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Test(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    

    def __str__(self):
        return self.name
    

class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question = models.TextField()

    def __str__(self):
        return self.question
    

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    option = models.CharField(max_length=1, choices=(("A", "A"), ("B", "B"), ("C", "C"), ("D", "D")))

    def __str__(self):
        return self.choice
    
class UserTestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.IntegerField()
    total = models.IntegerField()
    percentage = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)  # Automatically set the field to now when the object is first created
