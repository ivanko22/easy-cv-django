from django.urls import path
from core.views import CVListCreateAPIView, CVDetailAPIView

urlpatterns = [
    path('cvs/', CVListCreateAPIView.as_view(), name='cv-list-create'),
    path('cvs/<int:pk>/', CVDetailAPIView.as_view(), name='cv-detail'),
]
