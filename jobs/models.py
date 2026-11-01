import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.utils import timezone


class User(AbstractUser):
    ROLE_CHOICES = (
        ('candidate', 'Candidate'),
        ('employer', 'Employer'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='candidate')

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    @property
    def is_candidate(self):
        return self.role == 'candidate'

    @property
    def is_employer(self):
        return self.role == 'employer' or self.is_superuser


class CandidateProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='candidate_profile')
    phone = models.CharField(max_length=30, blank=True)
    headline = models.CharField(max_length=255, blank=True, help_text="e.g. Senior Full-Stack Python Developer")
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=120, blank=True)
    skills = models.CharField(max_length=350, blank=True, help_text="Comma-separated skills e.g. Python, Django, Tailwind CSS, JavaScript")
    experience_years = models.PositiveIntegerField(default=0)
    education = models.CharField(max_length=200, blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    website = models.URLField(blank=True)
    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Candidate Profile: {self.user.get_full_name() or self.user.username}"

    @property
    def skills_list(self):
        if not self.skills:
            return []
        return [s.strip() for s in self.skills.split(',') if s.strip()]


class CompanyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company_profile')
    name = models.CharField(max_length=160, unique=True)
    slug = models.SlugField(max_length=180, unique=True, blank=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=120, default='Remote')
    industry = models.CharField(max_length=100, default='Technology')
    size = models.CharField(max_length=60, default='50-200 Employees')
    about = models.TextField(blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=30, blank=True)
    founded_year = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Company Profiles'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name) or "company"
            candidate_slug = base_slug
            counter = 1
            while CompanyProfile.objects.filter(slug=candidate_slug).exclude(pk=self.pk).exists():
                candidate_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = candidate_slug
        super().save(*args, **kwargs)

    @property
    def active_jobs_count(self):
        return self.jobs.filter(is_active=True).count()


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    icon = models.CharField(max_length=60, default='briefcase')
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def active_jobs_count(self):
        return self.jobs.filter(is_active=True).count()


class Job(models.Model):
    JOB_TYPES = (
        ('Full-time', 'Full-time'),
        ('Part-time', 'Part-time'),
        ('Remote', 'Remote'),
        ('Contract', 'Contract'),
        ('Internship', 'Internship'),
    )

    EXPERIENCE_LEVELS = (
        ('Entry', 'Entry Level (0-2 yrs)'),
        ('Mid', 'Mid Level (2-5 yrs)'),
        ('Senior', 'Senior Level (5+ yrs)'),
        ('Lead', 'Lead / Principal'),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=240, unique=True, blank=True)
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, related_name='jobs')
    employer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_jobs')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='jobs')
    job_type = models.CharField(max_length=30, choices=JOB_TYPES, default='Full-time')
    experience_level = models.CharField(max_length=30, choices=EXPERIENCE_LEVELS, default='Mid')
    location = models.CharField(max_length=150, default='Remote')
    is_remote = models.BooleanField(default=False)
    
    salary_min = models.PositiveIntegerField(null=True, blank=True)
    salary_max = models.PositiveIntegerField(null=True, blank=True)
    salary_currency = models.CharField(max_length=10, default='USD')
    salary_negotiable = models.BooleanField(default=False)
    
    description = models.TextField(help_text="Role overview, team summary, and impact")
    requirements = models.TextField(help_text="Key technical qualifications and competencies")
    responsibilities = models.TextField(blank=True, help_text="Day-to-day duties")
    benefits = models.TextField(blank=True, help_text="Compensation perks, health coverage, PTO")
    skills_required = models.CharField(max_length=300, blank=True, help_text="Comma-separated skills e.g. Django, Python, Tailwind CSS")
    
    open_positions = models.PositiveIntegerField(default=1)
    deadline = models.DateField(null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    views_count = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} at {self.company.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.company.name}-{self.title}") or "job"
            unique_suffix = str(uuid.uuid4())[:6]
            self.slug = f"{base_slug}-{unique_suffix}"
        super().save(*args, **kwargs)

    @property
    def skills_list(self):
        if not self.skills_required:
            return []
        return [s.strip() for s in self.skills_required.split(',') if s.strip()]

    @property
    def formatted_salary(self):
        if self.salary_negotiable and not (self.salary_min or self.salary_max):
            return "Negotiable"
        if self.salary_min and self.salary_max:
            return f"${self.salary_min:,} - ${self.salary_max:,} / yr"
        if self.salary_min:
            return f"From ${self.salary_min:,} / yr"
        if self.salary_max:
            return f"Up to ${self.salary_max:,} / yr"
        return "Competitive"

    @property
    def days_remaining(self):
        if not self.deadline:
            return None
        delta = self.deadline - timezone.now().date()
        return max(0, delta.days)

    @property
    def applications_count(self):
        return self.applications.count()


class JobApplication(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Shortlisted', 'Shortlisted'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    )

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    candidate = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    full_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    cover_letter = models.TextField(blank=True)
    portfolio_url = models.URLField(blank=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Pending')
    employer_notes = models.TextField(blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-applied_at']
        unique_together = ('job', 'candidate')

    def __str__(self):
        return f"{self.full_name} -> {self.job.title} ({self.status})"


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Contact from {self.name}: {self.subject}"
