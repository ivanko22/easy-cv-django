from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework import status
from api.models import CV
from api.serializers import CVSerializer

from rest_framework.response import Response
from django.contrib.auth.models import User

class SignUpView(APIView):
    permission_classes = [AllowAny]  # Allow access without authentication

    """
    Handles user registration without server-side validation,
    as Vue handles input validation.
    """
    def post(self, request):
        # Extract data
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        email = request.data.get("email")
        password = request.data.get("password")

        # Validate required fields
        if not all([first_name, last_name, email, password]):
            return Response(
                {"error": "All fields (first_name, last_name, email, password) are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if email is already registered
        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        # Create user
        try:
            user = User.objects.create_user(
                username=email,  # Use email as username
                email=email,
                password=password,  # Automatically hashed by create_user
                first_name=first_name,
                last_name=last_name
            )
        except Exception as e:
            return Response(
                {"error": f"Failed to create user: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)

class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        
        if not refresh_token:
            return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Invalid token or logout failed"}, status=status.HTTP_400_BAD_REQUEST)

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
    

class CVDetailAPIView(RetrieveUpdateDestroyAPIView):
    """API view to retrieve, update, or delete a single CV."""
    queryset = CV.objects.all()
    serializer_class = CVSerializer
    permission_classes = [IsAuthenticated]
