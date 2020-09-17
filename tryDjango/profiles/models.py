from django.db import models

# Create your models here.
class ConfUser(models.Model):
	user_name = models.CharField(max_length=50)
	vercode = models.CharField(max_length=9)
	email = models.EmailField()