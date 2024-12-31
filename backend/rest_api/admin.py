from django.contrib import admin

# Register your models here.
from .models import Animaltype, Breed, Animal, Weighting


class AnimaltypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at')
    list_display_links = ('id',)
    search_fields = ('id', 'name', 'created_at', 'updated_at')
    list_editable = ('name',)
    list_filter = ('name', 'created_at', 'updated_at')


class BreedAdmin(admin.ModelAdmin):
    list_display = ('id', 'animaltype', 'name', 'created_at', 'updated_at')
    list_display_links = ('id',)
    search_fields = ('id', 'animaltype', 'name', 'created_at', 'updated_at')
    list_editable = ('animaltype', 'name',)
    list_filter = ('animaltype', 'name', 'created_at', 'updated_at')



class AnimalAdmin(admin.ModelAdmin):
    list_display = ('id', 'breed', 'invent_num', 'name', 'gender', 'arrival_date', 'arrival_age', 'parent',
                    'created_at', 'updated_at')
    list_display_links = ('id',)
    search_fields = ('id', 'breed', 'invent_num', 'name', 'gender', 'arrival_date', 'arrival_age', 'parent',
                     'created_at', 'updated_at')
    list_editable = ('breed', 'invent_num', 'name', 'gender', 'arrival_date', 'arrival_age', 'parent',)
    list_filter = ('breed', 'invent_num', 'name', 'gender', 'arrival_date', 'arrival_age', 'parent',
                   'created_at', 'updated_at')



class WeightingAdmin(admin.ModelAdmin):
    list_display = ('id', 'animal', 'user', 'weight', 'created_at', 'updated_at',)
    list_display_links = ('id',)
    search_fields = ('id', 'animal', 'user', 'weight', 'created_at', 'updated_at',)
    list_filter = ('animal', 'user', 'weight', 'created_at', 'updated_at',)
    list_editable = ('animal', 'user', 'weight',)



admin.site.register(Animaltype, AnimaltypeAdmin)
admin.site.register(Breed, BreedAdmin)
admin.site.register(Animal, AnimalAdmin)
admin.site.register(Weighting, WeightingAdmin)