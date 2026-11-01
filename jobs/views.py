from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import HttpResponseForbidden

from .models import User, CandidateProfile, CompanyProfile, Category, Job, JobApplication, ContactMessage
from .forms import (
    CandidateRegistrationForm, EmployerRegistrationForm, CustomAuthenticationForm,
    JobPostForm, JobApplicationForm, ContactForm,
    CandidateProfileForm, CompanyProfileForm
)


def home_view(request):
    featured_jobs = Job.objects.filter(is_active=True, is_featured=True).select_related('company', 'category')[:6]
    recent_jobs = Job.objects.filter(is_active=True).select_related('company', 'category')[:6]
    categories = Category.objects.annotate(active_jobs=Count('jobs', filter=Q(jobs__is_active=True))).order_by('-active_jobs')[:8]
    companies = CompanyProfile.objects.annotate(active_jobs=Count('jobs', filter=Q(jobs__is_active=True))).order_by('-active_jobs')[:6]

    context = {
        'featured_jobs': featured_jobs,
        'recent_jobs': recent_jobs,
        'categories': categories,
        'companies': companies,
    }
    return render(request, 'jobs/home.html', context)


def all_jobs_view(request):
    jobs = Job.objects.filter(is_active=True).select_related('company', 'category')

    query = request.GET.get('q', '').strip()
    location = request.GET.get('location', '').strip()
    category_slug = request.GET.get('category', '').strip()
    job_type = request.GET.get('type', '').strip()
    is_remote = request.GET.get('remote', '').strip()
    min_salary = request.GET.get('min_salary', '').strip()
    sort_by = request.GET.get('sort', 'newest').strip()

    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(skills_required__icontains=query) |
            Q(company__name__icontains=query)
        )

    if location:
        jobs = jobs.filter(location__icontains=location)

    if category_slug:
        jobs = jobs.filter(category__slug=category_slug)

    if job_type:
        jobs = jobs.filter(job_type=job_type)

    if is_remote == '1' or is_remote.lower() == 'true':
        jobs = jobs.filter(is_remote=True)

    if min_salary and min_salary.isdigit():
        jobs = jobs.filter(salary_max__gte=int(min_salary))

    if sort_by == 'salary_high':
        jobs = jobs.order_by('-salary_max', '-salary_min', '-created_at')
    elif sort_by == 'popular':
        jobs = jobs.order_by('-views_count', '-created_at')
    elif sort_by == 'oldest':
        jobs = jobs.order_by('created_at')
    else:
        jobs = jobs.order_by('-is_featured', '-created_at')

    total_count = jobs.count()

    paginator = Paginator(jobs, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    all_categories = Category.objects.all()

    context = {
        'page_obj': page_obj,
        'total_count': total_count,
        'all_categories': all_categories,
        'query': query,
        'selected_location': location,
        'selected_category': category_slug,
        'selected_type': job_type,
        'selected_remote': is_remote,
        'selected_min_salary': min_salary,
        'selected_sort': sort_by,
        'job_types': Job.JOB_TYPES,
    }
    return render(request, 'jobs/all_jobs.html', context)


def job_details_view(request, slug):
    job = get_object_or_404(Job.objects.select_related('company', 'category', 'employer'), slug=slug)

    # Increment view count
    Job.objects.filter(pk=job.pk).update(views_count=job.views_count + 1)
    job.refresh_from_db(fields=['views_count'])

    has_applied = False
    existing_application = None

    if request.user.is_authenticated and request.user.is_candidate:
        existing_application = JobApplication.objects.filter(job=job, candidate=request.user).first()
        has_applied = existing_application is not None

    related_jobs = Job.objects.filter(
        category=job.category,
        is_active=True
    ).exclude(id=job.id).select_related('company')[:3]

    # Pre-fill form if candidate profile exists
    initial_data = {}
    if request.user.is_authenticated and request.user.is_candidate:
        profile = getattr(request.user, 'candidate_profile', None)
        initial_data = {
            'full_name': request.user.get_full_name() or request.user.username,
            'email': request.user.email,
            'phone': profile.phone if profile else '',
            'portfolio_url': profile.website if profile else '',
        }

    apply_form = JobApplicationForm(initial=initial_data)

    context = {
        'job': job,
        'has_applied': has_applied,
        'existing_application': existing_application,
        'related_jobs': related_jobs,
        'apply_form': apply_form,
    }
    return render(request, 'jobs/job_details.html', context)


@login_required
def apply_job_view(request, slug):
    job = get_object_or_404(Job, slug=slug, is_active=True)

    if not request.user.is_candidate and not request.user.is_superuser:
        messages.warning(request, "Only candidate accounts can submit job applications. Please sign in as a candidate.")
        return redirect('job_details', slug=slug)

    # Prevent duplicate applications
    if JobApplication.objects.filter(job=job, candidate=request.user).exists():
        messages.info(request, "You have already applied for this position.")
        return redirect('my_applications')

    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.candidate = request.user
            application.status = 'Pending'
            if not application.resume and hasattr(request.user, 'candidate_profile') and request.user.candidate_profile.resume:
                application.resume = request.user.candidate_profile.resume
            application.save()

            messages.success(request, f"Your application for '{job.title}' has been submitted successfully!")
            return redirect('my_applications')
        else:
            for field, errs in form.errors.items():
                for err in errs:
                    messages.error(request, f"{field.capitalize()}: {err}")
            return redirect('job_details', slug=slug)

    return redirect('job_details', slug=slug)


# Auth Views
def candidate_register_view(request):
    if request.user.is_authenticated:
        return redirect('candidate_dashboard' if request.user.is_candidate else 'employer_dashboard')

    if request.method == 'POST':
        form = CandidateRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to CareerConnect, {user.first_name or user.username}! Your candidate account is created.")
            return redirect('candidate_dashboard')
    else:
        form = CandidateRegistrationForm()

    return render(request, 'jobs/candidate_register.html', {'form': form})


def candidate_login_view(request):
    if request.user.is_authenticated:
        return redirect('candidate_dashboard' if request.user.is_candidate else 'employer_dashboard')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name or user.username}!")
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('candidate_dashboard' if user.is_candidate else 'employer_dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = CustomAuthenticationForm()

    return render(request, 'jobs/candidate_login.html', {'form': form})


def employer_register_view(request):
    if request.user.is_authenticated:
        return redirect('employer_dashboard' if request.user.is_employer else 'candidate_dashboard')

    if request.method == 'POST':
        form = EmployerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to CareerConnect! Your employer account is ready to post jobs.")
            return redirect('employer_dashboard')
    else:
        form = EmployerRegistrationForm()

    return render(request, 'jobs/employer_register.html', {'form': form})


def employer_login_view(request):
    if request.user.is_authenticated:
        return redirect('employer_dashboard' if request.user.is_employer else 'candidate_dashboard')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name or user.username}!")
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('employer_dashboard' if user.is_employer else 'candidate_dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = CustomAuthenticationForm()

    return render(request, 'jobs/employer_login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('home')


# Dashboards
@login_required
def candidate_dashboard_view(request):
    if not request.user.is_candidate and not request.user.is_superuser:
        messages.warning(request, "Redirected to employer dashboard.")
        return redirect('employer_dashboard')

    profile, _ = CandidateProfile.objects.get_or_create(user=request.user)
    applications = JobApplication.objects.filter(candidate=request.user).select_related('job', 'job__company').order_by('-applied_at')

    if request.method == 'POST':
        profile_form = CandidateProfileForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('candidate_dashboard')
    else:
        profile_form = CandidateProfileForm(instance=profile)

    context = {
        'profile': profile,
        'profile_form': profile_form,
        'applications': applications[:5],
        'total_applications_count': applications.count(),
        'pending_count': applications.filter(status='Pending').count(),
        'shortlisted_count': applications.filter(status='Shortlisted').count(),
        'accepted_count': applications.filter(status='Accepted').count(),
    }
    return render(request, 'jobs/candidate_dashboard.html', context)


@login_required
def my_applications_view(request):
    if not request.user.is_candidate and not request.user.is_superuser:
        return redirect('employer_dashboard')

    status_filter = request.GET.get('status', '').strip()
    applications = JobApplication.objects.filter(candidate=request.user).select_related('job', 'job__company').order_by('-applied_at')

    if status_filter:
        applications = applications.filter(status=status_filter)

    context = {
        'applications': applications,
        'status_filter': status_filter,
        'status_choices': JobApplication.STATUS_CHOICES,
        'total_count': JobApplication.objects.filter(candidate=request.user).count(),
    }
    return render(request, 'jobs/my_applications.html', context)


@login_required
def employer_dashboard_view(request):
    if not request.user.is_employer:
        messages.warning(request, "Access restricted to employer accounts.")
        return redirect('candidate_dashboard')

    company = getattr(request.user, 'company_profile', None)
    if not company:
        company = CompanyProfile.objects.create(
            user=request.user,
            name=f"{request.user.first_name or request.user.username}'s Company"
        )

    posted_jobs = Job.objects.filter(employer=request.user).select_related('category').annotate(
        apps_count=Count('applications')
    ).order_by('-created_at')

    all_applications = JobApplication.objects.filter(job__employer=request.user).select_related('job', 'candidate').order_by('-applied_at')

    # Status filter for applicants
    status_filter = request.GET.get('status', '').strip()
    job_filter = request.GET.get('job_id', '').strip()

    filtered_applications = all_applications
    if status_filter:
        filtered_applications = filtered_applications.filter(status=status_filter)
    if job_filter and job_filter.isdigit():
        filtered_applications = filtered_applications.filter(job_id=int(job_filter))

    if request.method == 'POST' and 'update_company' in request.POST:
        company_form = CompanyProfileForm(request.POST, request.FILES, instance=company)
        if company_form.is_valid():
            company_form.save()
            messages.success(request, "Company profile updated successfully!")
            return redirect('employer_dashboard')
    else:
        company_form = CompanyProfileForm(instance=company)

    context = {
        'company': company,
        'company_form': company_form,
        'posted_jobs': posted_jobs,
        'total_jobs_count': posted_jobs.count(),
        'total_applications_count': all_applications.count(),
        'shortlisted_count': all_applications.filter(status='Shortlisted').count(),
        'accepted_count': all_applications.filter(status='Accepted').count(),
        'applications': filtered_applications[:15],
        'status_filter': status_filter,
        'job_filter': job_filter,
        'status_choices': JobApplication.STATUS_CHOICES,
    }
    return render(request, 'jobs/employer_dashboard.html', context)


@login_required
def update_application_status_view(request, app_id):
    application = get_object_or_404(JobApplication, id=app_id, job__employer=request.user)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        notes = request.POST.get('employer_notes', '')

        if new_status in dict(JobApplication.STATUS_CHOICES):
            application.status = new_status
            application.employer_notes = notes
            application.save()
            messages.success(request, f"Updated status for {application.full_name} to {new_status}.")

    return redirect('employer_dashboard')


@login_required
def post_job_view(request):
    if not request.user.is_employer:
        messages.error(request, "Only employers can post jobs. Please register or sign in as an employer.")
        return redirect('employer_login')

    company = getattr(request.user, 'company_profile', None)
    if not company:
        company = CompanyProfile.objects.create(
            user=request.user,
            name=f"{request.user.first_name or request.user.username}'s Company"
        )

    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.company = company
            job.employer = request.user
            job.save()
            messages.success(request, f"Job listing '{job.title}' posted successfully!")
            return redirect('job_details', slug=job.slug)
    else:
        form = JobPostForm()

    context = {
        'form': form,
        'company': company,
        'page_title': 'Post a New Job Opening',
    }
    return render(request, 'jobs/post_job.html', context)


@login_required
def edit_job_view(request, slug):
    job = get_object_or_404(Job, slug=slug, employer=request.user)

    if request.method == 'POST':
        form = JobPostForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, f"Job listing '{job.title}' updated successfully!")
            return redirect('job_details', slug=job.slug)
    else:
        form = JobPostForm(instance=job)

    context = {
        'form': form,
        'job': job,
        'company': job.company,
        'page_title': f"Edit Job: {job.title}",
    }
    return render(request, 'jobs/edit_job.html', context)


@login_required
def delete_job_view(request, slug):
    job = get_object_or_404(Job, slug=slug, employer=request.user)

    if request.method == 'POST':
        title = job.title
        job.delete()
        messages.success(request, f"Job '{title}' has been deleted successfully.")
        return redirect('employer_dashboard')

    return render(request, 'jobs/employer_dashboard.html')


def about_view(request):
    return render(request, 'jobs/about.html')


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you! Your message has been received. Our team will contact you shortly.")
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'jobs/contact.html', {'form': form})


def custom_404_view(request, exception=None):
    return render(request, 'jobs/404.html', status=404)
