from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Animaltype(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



class Breed(models.Model):
    animaltype = models.ForeignKey(Animaltype, on_delete=models.PROTECT, related_name='breeds')
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + ' (' + self.animaltype.name + ')'



class Animal(models.Model):
    breed = models.ForeignKey(Breed, on_delete=models.PROTECT, related_name='animals')
    invent_num = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    gender = models.BooleanField(blank=True, null=True, default=None)
    arrival_date = models.DateField()
    arrival_age = models.PositiveSmallIntegerField()
    parent = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, related_name='animals')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + '(' + str(self.invent_num) + ')'



class Weighting(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='weightings')
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='weightings')
    weight = models.DecimalField(max_digits=9, decimal_places=3)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.animal.__str__() + ', ' + str(self.weight)