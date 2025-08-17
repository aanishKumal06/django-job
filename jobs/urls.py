from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.JobListView.as_view(), name='job_list'),
    path('my-jobs/', views.MyJobListView.as_view(), name='job_my_list'),
    path('create/', views.JobCreateView.as_view(), name='job_create'),
    path('<int:pk>/', views.JobDetailView.as_view(), name='job_detail'),
    path('<int:pk>/update/', views.JobUpdateView.as_view(), name='job_update'),
    path('<int:pk>/delete/', views.JobDeleteView.as_view(), name='job_delete'),
]
