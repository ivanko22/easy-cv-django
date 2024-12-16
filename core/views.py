from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework import status
from core.models import CV
from core.serializers import CVSerializer

class CVListCreateAPIView(APIView):
    """API view to list and create CVs."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Only return CVs owned by the logged-in user
        cvs = CV.objects.filter(user=request.user)
        serializer = CVSerializer(cvs, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Automatically associate the logged-in user with the new CV
        serializer = CVSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # Save with the current user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
from rest_framework.generics import RetrieveUpdateDestroyAPIView

class CVDetailAPIView(RetrieveUpdateDestroyAPIView):
    """API view to retrieve, update, or delete a single CV."""
    queryset = CV.objects.all()
    serializer_class = CVSerializer
    permission_classes = [IsAuthenticated]
