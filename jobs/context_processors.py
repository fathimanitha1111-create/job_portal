from .models import Category, Job, CompanyProfile, JobApplication

def careerconnect_context(request):
    top_categories = Category.objects.all()[:8]
    applied_job_ids = []

    if request.user.is_authenticated and request.user.is_candidate:
        applied_job_ids = list(JobApplication.objects.filter(candidate=request.user).values_list('job_id', flat=True))

    stats = {
        'total_jobs': Job.objects.filter(is_active=True).count(),
        'total_companies': CompanyProfile.objects.count(),
        'total_categories': Category.objects.count(),
    }

    return {
        'portal_categories': top_categories,
        'applied_job_ids': applied_job_ids,
        'site_stats': stats,
    }
