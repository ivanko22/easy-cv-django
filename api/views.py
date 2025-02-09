from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework import status
from api.models import CV, Employment, Social
from api.serializers import CVSerializer, EmploymentSerializer, SocialSerializer

from rest_framework.response import Response
from django.contrib.auth.models import User

class SignUpView(APIView):
    permission_classes = [AllowAny]  # Allow access without authentication

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

            # Generate tokens
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token

            return Response(
                {
                    "message": "User created successfully.",
                    "tokens": {
                        "access": str(access),
                        "refresh": str(refresh),
                    }
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return Response(
                {"error": f"Failed to create user: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        
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

class EmploymentListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]

    def get(self, request):
        jobs = Employment.objects.filter(user=request.user)
        serializer = EmploymentSerializer(jobs, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        serializer = EmploymentSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class EmploymentDetailUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]

    def patch(self, request, pk):
        try:
            employment = Employment.objects.get(pk=pk, user=request.user)
        except Employment.DoesNotExist:
            return Response({"error": "Employment record not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = EmploymentSerializer(employment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            employment = Employment.objects.get(pk=pk, user=request.user)
        except Employment.DoesNotExist:
            return Response({"error": "Employment record not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = EmploymentSerializer(employment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        try:
            employment = Employment.objects.get(pk=pk, user=request.user)
            employment.delete()
            return Response({"message": "Employment record deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Employment.DoesNotExist:
            return Response({"error": "Employment record not found"}, status=status.HTTP_404_NOT_FOUND)
    
class CVListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Fetch the single CV for the user, or return an empty list if none exist
        cv = CV.objects.filter(user=request.user).first()
        if cv:
            serializer = CVSerializer(cv)
            return Response(serializer.data)
        return Response({"message": "No CV found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        print("Request Data (Post):", request.data)

        # Ensure that there is only one CV per user
        CV.objects.filter(user=request.user).delete()

        serializer = CVSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            cv = serializer.save()
            print(f"CV Created: {cv}, Work History: {cv.work_history.all()}")  # Debugging
            return Response(CVSerializer(cv).data, status=status.HTTP_201_CREATED)
        
        print("Errors:", serializer.errors)  # Debugging validation issues
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CVDetailAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CVSerializer
    queryset = CV.objects.all()

    def get_queryset(self):
        return CV.objects.filter(user=self.request.user)

PREDEFINED_SOCIALS = [
    {"name": "+ Cell", "link": "+ Cell"},
    {"name": "+ Portfolio", "link": "+ Portfolio"},
    {"name": "+ Linkedin", "link": "+ Linkedin"},
    {"name": "+ Location", "link": "+ Location"},
    {"name": "+ Github", "link": "+ Github"},
    {"name": "+ Other", "link": "+ Other"},
]

class SocialCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve all predefined socials for the user, initializing them if not already present.
        """
        user = request.user

        # Ensure predefined socials exist for the user
        for social in PREDEFINED_SOCIALS:
            Social.objects.get_or_create(user=user, name=social["name"], defaults={"link": social["link"]})

        # Retrieve user's socials and convert QuerySet to a list
        socials = list(Social.objects.filter(user=user))
        
        # Sort by predefined order
        name_order = {social["name"]: index for index, social in enumerate(PREDEFINED_SOCIALS)}
        socials.sort(key=lambda s: name_order.get(s.name, float("inf")))  # Use inf to push unknown names to the end
        serializer = SocialSerializer(socials, many=True)
        
        return Response(serializer.data)

    def post(self, request):
        """
        Update the link for a specific social.
        """
        social_name = request.data.get("name")
        link = request.data.get("link")

        if not social_name or not link:
            return Response({"error": "Both 'name' and 'link' are required."}, status=400)

        try:
            # Update the specific social link for the user
            social = Social.objects.get(user=request.user, name=social_name)
            social.link = link
            social.save()
            serializer = SocialSerializer(social)
            return Response(serializer.data, status=200)
        except Social.DoesNotExist:
            return Response({"error": f"Social with name '{social_name}' not found for the user."}, status=404)
        