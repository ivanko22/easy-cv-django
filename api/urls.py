from django.urls import path
from api.views import (
    EmploymentListCreateView,
    EmploymentDetailUpdateView,
    CVListCreateAPIView,
    CVDetailAPIView,
    SignUpView,
    LogoutView,
)

urlpatterns = [
    path('cv/', CVListCreateAPIView.as_view(), name='cv-list-create'),
    path('cv/<int:pk>/', CVDetailAPIView.as_view(), name='cv-detail'),

    # Employment routes
    path('user/employment', EmploymentListCreateView.as_view(), name='employment-list-create'),
    path('user/employment/<int:pk>/', EmploymentDetailUpdateView.as_view(), name='employment-detail-update'),

    path('sign-up/', SignUpView.as_view(), name='sign-up'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
