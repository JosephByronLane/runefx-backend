from django.shortcuts import render
from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response

from .models import Release
from .serializers import ReleaseSerializer, ReleaseSerializerWithoutContent
# Create your views here.




class ReleaseViewSet(viewsets.ModelViewSet):
    queryset = Release.objects.all()

    serializer_class = ReleaseSerializerWithoutContent
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


    def perform_create(self, serializer):
        return super().perform_create(serializer)
    
    def get_queryset(self):
        return super().get_queryset()
    
class ReleaseDetailView(generics.RetrieveAPIView):
    queryset = Release.objects.all().order_by('-created_at')
    serializer_class = ReleaseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    lookup_field = 'id'
    lookup_url_kwarg = 'release_id'