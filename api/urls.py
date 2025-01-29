from django.urls import path
from api.views import (
    EmploymentListCreateView,
    EmploymentDetailUpdateView,
    CVListCreateAPIView,
    CVDetailAPIView,
    SignUpView,
    LogoutView,
    SocialCreateAPIView,
)

urlpatterns = [
    path('cv/', CVListCreateAPIView.as_view(), name='cv-list-create'),
    path('socials/', SocialCreateAPIView.as_view(), name='social-list'),

    # Employment routes
    path('user/employment', EmploymentListCreateView.as_view(), name='employment-list-create'),
    path('user/employment/<int:pk>/', EmploymentDetailUpdateView.as_view(), name='employment-detail-update'),

    path('sign-up/', SignUpView.as_view(), name='sign-up'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
