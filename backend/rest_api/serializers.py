from enum import unique

from django.core.validators import RegexValidator
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer
from rest_framework.validators import UniqueValidator

from .models import Animaltype, Breed, Animal, Weighting
from django.contrib.auth.models import Group, User



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_superuser']
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
            # 'is_superuser': {'required': True}
        }
#
#
# class GroupSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Group
#         fields = ['name']



class CustomUserCreateSerializer(UserCreateSerializer):
    email = serializers.EmailField(required=True, trim_whitespace=True)
    username = serializers.CharField(
        required=True, max_length=150, trim_whitespace=True,
        error_messages={'invalid': 'Не более 150 символов. Разрешённые символы: a-z, 0-9, - . @  _ +.'},
        validators=[
            UniqueValidator(queryset=User.objects.all(), message=("Такой пользователь уже существует")),
            RegexValidator(regex=r'^[a-z0-9-_@\.\+]*$', message=("Разрешённые символы: a-z, 0-9, - . @  _ +."))
        ]
    )

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ["id", "email", "username", "first_name", "last_name", "is_active", 'password']
        # extra_kwargs = {
        #     'email': {'required': True},
        #     'username': {'required': True},
        #     # 'password': {'required': True}
        # }



class AnimaltypeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        required=True, trim_whitespace=True, max_length=100,
        validators=[
            UniqueValidator(queryset=Animaltype.objects.all(), message=("Такой тип уже существует")),
        ]
    )
    class Meta:
        model = Animaltype
        fields = '__all__'



class BreedSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        required=True, trim_whitespace=True, max_length=100,
        validators=[
            UniqueValidator(queryset=Breed.objects.all(), message=("Такая порода уже существует")),
        ]
    )
    animaltype_name = serializers.CharField(source='animaltype.name', required=False)
    class Meta:
        model = Breed
        fields = '__all__'



class AnimalSerializer(serializers.ModelSerializer):
    animaltype = serializers.CharField(source='breed.animaltype.id', required=False, allow_blank=True, allow_null=True)
    animaltype_name = serializers.CharField(source='breed.animaltype.name', required=False, allow_blank=True, allow_null=True)
    breed_name = serializers.CharField(source='breed.name', required=False)
    parent_name = serializers.CharField(source='parent.name', required=False, allow_blank=True, allow_null=True)
    invent_num = serializers.CharField(
        max_length=10, required=True,
        validators=[UniqueValidator(queryset=Animal.objects.all(), message=("Такой инвентарный номер уже существует")),]
    )
    class Meta:
        model = Animal
        fields = '__all__'



class WeightingSerializer(serializers.ModelSerializer):
    animal_name = serializers.CharField(source='animal.name', required=False)
    breed_name = serializers.CharField(source='animal.breed.name', required=False)
    animaltype_name = serializers.CharField(source='animal.breed.animaltype.name', required=False)
    username = serializers.CharField(source='user.username', required=False, allow_blank=True, allow_null=True)
    gender = serializers.BooleanField(source='animal.gender', required=False, allow_null=True)
    invent_num = serializers.CharField(source='animal.invent_num', required=False)
    class Meta:
        model = Weighting
        fields = '__all__'