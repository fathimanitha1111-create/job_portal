from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, CandidateProfile, CompanyProfile, Job, JobApplication, ContactMessage, Category


class CandidateRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=60, required=True, widget=forms.TextInput(attrs={
        'class': 'form-input', 'placeholder': 'First Name'
    }))
    last_name = forms.CharField(max_length=60, required=True, widget=forms.TextInput(attrs={
        'class': 'form-input', 'placeholder': 'Last Name'
    }))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-input', 'placeholder': 'name@example.com'
    }))
    headline = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={
        'class': 'form-input', 'placeholder': 'e.g. Senior Full-Stack Python Developer'
    }))
    skills = forms.CharField(max_length=350, required=False, widget=forms.TextInput(attrs={
        'class': 'form-input', 'placeholder': 'Python, Django, Tailwind CSS, JavaScript'
    }))
    phone = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={
        'class': 'form-input', 'placeholder': '+1 (555) 000-0000'
    }))
    resume = forms.FileField(required=False, widget=forms.FileInput(attrs={
        'class': 'form-file', 'accept': '.pdf,.doc,.docx'
    }))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-input'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email address already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'candidate'
        if commit:
            user.save()
            CandidateProfile.objects.create(
                user=user,
                phone=self.cleaned_data.get('phone', ''),
                headline=self.cleaned_data.get('headline', ''),
                skills=self.cleaned_data.get('skills', ''),
                resume=self.cleaned_data.get('resume'),
            )
        return user


class EmployerRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=60, required=True, widget=forms.TextInput(attrs={
        'class': 'form-input', 'placeholder': 'Hiring Contact First Name'
    }))
    last_name = forms.CharField(max_length=60, required=True, widget=forms.TextInput(attrs={
        'class': 'form-input', 'placeholder': 'Hiring Contact Last Name'
    }))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-input', 'placeholder': 'recruiter@company.com'
    }))
    company_name = forms.CharField(max_length=160, required=True, widget=forms.TextInput(attrs={
        'class': 'form-input', 'placeholder': 'Company or Organization Name'
    }))
    company_industry = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'class': 'form-input', 'placeholder': 'e.g. Software, Fintech, Healthcare'
    }))
    company_location = forms.CharField(max_length=120, required=False, widget=forms.TextInput(attrs={
        'class': 'form-input', 'placeholder': 'City, State or Remote'
    }))
    company_website = forms.URLField(required=False, widget=forms.URLInput(attrs={
        'class': 'form-input', 'placeholder': 'https://yourcompany.com'
    }))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-input'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email address already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'employer'
        if commit:
            user.save()
            CompanyProfile.objects.create(
                user=user,
                name=self.cleaned_data['company_name'],
                industry=self.cleaned_data.get('company_industry', 'Technology'),
                location=self.cleaned_data.get('company_location', 'Remote'),
                website=self.cleaned_data.get('company_website', ''),
                contact_email=user.email,
            )
        return user


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-input'


class JobPostForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = (
            'title', 'category', 'job_type', 'experience_level', 'location', 'is_remote',
            'salary_min', 'salary_max', 'salary_currency', 'salary_negotiable',
            'skills_required', 'open_positions', 'deadline',
            'description', 'requirements', 'responsibilities', 'benefits',
            'is_featured', 'is_active'
        )
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Senior Backend Python Developer'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'job_type': forms.Select(attrs={'class': 'form-select'}),
            'experience_level': forms.Select(attrs={'class': 'form-select'}),
            'location': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. New York, NY / Remote'}),
            'is_remote': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'salary_min': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'e.g. 100000'}),
            'salary_max': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'e.g. 140000'}),
            'salary_currency': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'USD'}),
            'salary_negotiable': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'skills_required': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Python, Django, Tailwind CSS, PostgreSQL'}),
            'open_positions': forms.NumberInput(attrs={'class': 'form-input', 'value': 1}),
            'deadline': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4, 'placeholder': 'Overview of the role, team, and impact...'}),
            'requirements': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4, 'placeholder': 'Key requirements, competencies, and qualifications...'}),
            'responsibilities': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'Day-to-day duties and core deliverables...'}),
            'benefits': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'Health benefits, 401(k), paid time off, remote stipend...'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'salary_currency' in self.fields:
            self.fields['salary_currency'].required = False
            self.fields['salary_currency'].initial = 'USD'
        if 'open_positions' in self.fields:
            self.fields['open_positions'].required = False
            self.fields['open_positions'].initial = 1

    def clean_salary_currency(self):
        return self.cleaned_data.get('salary_currency') or 'USD'

    def clean_open_positions(self):
        return self.cleaned_data.get('open_positions') or 1


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ('full_name', 'email', 'phone', 'resume', 'cover_letter', 'portfolio_url')
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'name@example.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '+1 (555) 000-0000'}),
            'portfolio_url': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://github.com/username or LinkedIn'}),
            'resume': forms.FileInput(attrs={'class': 'form-file', 'accept': '.pdf,.doc,.docx'}),
            'cover_letter': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4, 'placeholder': 'Tell the hiring team why you are a great fit for this position...'}),
        }

    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if resume:
            # File size validation (max 5MB)
            if resume.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Resume file size cannot exceed 5MB.")
            # File extension validation
            ext = resume.name.split('.')[-1].lower()
            if ext not in ['pdf', 'doc', 'docx']:
                raise forms.ValidationError("Only PDF, DOC, and DOCX files are allowed.")
        return resume


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ('name', 'email', 'subject', 'message')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'name@example.com'}),
            'subject': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Subject of your message'}),
            'message': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4, 'placeholder': 'How can our team help you?'}),
        }


class CandidateProfileForm(forms.ModelForm):
    class Meta:
        model = CandidateProfile
        fields = ('phone', 'headline', 'bio', 'location', 'skills', 'experience_years', 'education', 'resume', 'avatar', 'website', 'github', 'linkedin')
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-input'}),
            'headline': forms.TextInput(attrs={'class': 'form-input'}),
            'bio': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
            'location': forms.TextInput(attrs={'class': 'form-input'}),
            'skills': forms.TextInput(attrs={'class': 'form-input'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-input'}),
            'education': forms.TextInput(attrs={'class': 'form-input'}),
            'website': forms.URLInput(attrs={'class': 'form-input'}),
            'github': forms.URLInput(attrs={'class': 'form-input'}),
            'linkedin': forms.URLInput(attrs={'class': 'form-input'}),
            'resume': forms.FileInput(attrs={'class': 'form-file'}),
            'avatar': forms.FileInput(attrs={'class': 'form-file'}),
        }


class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = ('name', 'logo', 'website', 'location', 'industry', 'size', 'about', 'contact_email', 'contact_phone', 'founded_year')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'website': forms.URLInput(attrs={'class': 'form-input'}),
            'location': forms.TextInput(attrs={'class': 'form-input'}),
            'industry': forms.TextInput(attrs={'class': 'form-input'}),
            'size': forms.TextInput(attrs={'class': 'form-input'}),
            'about': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-input'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-input'}),
            'founded_year': forms.NumberInput(attrs={'class': 'form-input'}),
            'logo': forms.FileInput(attrs={'class': 'form-file'}),
        }
