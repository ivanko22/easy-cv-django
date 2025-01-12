from django.urls import path
from api.views import CVListCreateAPIView, CVDetailAPIView, SignUpView, LogoutView

urlpatterns = [
    path('cvs/', CVListCreateAPIView.as_view(), name='cv-list-create'),
    path('cvs/<int:pk>/', CVDetailAPIView.as_view(), name='cv-detail'),
    path('sign-up/', SignUpView.as_view(), name='sign-up'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
