import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
from jobs.models import CandidateProfile, CompanyProfile, Category, Job, JobApplication

User = get_user_model()


class Command(BaseCommand):
    help = 'Seeds database with realistic CareerConnect categories, employers, candidates, and job postings'

    def handle(self, *args, **options):
        self.stdout.write("Seeding CareerConnect database...")

        # 1. Admin Superuser
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@careerconnect.com',
                'first_name': 'System',
                'last_name': 'Admin',
                'is_staff': True,
                'is_superuser': True,
                'role': 'employer',
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("Created admin: admin / admin123"))

        # 2. Employer 1 (TechCorp)
        employer_user1, created = User.objects.get_or_create(
            username='employer',
            defaults={
                'email': 'recruiting@cloudscale.io',
                'first_name': 'Marcus',
                'last_name': 'Vance',
                'role': 'employer',
            }
        )
        if created:
            employer_user1.set_password('password123')
            employer_user1.save()
            self.stdout.write(self.style.SUCCESS("Created employer: employer / password123"))

        company1, _ = CompanyProfile.objects.get_or_create(
            user=employer_user1,
            defaults={
                'name': 'CloudScale Technologies',
                'website': 'https://cloudscale.io',
                'location': 'San Francisco, CA (Remote)',
                'industry': 'Cloud Infrastructure & SaaS',
                'size': '250-500 Employees',
                'about': 'CloudScale Technologies delivers high-performance managed infrastructure and automated cloud platforms powering modern engineering organizations.',
                'contact_email': 'recruiting@cloudscale.io',
                'contact_phone': '+1 (415) 555-0199',
                'founded_year': 2018,
            }
        )

        # 2b. Employer 2 (Fintech & Design)
        employer_user2, created = User.objects.get_or_create(
            username='techcorp',
            defaults={
                'email': 'careers@finovatech.com',
                'first_name': 'Elena',
                'last_name': 'Rostova',
                'role': 'employer',
            }
        )
        if created:
            employer_user2.set_password('password123')
            employer_user2.save()

        company2, _ = CompanyProfile.objects.get_or_create(
            user=employer_user2,
            defaults={
                'name': 'Finova Global',
                'website': 'https://finovatech.com',
                'location': 'New York, NY (Hybrid)',
                'industry': 'Fintech & Digital Banking',
                'size': '500+ Employees',
                'about': 'Finova Global is a financial technology powerhouse building scalable cross-border payment networks and enterprise banking software.',
                'contact_email': 'careers@finovatech.com',
                'contact_phone': '+1 (212) 555-0144',
                'founded_year': 2016,
            }
        )

        # 3. Candidate (Seeker)
        candidate_user, created = User.objects.get_or_create(
            username='candidate',
            defaults={
                'email': 'david.miller@example.com',
                'first_name': 'David',
                'last_name': 'Miller',
                'role': 'candidate',
            }
        )
        if created:
            candidate_user.set_password('password123')
            candidate_user.save()
            self.stdout.write(self.style.SUCCESS("Created candidate: candidate / password123"))

        candidate_profile, _ = CandidateProfile.objects.get_or_create(
            user=candidate_user,
            defaults={
                'headline': 'Senior Full-Stack Python & React Developer',
                'bio': 'Passionate software engineer with 5+ years of experience building reliable web applications with Python, Django, PostgreSQL, and modern Tailwind CSS.',
                'location': 'Austin, TX (Open to Remote)',
                'skills': 'Python, Django, Tailwind CSS, JavaScript, PostgreSQL, Docker, Git',
                'experience_years': 5,
                'education': 'B.S. in Computer Science',
                'website': 'https://davidmiller.dev',
                'github': 'https://github.com/davidmiller',
                'linkedin': 'https://linkedin.com/in/davidmiller',
                'phone': '+1 (555) 234-5678',
            }
        )

        # 4. Categories
        categories_data = [
            {'name': 'Software Engineering', 'icon': 'code', 'description': 'Backend, Frontend, Full-stack, Mobile, and Cloud engineering'},
            {'name': 'UI/UX & Product Design', 'icon': 'palette', 'description': 'Visual design, Design Systems, UX Research, and Product Prototyping'},
            {'name': 'Data Science & AI', 'icon': 'cpu', 'description': 'Machine Learning, Deep Learning, MLOps, and Analytics'},
            {'name': 'Product & Project Management', 'icon': 'kanban', 'description': 'Technical Product Managers, Agile Coaches, and Delivery Leads'},
            {'name': 'Marketing & Growth', 'icon': 'megaphone', 'description': 'Performance marketing, SEO/SEM, Content, and Brand strategy'},
            {'name': 'Finance & Operations', 'icon': 'chart-pie', 'description': 'Accounting, Financial Planning, Operations, and Business Analysis'},
            {'name': 'Sales & Customer Success', 'icon': 'trending-up', 'description': 'Enterprise Account Executives, BDRs, and Client Success'},
            {'name': 'DevOps & Cybersecurity', 'icon': 'shield-check', 'description': 'Cloud security, Infrastructure-as-code, and SRE'},
        ]

        category_objs = {}
        for cat in categories_data:
            c, _ = Category.objects.get_or_create(
                name=cat['name'],
                defaults={'icon': cat['icon'], 'description': cat['description']}
            )
            category_objs[c.name] = c

        # 5. Jobs
        jobs_data = [
            {
                'title': 'Senior Full-Stack Django & JavaScript Engineer',
                'company': company1,
                'employer': employer_user1,
                'category': category_objs['Software Engineering'],
                'job_type': 'Full-time',
                'experience_level': 'Senior',
                'location': 'Remote (Global)',
                'is_remote': True,
                'salary_min': 125000,
                'salary_max': 160000,
                'is_featured': True,
                'skills_required': 'Python, Django, Tailwind CSS, JavaScript, PostgreSQL, Docker',
                'open_positions': 2,
                'deadline': timezone.now().date() + datetime.timedelta(days=45),
                'description': 'We are looking for a skilled Senior Full-Stack Engineer who enjoys building robust, high-performance web platforms using Python, Django, and modern Tailwind CSS. You will collaborate with cross-functional teams to craft responsive user experiences and scalable server-side systems.',
                'requirements': '• 5+ years of software development experience with Python and Django.\n• Strong mastery of HTML5, CSS3, Tailwind CSS, and vanilla JavaScript.\n• Deep understanding of relational databases and PostgreSQL query tuning.\n• Experience with containerized deployments (Docker) and CI/CD pipelines.\n• Excellent proactive communication skills in a remote work environment.',
                'responsibilities': '• Architect, build, and maintain production-grade Django web applications.\n• Collaborate with product designers to implement clean, pixel-perfect user interfaces.\n• Participate in code reviews, technical design discussions, and system monitoring.\n• Mentor junior and mid-level engineering team members.',
                'benefits': '• 100% Remote flexibility with home office stipend ($1,500)\n• Comprehensive health, dental, and vision insurance\n• 401(k) retirement savings with 5% company matching\n• Unlimited Paid Time Off (PTO)\n• $1,200 annual learning & development budget',
            },
            {
                'title': 'Lead Product Designer (UI/UX)',
                'company': company2,
                'employer': employer_user2,
                'category': category_objs['UI/UX & Product Design'],
                'job_type': 'Full-time',
                'experience_level': 'Lead',
                'location': 'New York, NY (Hybrid)',
                'is_remote': False,
                'salary_min': 115000,
                'salary_max': 150000,
                'is_featured': True,
                'skills_required': 'Figma, Design Systems, Wireframing, UX Research, Mobile UX',
                'open_positions': 1,
                'deadline': timezone.now().date() + datetime.timedelta(days=30),
                'description': 'Finova Global is seeking a Lead Product Designer to lead design initiatives across our web and mobile banking platforms. You will shape design systems, direct user research, and deliver world-class digital experiences.',
                'requirements': '• 6+ years designing complex consumer or enterprise web platforms.\n• Proven mastery of Figma, design systems, and rapid prototyping.\n• Demonstrated track record conducting qualitative and quantitative user research.\n• Strong presentation skills and ability to articulate design rationale.',
                'responsibilities': '• Own end-to-end user experience across critical product journeys.\n• Build, scale, and maintain comprehensive design system components.\n• Work directly with engineers to ensure faithful design implementation.',
                'benefits': '• Competitive base salary + equity compensation\n• Flexible hybrid schedule (2 office days, 3 remote days)\n• Latest Apple MacBook Pro + 4K display\n• Annual design team offsite in international tech hubs',
            },
            {
                'title': 'AI & Machine Learning Research Specialist',
                'company': company1,
                'employer': employer_user1,
                'category': category_objs['Data Science & AI'],
                'job_type': 'Full-time',
                'experience_level': 'Senior',
                'location': 'Remote (US & Canada)',
                'is_remote': True,
                'salary_min': 140000,
                'salary_max': 185000,
                'is_featured': True,
                'skills_required': 'Python, PyTorch, LLMs, NLP, Transformer Architectures',
                'open_positions': 1,
                'deadline': timezone.now().date() + datetime.timedelta(days=60),
                'description': 'Help pioneer next-generation generative AI and natural language models at CloudScale. You will train custom foundation models, optimize inference speeds, and deploy intelligent agents.',
                'requirements': '• MS or PhD in Computer Science, AI, or equivalent practical industry experience.\n• 4+ years of hands-on experience training deep neural networks with PyTorch.\n• Deep familiarity with Transformer models, vector indexing, and RAG architectures.\n• Solid programming habits with clean, test-driven Python code.',
                'responsibilities': '• Train, benchmark, and deploy domain-specific LLM models.\n• Optimize model latency and cost on GPU compute clusters.\n• Publish technical whitepapers and guide product integrations.',
                'benefits': '• Significant equity grant with top-tier tier-1 venture backing\n• 100% employer-covered health and dental premiums\n• Direct access to dedicated multi-node H100 clusters',
            },
            {
                'title': 'Junior Python / Backend Developer',
                'company': company1,
                'employer': employer_user1,
                'category': category_objs['Software Engineering'],
                'job_type': 'Full-time',
                'experience_level': 'Entry',
                'location': 'Remote',
                'is_remote': True,
                'salary_min': 70000,
                'salary_max': 90000,
                'is_featured': False,
                'skills_required': 'Python, Django, SQLite, HTML5, CSS3, REST APIs',
                'open_positions': 2,
                'deadline': timezone.now().date() + datetime.timedelta(days=25),
                'description': 'An outstanding entry-level opportunity for an ambitious junior developer wanting to learn from senior engineers and build real-world software.',
                'requirements': '• Solid grasp of Python fundamentals and object-oriented programming.\n• Hands-on project experience with Django or similar web frameworks.\n• Basic knowledge of SQL, Git version control, and web standards.\n• Curiosity, enthusiasm, and a hunger to develop technical skills.',
                'responsibilities': '• Develop API endpoints and write comprehensive unit tests.\n• Assist in debugging, code refactoring, and documentation updates.\n• Attend daily standups and sprint reviews with the engineering team.',
                'benefits': '• Dedicated 1-on-1 mentorship program with Senior Principal Engineers\n• Comprehensive health and life insurance plans\n• Generous tech book and conference allowance',
            },
            {
                'title': 'Cloud DevOps & Infrastructure Engineer',
                'company': company1,
                'employer': employer_user1,
                'category': category_objs['DevOps & Cybersecurity'],
                'job_type': 'Full-time',
                'experience_level': 'Mid',
                'location': 'Austin, TX (Remote)',
                'is_remote': True,
                'salary_min': 110000,
                'salary_max': 140000,
                'is_featured': True,
                'skills_required': 'AWS, Terraform, Kubernetes, Linux, CI/CD, Python',
                'open_positions': 1,
                'deadline': timezone.now().date() + datetime.timedelta(days=35),
                'description': 'CloudScale is looking for a DevOps Engineer to automate cloud infrastructure, harden Kubernetes clusters, and optimize deployment speeds.',
                'requirements': '• 3+ years managing production workloads on AWS.\n• Expertise with Terraform Infrastructure as Code.\n• Practical experience managing Kubernetes clusters in production.\n• Strong scripting skills in Python or Bash.',
                'responsibilities': '• Maintain automated CI/CD deployment pipelines.\n• Monitor cluster health, uptime, and system performance metrics.\n• Implement proactive security controls and backup redundancy.',
                'benefits': '• Flexible working hours and remote-first setup\n• Full coverage for AWS and Kubernetes professional certifications\n• Competitive salary + bonus',
            },
            {
                'title': 'Technical Product Manager',
                'company': company2,
                'employer': employer_user2,
                'category': category_objs['Product & Project Management'],
                'job_type': 'Full-time',
                'experience_level': 'Senior',
                'location': 'New York, NY / Remote',
                'is_remote': True,
                'salary_min': 130000,
                'salary_max': 165000,
                'is_featured': False,
                'skills_required': 'Product Roadmaps, Agile, API Design, Customer Interviews, Metrics',
                'open_positions': 1,
                'deadline': timezone.now().date() + datetime.timedelta(days=40),
                'description': 'Lead product strategy and execution for our core developer API platform. Work directly with cross-functional engineering, design, and executive stakeholders.',
                'requirements': '• 4+ years in product management at a tech or SaaS company.\n• Technical background with ability to read APIs and review schema docs.\n• Data-driven mindset with proven execution velocity.\n• Exceptional communication and stakeholder alignment skills.',
                'responsibilities': '• Define feature specifications, user stories, and release milestones.\n• Prioritize product backlogs in close alignment with customer feedback.\n• Track key metrics including adoption, retention, and Net Promoter Score.',
                'benefits': '• Competitive salary, stock options, and 401(k) match\n• Comprehensive health, dental, and mental wellness coverage\n• Flexible remote work arrangement',
            },
        ]

        created_jobs = []
        for j_data in jobs_data:
            job, _ = Job.objects.get_or_create(
                title=j_data['title'],
                company=j_data['company'],
                defaults=j_data
            )
            created_jobs.append(job)

        self.stdout.write(self.style.SUCCESS(f"Created {len(created_jobs)} jobs"))

        # 6. Sample Application
        if created_jobs:
            app1, _ = JobApplication.objects.get_or_create(
                job=created_jobs[0],
                candidate=candidate_user,
                defaults={
                    'full_name': 'David Miller',
                    'email': 'david.miller@example.com',
                    'phone': '+1 (555) 234-5678',
                    'portfolio_url': 'https://davidmiller.dev',
                    'cover_letter': 'I am excited to submit my application for the Senior Full-Stack Django Engineer role at CloudScale Technologies. With over 5 years of production experience in Python, Django, and modern Tailwind CSS, I am ready to make immediate contributions to your core engineering objectives.',
                    'status': 'Shortlisted',
                    'employer_notes': 'Strong background in Python and Tailwind. Scheduled for initial interview.',
                }
            )

            app2, _ = JobApplication.objects.get_or_create(
                job=created_jobs[3],
                candidate=candidate_user,
                defaults={
                    'full_name': 'David Miller',
                    'email': 'david.miller@example.com',
                    'phone': '+1 (555) 234-5678',
                    'cover_letter': 'Excited to submit my application for this role. Looking forward to speaking with the hiring team.',
                    'status': 'Pending',
                }
            )

        self.stdout.write(self.style.SUCCESS("CareerConnect database seeding completed successfully!"))
