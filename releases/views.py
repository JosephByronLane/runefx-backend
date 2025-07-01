from django.shortcuts import render
from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response

from .models import Release
from .serializers import ReleaseSerializer, ReleaseSerializerWithoutContent
# Create your views here.




class ReleaseViewSet(viewsets.ModelViewSet):
    queryset = Release.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.action in ['create', 'retrieve']:
            return ReleaseSerializer
        return ReleaseSerializerWithoutContent    

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    def get_queryset(self):
        return Release.objects.all().order_by('-created_at')
    
