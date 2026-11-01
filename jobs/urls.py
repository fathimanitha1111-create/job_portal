from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('jobs/', views.all_jobs_view, name='all_jobs'),
    path('jobs/post/', views.post_job_view, name='post_job'),
    path('jobs/<slug:slug>/', views.job_details_view, name='job_details'),
    path('jobs/<slug:slug>/apply/', views.apply_job_view, name='apply_job'),
    path('jobs/<slug:slug>/edit/', views.edit_job_view, name='edit_job'),
    path('jobs/<slug:slug>/delete/', views.delete_job_view, name='delete_job'),

    # Candidate Authentication & Dashboard
    path('candidate/register/', views.candidate_register_view, name='candidate_register'),
    path('candidate/login/', views.candidate_login_view, name='candidate_login'),
    path('candidate/dashboard/', views.candidate_dashboard_view, name='candidate_dashboard'),
    path('my-applications/', views.my_applications_view, name='my_applications'),

    # Employer Authentication & Dashboard
    path('employer/register/', views.employer_register_view, name='employer_register'),
    path('employer/login/', views.employer_login_view, name='employer_login'),
    path('employer/dashboard/', views.employer_dashboard_view, name='employer_dashboard'),
    path('applications/<int:app_id>/status/', views.update_application_status_view, name='update_application_status'),

    # Common Auth
    path('logout/', views.logout_view, name='logout'),

    # Informational Pages
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
]
