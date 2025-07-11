from django.shortcuts import render
from django.shortcuts import render
from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response

from .models import Movie
from .serializers import VfxSerializerDetail, VfxSerializerBase
# Create your views here.
class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]   

    def get_serializer_class(self):
        if self.action in ['create', 'retrieve']:
            return VfxSerializerDetail
        return VfxSerializerBase  
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    def get_queryset(self):
        return Movie.objects.all().order_by('-year')
    
