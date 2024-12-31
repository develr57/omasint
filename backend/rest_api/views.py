from django.conf import settings
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets, status
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models.deletion import ProtectedError
from rest_framework.response import Response
from rest_framework.settings import api_settings

from .models import Animaltype, Breed, Animal, Weighting
from .serializers import AnimaltypeSerializer, BreedSerializer, AnimalSerializer, WeightingSerializer
    #UserSerializer, GroupSerializer
from django.contrib.auth.models import Group, User
import datetime
from django.utils import timezone



# Create your views here.
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     # permission_classes = [permissions.IsAuthenticated]
#
#
#
# class GroupViewSet(viewsets.ModelViewSet):
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer
#     # permission_classes = [permissions.IsAuthenticated]



class AnimaltypeViewSet(viewsets.ModelViewSet):
    queryset = Animaltype.objects.all().order_by('id')
    serializer_class = AnimaltypeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name']
    search_fields = ['$name']
    ordering_fields = ['name']
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError as e:
            return Response({'detail': 'Запись не может быть удалена, т.к. на нёё ссылаются другие.'},
                            status=status.HTTP_403_FORBIDDEN)



class BreedViewSet(viewsets.ModelViewSet):
    queryset = Breed.objects.all().order_by('id').select_related('animaltype')
    serializer_class = BreedSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name']
    search_fields = ['$name']
    ordering_fields = ['name']
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError as e:
            return Response({'detail': 'Запись не может быть удалена, т.к. на нёё ссылаются другие.'},
                            status=status.HTTP_403_FORBIDDEN)



class AnimalViewSet(viewsets.ModelViewSet):
    queryset = Animal.objects.all().order_by('id').select_related('breed', 'breed__animaltype')
    serializer_class = AnimalSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name']
    search_fields = ['$name']
    ordering_fields = ['name']
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError as e:
            return Response({'detail': 'Запись не может быть удалена, т.к. на нёё ссылаются другие.'},
                            status=status.HTTP_403_FORBIDDEN)



class WeightingViewSet(viewsets.ModelViewSet):
    queryset = Weighting.objects.all().order_by('id').select_related('animal', 'user')
    serializer_class = WeightingSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['id', 'animal', 'user']
    # search_fields = ['$name']
    ordering_fields = ['id', 'created_at']
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            queryset = self.filter_queryset(self.get_queryset())
        else:
            queryset = self.filter_queryset(self.get_queryset().filter(user=self.request.user.id))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        tz = timezone.get_current_timezone()
        query = Weighting.objects.all().filter(animal=request.data.get('animal'))
        if query.count() > 0:
            date = query.last().created_at.astimezone(tz).date()
            if date == datetime.datetime.now().astimezone(tz).date():
                return Response({'detail': 'Нельзя фиксировать вес животного более одного раза в день'},
                                status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}