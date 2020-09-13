from django.db import models

# Create your models here.
class Data(models.Model):
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	email = models.EmailField(unique=True)
	profile = models.ImageField(upload_to='',null=True)
	date_of_birth = models.DateField()