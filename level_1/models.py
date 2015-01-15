from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Question(models.Model):
    description = models.TextField()
    choice_1 = models.TextField()
    choice_2 = models.TextField()
    choice_3 = models.TextField()
    choice_4 = models.TextField()
    answer = models.IntegerField(default=0)	
    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'question'
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'


class Answer(models.Model):
    user = models.ForeignKey(User)
    answer_list = models.CommaSeparatedIntegerField(max_length=255)
    active_status_list = models.CommaSeparatedIntegerField(max_length=255)
    s1 = models.IntegerField(default=-1)
    s2 = models.IntegerField(default=-1)
    s3 = models.IntegerField(default=-1)				
    def __str__(self):
        return str(self.user)
    class Meta:
    	    db_table = 'answer'
    	    verbose_name = 'Answer'
    	    verbose_name_plural = 'Answers'



