from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, CandidateProfile, CompanyProfile, Category, Job, JobApplication, ContactMessage


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Role Information', {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role Information', {'fields': ('role',)}),
    )


@admin.register(CandidateProfile)
class CandidateProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'headline', 'location', 'experience_years', 'created_at')
    search_fields = ('user__username', 'user__email', 'headline', 'skills')


@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'industry', 'location', 'size', 'active_jobs_count', 'created_at')
    search_fields = ('name', 'industry', 'location')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'active_jobs_count')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'category', 'job_type', 'experience_level', 'location', 'is_remote', 'is_featured', 'is_active', 'created_at')
    list_filter = ('job_type', 'experience_level', 'is_remote', 'is_featured', 'is_active', 'category')
    search_fields = ('title', 'description', 'company__name', 'skills_required')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_featured', 'is_active')


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'job', 'status', 'applied_at')
    list_filter = ('status', 'applied_at')
    search_fields = ('full_name', 'email', 'job__title', 'candidate__username')
    list_editable = ('status',)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
