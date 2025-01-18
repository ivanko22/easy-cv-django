from django.urls import path
from api.views import CVListCreateAPIView, CVDetailAPIView, SignUpView, LogoutView, EmploymentCreateView

urlpatterns = [
    path('cv/', CVListCreateAPIView.as_view(), name='cv-list-create'),
    path('cv/<int:pk>/', CVDetailAPIView.as_view(), name='cv-detail'),
    path('user/employment', EmploymentCreateView.as_view(), name='employment'),
    path('sign-up/', SignUpView.as_view(), name='sign-up'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
