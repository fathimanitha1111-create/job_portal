# CareerConnect - Modern Job Portal Platform

A complete, responsive, full-stack Job Portal platform built with **Python Django 5.x/6.x**, **Vite**, **Tailwind CSS**, and **SQLite** (structured for seamless switching to **MySQL**).

---

## 📑 Table of Contents
1. [Project Overview](#-project-overview)
2. [Technology Stack](#-technology-stack)
3. [Design System & Color Palette](#-design-system--color-palette)
4. [Project Structure](#-project-structure)
5. [Windows PowerShell Setup Guide](#-windows-powershell-setup-guide)
6. [Frontend Vite & Tailwind CSS Integration](#-frontend-vite--tailwind-css-integration)
7. [Database Configuration: SQLite to MySQL Switch](#-database-configuration-sqlite-to-mysql-switch)
8. [Demo Accounts & Credentials](#-demo-accounts--credentials)
9. [Pages & Features Summary](#-pages--features-summary)
10. [Testing Suite](#-testing-suite)
11. [Explanation in Malayalam (മലയാളം വിവരണം)](#-malayalam-explanation-മലയാളം-വിവരണം)

---

## 🌟 Project Overview

**CareerConnect** connects ambitious job seekers and forward-thinking employers through a clean, intuitive, and modern web application.

- **Frontend**: Vite + Tailwind CSS + Vanilla JavaScript (No React).
- **Backend**: Python 3.12 + Django.
- **App Architecture**: Single Django project (`careerconnect`) and **only one Django app** (`jobs`).
- **Database**: SQLite default for fast zero-configuration setup, with environment variable switching to MySQL.
- **Pages**: 14 distinct pages, each with its own dedicated HTML template and corresponding CSS file.

---

## 🛠️ Technology Stack

| Component | Technology | Version / Notes |
| :--- | :--- | :--- |
| **Backend Framework** | Python Django | 6.x / Python 3.12 |
| **App Name** | `jobs` | Single Django application |
| **Frontend Tooling** | Vite | 6.0+ |
| **Styling Framework** | Tailwind CSS | 3.4+ / Vanilla CSS overrides |
| **Client Scripting** | Vanilla JavaScript | ES6+ Modules & native DOM APIs |
| **Database** | SQLite 3 | Swappable to MySQL via `.env` |
| **Testing** | Django TestCase | 11 automated test cases |

---

## 🎨 Design System & Color Palette

The interface is styled using Tailwind CSS with a curated palette:
- **Navy Blue (Primary)**: `#0a192f` (`navy-900`), `#102a43` (`navy-800`), `#243b53` (`navy-700`)
- **White & Clean Slate**: `#ffffff`, `#f8fafc` (`slate-50`), `#f1f5f9` (`slate-100`)
- **Light Grey**: `#e2e8f0` (`slate-200`), `#cbd5e1` (`slate-300`)
- **Cyan Accent**: `#06b6d4` (`accent-500`), `#0891b2` (`accent-600`), `#0e7490` (`accent-700`)

Typography: **Inter** for clean readability and **Plus Jakarta Sans** for prominent headings.

---

## 📁 Project Structure

```
job_portal/
│
├── manage.py                          # Django management CLI
├── requirements.txt                   # Python dependencies (Django, Pillow, etc.)
├── .env.example                       # Environment template (SQLite / MySQL config)
├── .gitignore                         # Git exclusion rules
├── README.md                          # Documentation & guide
├── db.sqlite3                         # Seeded SQLite database
│
├── careerconnect/                     # Django Project Package
│   ├── __init__.py
│   ├── settings.py                    # Settings (DB switch, static, custom User model)
│   ├── urls.py                        # Root URL router
│   ├── asgi.py                        # ASGI entrypoint
│   └── wsgi.py                        # WSGI entrypoint
│
├── jobs/                              # Single Django App
│   ├── __init__.py
│   ├── admin.py                       # Django Admin configuration
│   ├── apps.py                        # JobsConfig
│   ├── models.py                      # User, CandidateProfile, CompanyProfile, Job, Application
│   ├── views.py                       # All 15 page views & CRUD operations
│   ├── urls.py                        # App route patterns
│   ├── forms.py                       # Registration, Login, JobPost, Application forms
│   ├── tests.py                       # 11 automated test cases
│   ├── management/
│   │   └── commands/
│   │       └── seed_data.py           # Database seeder (Demo jobs, categories, users)
│   │
│   ├── templates/
│   │   └── jobs/                      # 14 distinct HTML templates + base + 404
│   │       ├── base.html              # Core navigation, drawer, footer & alerts
│   │       ├── home.html              # Landing page with hero search & categories
│   │       ├── all_jobs.html          # Job catalog with filters & sorting
│   │       ├── job_details.html       # Job details & application modal
│   │       ├── candidate_register.html# Job seeker registration
│   │       ├── candidate_login.html   # Job seeker login with 1-click demo fill
│   │       ├── employer_register.html # Employer registration
│   │       ├── employer_login.html    # Employer login with 1-click demo fill
│   │       ├── candidate_dashboard.html# Candidate dashboard & profile editor
│   │       ├── employer_dashboard.html# Employer dashboard & applicant manager
│   │       ├── post_job.html          # New job listing form
│   │       ├── edit_job.html          # Update existing job form
│   │       ├── my_applications.html   # Candidate application tracker
│   │       ├── about.html             # About platform & stats
│   │       ├── contact.html           # Contact form & FAQ accordion
│   │       └── 404.html               # Custom 404 error page
│   │
│   └── static/                        # Static assets
│       ├── css/                       # Dedicated CSS file for each page
│       │   ├── base.css               # Compiled Tailwind CSS layer
│       │   ├── home.css               # Home page specific styling
│       │   ├── all_jobs.css           # All jobs catalog styling
│       │   ├── job_details.css        # Job details styling
│       │   ├── candidate_register.css # Candidate registration styling
│       │   ├── candidate_login.css    # Candidate login styling
│       │   ├── employer_register.css  # Employer registration styling
│       │   ├── employer_login.css     # Employer login styling
│       │   ├── candidate_dashboard.css# Candidate dashboard styling
│       │   ├── employer_dashboard.css # Employer dashboard styling
│       │   ├── post_job.css           # Job posting form styling
│       │   ├── edit_job.css           # Job editing styling
│       │   ├── my_applications.css    # Applications tracking styling
│       │   ├── about.css              # About page styling
│       │   └── contact.css            # Contact page styling
│       ├── js/
│       │   └── main.js                # Mobile drawer, modal, auto-fill, toast alerts
│       └── images/
│           ├── logo.png               # CareerConnect platform logo
│           ├── hero-image.png         # Homepage hero illustration
│           └── default-company.png    # Placeholder company avatar
│
└── frontend/                          # Vite + Tailwind Pipeline
    ├── package.json                   # npm build scripts and dev dependencies
    ├── vite.config.js                 # Vite bundler configuration
    ├── tailwind.config.js             # Tailwind theme & color extensions
    ├── postcss.config.js              # PostCSS plugins
    ├── index.html                     # Frontend entrypoint
    └── src/
        ├── input.css                  # Tailwind directives (@tailwind base, etc.)
        ├── output.css                 # Local compiled CSS
        └── main.js                    # Vite frontend script
```

---

## 💻 Windows PowerShell Setup Guide

Open Windows PowerShell in the project directory: `c:\Users\LENOVO\Desktop\job_portal`

### Step 1: Create and Activate Python Virtual Environment
```powershell
# Create virtual environment
py -3.12 -m venv .venv

# Activate virtual environment
.\.venv\Scripts\Activate.ps1
```

> **Note**: If PowerShell shows an ExecutionPolicy error, run:
> `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`

### Step 2: Install Python Dependencies
```powershell
pip install -r requirements.txt
```

### Step 3: Run Database Migrations
```powershell
python manage.py makemigrations jobs
python manage.py migrate
```

### Step 4: Seed Demo Data
Populate the database with demo users, 8 categories, and 6 verified jobs:
```powershell
python manage.py seed_data
```

### Step 5: Build Frontend Tailwind CSS Assets
```powershell
cd frontend
npm install --ignore-scripts
npm run build:css
cd ..
```

### Step 6: Start the Django Server
```powershell
python manage.py runserver 127.0.0.1:8000
```
Open your browser and navigate to: **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## ⚡ Frontend Vite & Tailwind CSS Integration

The frontend uses **Tailwind CSS v3.4** and **Vite**.

### Available npm commands in `frontend/`:
```powershell
cd frontend

# Build CSS into jobs/static/css/base.css
npm run build:css

# Run Tailwind in watch mode while designing
npm run watch:css

# Start Vite local development server
npm run dev
```

Tailwind styles are compiled directly into `jobs/static/css/base.css`, which Django templates load via:
```html
{% load static %}
<link rel="stylesheet" href="{% static 'css/base.css' %}">
<link rel="stylesheet" href="{% static 'css/home.css' %}">
```
In addition, `base.html` includes the Tailwind Play CDN configuration to ensure all responsive utility classes render smoothly in development and production.

---

## 🗄️ Database Configuration: SQLite to MySQL Switch

The database configuration in `careerconnect/settings.py` is modular and controlled by environment variables.

### Default: SQLite
No configuration needed. SQLite runs out of the box using `db.sqlite3`.

### Switching to MySQL:
1. Create a MySQL database in phpMyAdmin, MySQL Workbench, or CLI:
   ```sql
   CREATE DATABASE careerconnect_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
2. Install the MySQL Python client:
   ```powershell
   pip install mysqlclient
   # Or pure Python alternative:
   pip install pymysql
   ```
3. Copy `.env.example` to `.env` and configure:
   ```ini
   USE_MYSQL=True
   DB_NAME=careerconnect_db
   DB_USER=root
   DB_PASSWORD=your_mysql_password
   DB_HOST=127.0.0.1
   DB_PORT=3306
   ```
4. Run migrations on MySQL:
   ```powershell
   python manage.py migrate
   python manage.py seed_data
   ```

---

## 🔑 Demo Accounts & Credentials

Every login page features **1-click demo buttons** to fill these credentials automatically:

| User Role | Username | Password | Email | Access |
| :--- | :--- | :--- | :--- | :--- |
| **Candidate** | `candidate` | `password123` | `rahul@example.com` | Candidate Dashboard, Apply, My Applications |
| **Employer** | `employer` | `password123` | `hiring@technova.com` | Employer Dashboard, Post Job, Edit, Applicants |
| **Admin** | `admin` | `password123` | `admin@careerconnect.com` | Full Django Admin & Platform access |

Django Admin Panel: **[http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)**

---

## 📄 Pages & Features Summary

| Page | HTML Template | CSS File | Key Real Functionalities |
| :--- | :--- | :--- | :--- |
| **Home** | `home.html` | `home.css` | Hero search bar, featured jobs, category pills, verified hiring companies |
| **All Jobs** | `all_jobs.html` | `all_jobs.css` | Search by title/keyword, location, remote checkbox, job type, min salary, sort order |
| **Job Details** | `job_details.html` | `job_details.css` | Role description, compensation, requirements, application modal with duplicate prevention |
| **Candidate Register** | `candidate_register.html` | `candidate_register.css` | Full user registration with role assignment and candidate profile generation |
| **Candidate Login** | `candidate_login.html` | `candidate_login.css` | Secure session authentication with 1-click demo fill |
| **Employer Register** | `employer_register.html` | `employer_register.css` | User registration + company name, industry, location, and website creation |
| **Employer Login** | `employer_login.html` | `employer_login.css` | Employer authentication with 1-click demo fill |
| **Candidate Dashboard** | `candidate_dashboard.html` | `candidate_dashboard.css` | Total applications metric, status counters (Pending, Shortlisted, Accepted), profile editor |
| **Employer Dashboard** | `employer_dashboard.html` | `employer_dashboard.css` | Posted jobs table, applicant filter by status & job, company profile editor, quick status updates |
| **Post Job** | `post_job.html` | `post_job.css` | Real form creating jobs tied to the authenticated employer and company |
| **Edit Job** | `edit_job.html` | `edit_job.css` | Real form updating title, salary, skills, requirements, and active status |
| **My Applications** | `my_applications.html` | `my_applications.css` | Candidate applications tracker with status badges and filter by status |
| **About** | `about.html` | `about.css` | Company mission, platform statistics, core values |
| **Contact** | `contact.html` | `contact.css` | Real message submission storing in `ContactMessage` model + interactive FAQ accordion |
| **404 Page** | `404.html` | `base.css` | Branded page not found screen with return to home button |

### Real Interactive Workflows:
1. **Apply for a Job**: Candidates click "Apply Now", complete the modal form, attach resume (max 5MB, PDF/DOC/DOCX), and submit.
2. **Duplicate Application Prevention**: Candidates cannot submit multiple applications for the same job.
3. **Application Review & Status Updates**: Employers view applications in their dashboard and update statuses (**Pending &rarr; Shortlisted &rarr; Accepted &rarr; Rejected**) with optional feedback notes.
4. **Job CRUD**: Employers create, read, update, and delete jobs. Delete requests require confirmation to prevent accidental loss.

---

## 🧪 Testing Suite

Automated unit tests are located in `jobs/tests.py`. Run tests using:
```powershell
python manage.py test jobs
```
### Test Coverage (11 Tests):
- `test_home_page_loads`: Confirms landing page loads HTTP 200 with branding.
- `test_all_jobs_page_loads`: Confirms job listings page renders.
- `test_job_details_page`: Confirms slug-based job details render.
- `test_job_search_and_filter`: Tests keyword search and empty state handling.
- `test_candidate_duplicate_application_prevention`: Verifies duplicate applications are rejected and redirected.
- `test_employer_post_job`: Confirms employer job creation.
- `test_candidate_cannot_post_job`: Role-based security test ensuring candidates cannot post jobs.
- `test_employer_edit_job`: Confirms job modification by the owner.
- `test_employer_delete_job`: Confirms job deletion.
- `test_employer_update_application_status`: Tests updating status to Shortlisted and saving notes.
- `test_contact_form_submission`: Confirms contact form writes to the database.

---

## 🌐 Malayalam Explanation (മലയാളം വിവരണം)

### CareerConnect പ്രൊജക്റ്റ് വിശദീകരണം

ഈ പ്രോജക്റ്റ് **Python Django** ബാക്കെൻഡും, **Vite + Tailwind CSS** ഫ്രണ്ട് എൻഡും ഉപയോഗിച്ച് നിർമ്മിച്ച ഒരു പൂർണ്ണമായ ജോബ് പോർട്ടൽ (Job Portal) വെബ്‌സൈറ്റാണ്. ഇതിൽ React ഉപയോഗിച്ചിട്ടില്ല; പൂർണ്ണമായും **Vanilla JavaScript**, **HTML**, **CSS** എന്നിവയാണ് ഉപയോഗിച്ചിരിക്കുന്നത്.

### പ്രധാന സവിശേഷതകൾ:
1. **സിംഗിൾ ആപ്പ് ഘടന (Single Django App)**:
   - പ്രൊജക്റ്റിന്റെ പേര്: `careerconnect`
   - ആപ്പിന്റെ പേര്: `jobs` (എല്ലാ മോഡലുകളും, വ്യൂസും, ടെംപ്ലേറ്റുകളും ഇതിനുള്ളിലാണ്).
2. **14 പേജുകൾ (Dedicated HTML & CSS)**:
   - ഓരോ പേജിനും പ്രത്യേകം HTML ഫയലും (`home.html`, `all_jobs.html`, etc.) അതത് പേജിന് അനുയോജ്യമായ CSS ഫയലുകളും (`home.css`, `all_jobs.css`, etc.) നൽകിയിട്ടുണ്ട്.
3. **യൂസർ റോളുകൾ (User Roles)**:
   - **ഉദ്യോഗാർത്ഥി (Candidate)**: അക്കൗണ്ട് ഉണ്ടാക്കാനും, റെസ്യുമെ അപ്‌ലോഡ് ചെയ്യാനും, ജോലികൾക്ക് അപേക്ഷിക്കാനും, അപേക്ഷയുടെ നില (Pending, Shortlisted, Accepted, Rejected) ട്രാക്ക് ചെയ്യാനും സാധിക്കും.
   - **തൊഴിൽദാതാവ് (Employer)**: കമ്പനി പ്രൊഫൈൽ നിർമ്മിക്കാനും, പുതിയ ജോലികൾ പോസ്റ്റ് ചെയ്യാനും, എഡിറ്റ് ചെയ്യാനും, ഡിലീറ്റ് ചെയ്യാനും, ലഭിച്ച അപേക്ഷകൾ പരിശോധിച്ച് സ്റ്റാറ്റസ് മാറ്റാനും കഴിയും.
   - **അഡ്മിൻ (Admin)**: Django Admin പാനൽ വഴി മുഴുവൻ ഡാറ്റയും നിയന്ത്രിക്കാം.
4. **ഡ്യൂപ്ലിക്കേറ്റ് ആപ്ലിക്കേഷൻ നിയന്ത്രണം**: ഒരു ഉദ്യോഗാർത്ഥിക്ക് ഒരേ ജോലിക്ക് ഒന്നിൽ കൂടുതൽ തവണ അപേക്ഷിക്കാൻ സാധിക്കില്ല.
5. **ഡാറ്റാബേസ് മാറ്റം (SQLite to MySQL)**:
   - തുടക്കത്തിൽ SQLite ഉപയോഗിക്കുന്നു.
   - ഭാവിയിൽ MySQL-ലേക്ക് മാറ്റാൻ `.env` ഫയലിൽ `USE_MYSQL=True` നൽകിയാൽ മതിയാകും.

### എങ്ങനെ റൺ ചെയ്യാം (PowerShell Commands):
```powershell
# 1. വെർച്വൽ എൻവയോൺമെന്റ് ആക്റ്റീവ് ചെയ്യുക
.\.venv\Scripts\Activate.ps1

# 2. ഡിപൻഡൻസികൾ ഇൻസ്റ്റാൾ ചെയ്യുക
pip install -r requirements.txt

# 3. മൈഗ്രേഷൻ നടത്തുക
python manage.py migrate

# 4. ഡെമോ ഡാറ്റ ചേർക്കുക
python manage.py seed_data

# 5. സെർവർ ആരംഭിക്കുക
python manage.py runserver 127.0.0.1:8000
```
ബ്രൗസറിൽ **`http://127.0.0.1:8000/`** തുറക്കുക.

### ഡെമോ അക്കൗണ്ടുകൾ (Demo Logins):
- **Candidate Login**: Username: `candidate`, Password: `password123`
- **Employer Login**: Username: `employer`, Password: `password123`
- **Admin Panel**: Username: `admin`, Password: `password123` (URL: `/admin/`)

---

## 🚀 GitHub Push & Vercel Deployment Guide

Follow these step-by-step instructions in Windows PowerShell to upload your repository to GitHub and deploy it publicly on Vercel.

### Step 1: Initialize Git and Commit Your Code
Open PowerShell in `c:\Users\LENOVO\Desktop\job_portal`:
```powershell
# 1. Initialize git (if not already done)
git init

# 2. Stage all project files (ignoring .venv, .env, db.sqlite3 via .gitignore)
git add .

# 3. Create your initial commit
git commit -m "feat: initial commit for CareerConnect job portal"
```

### Step 2: Create a Repository on GitHub and Push
1. Go to [https://github.com/new](https://github.com/new) in your browser.
2. Enter a repository name (e.g. `careerconnect-job-portal`).
3. Leave it **Public** (or Private). Do **not** initialize with README or .gitignore (we already have them).
4. Click **Create repository**.
5. Copy your repository URL, then run in PowerShell:
```powershell
# Set main branch
git branch -M main

# Link your remote GitHub repository (replace with your actual GitHub URL)
git remote add origin https://github.com/YOUR_USERNAME/careerconnect-job-portal.git

# Push code to GitHub
git push -u origin main
```

---

### Step 3: Production Database Setup (Free PostgreSQL on Neon or Supabase)
Because Vercel is a serverless platform with a read-only filesystem, SQLite will not retain permanent data in production. Connect a free cloud PostgreSQL database:
1. Create a free account at [https://neon.tech](https://neon.tech) or [https://supabase.com](https://supabase.com).
2. Create a new database named `careerconnect`.
3. Copy the database connection URL (`DATABASE_URL`), which looks like:
   `postgresql://username:password@ep-cool-sample.us-east-2.aws.neon.tech/careerconnect?sslmode=require`

---

### Step 4: Import Project into Vercel
1. Log in to [https://vercel.com](https://vercel.com).
2. Click **Add New...** &rarr; **Project**.
3. Under **Import Git Repository**, select your `careerconnect-job-portal` repository.
4. **Project Settings**:
   - Framework Preset: **Other** (or detected Python).
   - Root Directory: `./` (leave default).

---

### Step 5: Configure Environment Variables in Vercel
In the Vercel project configuration screen, expand **Environment Variables** and add:

| Variable Name | Value | Description |
| :--- | :--- | :--- |
| `SECRET_KEY` | *(A long random secret string)* | Production Django Secret Key |
| `DEBUG` | `False` | Disables debug mode in production |
| `ALLOWED_HOSTS` | `.vercel.app` | Allows all Vercel deployment URLs |
| `CSRF_TRUSTED_ORIGINS` | `https://*.vercel.app` | Prevents CSRF errors on forms |
| `DATABASE_URL` | *(Your Neon or Supabase connection string)* | Cloud PostgreSQL database |

---

### Step 6: Deploy
Click **Deploy**!
Vercel will run `build_files.sh`, install requirements, collect static files, and provide you with a live public URL (e.g., `https://careerconnect-job-portal.vercel.app`).

---

### 🌐 GitHub & Vercel വിന്യാസ വഴികാട്ടി (Malayalam Explanation)

നിങ്ങളുടെ പ്രൊജക്റ്റ് **GitHub**-ലേക്ക് അപ്‌ലോഡ് ചെയ്യാനും **Vercel** വഴി ലോകമെമ്പാടും ലഭ്യമാക്കാനും താഴെ പറയുന്ന ലളിതമായ ഘട്ടങ്ങൾ പാലിക്കുക:

1. **GitHub-ലേക്ക് അപ്‌ലോഡ് ചെയ്യൽ**:
   - PowerShell-ൽ `git add .` നൽകി ഫയലുകൾ ചേർക്കുക. `.gitignore` ഉള്ളതിനാൽ പാസ്‌വേഡുകളോ `.venv` ഫയലുകളോ അപ്‌ലോഡ് ആകില്ല.
   - GitHub-ൽ ഉണ്ടാക്കിയ പുതിയ repository-ലേക്ക് `git push -u origin main` വഴി കോഡ് അയക്കുക.

2. **ഡാറ്റാബേസ് ക്രമീകരണം (Production Database)**:
   - Vercel-ൽ SQLite സ്ഥിരമായി ഡാറ്റ സേവ് ചെയ്യില്ല. അതിനാൽ [Neon.tech](https://neon.tech) അല്ലെങ്കിൽ [Supabase.com](https://supabase.com) വഴി സൗജന്യമായി ഒരു PostgreSQL ഡാറ്റാബേസ് ഉണ്ടാക്കി അതിന്റെ ലിങ്ക് (`DATABASE_URL`) ഉപയോഗിക്കുക.

3. **Vercel വിന്യാസം (Vercel Deployment)**:
   - [Vercel.com](https://vercel.com)-ൽ ലോഗിൻ ചെയ്ത് GitHub repository തിരഞ്ഞെടുക്കുക.
   - Environment Variables-ൽ `DEBUG=False`, `ALLOWED_HOSTS=.vercel.app`, `CSRF_TRUSTED_ORIGINS=https://*.vercel.app`, `DATABASE_URL` എന്നിവ ചേർക്കുക.
   - **Deploy** ബട്ടൺ അമർത്തുക. ഏതാനും നിമിഷങ്ങൾക്കുള്ളിൽ നിങ്ങളുടെ വെബ്‌സൈറ്റ് ലൈവ് ആകും!

