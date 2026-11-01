from django.test import TestCase
from django.urls import reverse
from .models import User, CompanyProfile, CandidateProfile, Category, Job, JobApplication, ContactMessage


class CareerConnectTests(TestCase):
    def setUp(self):
        # Create candidate user
        self.candidate_user = User.objects.create_user(
            username='testcandidate',
            email='candidate@test.com',
            password='testpassword123',
            role='candidate'
        )
        self.candidate_profile = CandidateProfile.objects.create(
            user=self.candidate_user,
            headline='Software Engineer'
        )

        # Create employer user
        self.employer_user = User.objects.create_user(
            username='testemployer',
            email='employer@test.com',
            password='testpassword123',
            role='employer'
        )
        self.company = CompanyProfile.objects.create(
            user=self.employer_user,
            name='Test Innovations Inc',
            location='Kochi, Kerala'
        )

        # Create category and job
        self.category = Category.objects.create(name='Engineering', slug='engineering')
        self.job = Job.objects.create(
            title='Python Full-Stack Engineer',
            company=self.company,
            employer=self.employer_user,
            category=self.category,
            location='Kochi, Kerala',
            job_type='Full-time',
            experience_level='Mid',
            is_remote=True,
            salary_min=100000,
            salary_max=130000,
            description='Test job description content here.',
            requirements='Python, Django, Tailwind CSS, PostgreSQL.'
        )

    def test_home_page_loads(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'CareerConnect')

    def test_all_jobs_page_loads(self):
        response = self.client.get(reverse('all_jobs'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.job.title)

    def test_job_details_page(self):
        response = self.client.get(reverse('job_details', kwargs={'slug': self.job.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.job.title)

    def test_job_search_and_filter(self):
        # Filter by keyword
        response = self.client.get(reverse('all_jobs') + '?q=Python')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.job.title)

        # Filter by non-matching keyword
        response_empty = self.client.get(reverse('all_jobs') + '?q=NonExistentJobRole123')
        self.assertEqual(response_empty.status_code, 200)
        self.assertContains(response_empty, 'No Matching Jobs Found')

    def test_candidate_duplicate_application_prevention(self):
        self.client.login(username='testcandidate', password='testpassword123')
        # Create first application
        JobApplication.objects.create(
            job=self.job,
            candidate=self.candidate_user,
            full_name='Test Candidate',
            email='candidate@test.com',
            phone='1234567890'
        )
        # Attempt to apply again
        response = self.client.post(reverse('apply_job', kwargs={'slug': self.job.slug}), {
            'full_name': 'Test Candidate',
            'email': 'candidate@test.com',
            'phone': '1234567890',
        })
        # Should redirect to my_applications
        self.assertRedirects(response, reverse('my_applications'))
        # Total applications should still be 1
        self.assertEqual(JobApplication.objects.filter(job=self.job, candidate=self.candidate_user).count(), 1)

    def test_employer_post_job(self):
        self.client.login(username='testemployer', password='testpassword123')
        response = self.client.post(reverse('post_job'), {
            'title': 'Senior DevOps Engineer',
            'category': self.category.id,
            'job_type': 'Full-time',
            'location': 'Bangalore / Remote',
            'is_remote': True,
            'salary_min': 150000,
            'salary_max': 200000,
            'experience_level': 'Senior',
            'description': 'Leading cloud infrastructure with Docker and Kubernetes.',
            'requirements': 'AWS, Terraform, CI/CD pipelines.',
            'is_active': True,
        })
        self.assertEqual(response.status_code, 302)
        created_job = Job.objects.filter(title='Senior DevOps Engineer').first()
        self.assertIsNotNone(created_job)
        self.assertEqual(created_job.employer, self.employer_user)

    def test_candidate_cannot_post_job(self):
        self.client.login(username='testcandidate', password='testpassword123')
        response = self.client.get(reverse('post_job'))
        # Should redirect away because user is not employer
        self.assertEqual(response.status_code, 302)

    def test_employer_edit_job(self):
        self.client.login(username='testemployer', password='testpassword123')
        response = self.client.post(reverse('edit_job', kwargs={'slug': self.job.slug}), {
            'title': 'Lead Python Architect',
            'category': self.category.id,
            'job_type': 'Full-time',
            'location': 'Kochi, Kerala',
            'is_remote': True,
            'salary_min': 120000,
            'salary_max': 160000,
            'experience_level': 'Lead',
            'description': 'Updated job description with high standards.',
            'requirements': 'Python, Django, Microservices.',
            'is_active': True,
        })
        self.assertEqual(response.status_code, 302)
        self.job.refresh_from_db()
        self.assertEqual(self.job.title, 'Lead Python Architect')

    def test_employer_delete_job(self):
        self.client.login(username='testemployer', password='testpassword123')
        response = self.client.post(reverse('delete_job', kwargs={'slug': self.job.slug}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Job.objects.filter(id=self.job.id).exists())

    def test_employer_update_application_status(self):
        self.client.login(username='testemployer', password='testpassword123')
        application = JobApplication.objects.create(
            job=self.job,
            candidate=self.candidate_user,
            full_name='Test Candidate',
            email='candidate@test.com',
            phone='1234567890',
            status='Pending'
        )
        response = self.client.post(reverse('update_application_status', kwargs={'app_id': application.id}), {
            'status': 'Shortlisted',
            'employer_notes': 'Great profile, invited for initial interview.'
        })
        self.assertEqual(response.status_code, 302)
        application.refresh_from_db()
        self.assertEqual(application.status, 'Shortlisted')
        self.assertEqual(application.employer_notes, 'Great profile, invited for initial interview.')

    def test_contact_form_submission(self):
        response = self.client.post(reverse('contact'), {
            'name': 'Priya Nair',
            'email': 'priya@example.com',
            'subject': 'Inquiry regarding employer features',
            'message': 'Hello, I would like more information on job postings.'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ContactMessage.objects.filter(email='priya@example.com').count(), 1)
