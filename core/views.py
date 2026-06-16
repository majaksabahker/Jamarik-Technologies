from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from .models import Testimonial
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import (
    Service, Solution, PortfolioProject, TeamMember,
    BlogPost, JobOpening, Testimonial, Stat,
    Page
)

from .forms import ContactForm


# ---------------- HOME ----------------
def home(request):
    stats = Stat.objects.all()
    services = Service.objects.all()
    solutions = Solution.objects.filter(is_featured=True)
    projects = PortfolioProject.objects.filter(is_featured=True)
    blog_posts = BlogPost.objects.filter(status='published')[:3]

    testimonials = Testimonial.objects.filter(is_featured=True)

    context = {
        "stats": stats,
        "services": services,
        "solutions": solutions,
        "projects": projects,
        "blog_posts": blog_posts,
        "testimonials": testimonials,  # 👈 THIS LINE FIXES IT
    }

    return render(request, "home.html", context)


# views.py
from .models import LegalPage

def privacy_policy(request):
    page = LegalPage.objects.get(title="Privacy Policy")
    return render(request, "privacy.html", {"page": page})

# ---------------- ABOUT ----------------
def about(request):
    return render(request, 'about.html', {
        'team': TeamMember.objects.all(),
        'stats': Stat.objects.all(),
    })


# ---------------- SERVICES ----------------
def services(request):
    return render(request, 'services.html', {
        'services': Service.objects.all(),
    })


# ---------------- SOLUTIONS ----------------
def solutions(request):
    return render(request, 'solutions.html', {
        'solutions': Solution.objects.all(),
    })


# ---------------- PORTFOLIO ----------------
def portfolio(request):
    category = request.GET.get('category', '')
    projects = PortfolioProject.objects.all()

    if category:
        projects = projects.filter(category=category)

    return render(request, 'portfolio.html', {
        'projects': projects,
        'active_category': category,
        'categories': PortfolioProject.CATEGORY_CHOICES,
    })


def portfolio_detail(request, slug):
    project = get_object_or_404(PortfolioProject, slug=slug)

    related = PortfolioProject.objects.filter(
        category=project.category
    ).exclude(pk=project.pk)[:3]

    return render(request, 'portfolio_detail.html', {
        'project': project,
        'related': related
    })


# ---------------- CAREERS ----------------
def careers(request):
    return render(request, 'careers.html', {
        'jobs': JobOpening.objects.filter(is_active=True),
    })


# ---------------- BLOG (PRODUCTION READY) ----------------
def blog(request):
    tag = request.GET.get('tag')
    page_number = request.GET.get('page', 1)

    posts_queryset = BlogPost.objects.filter(
        status='published'
    ).order_by('-published_at')

    if tag:
        posts_queryset = posts_queryset.filter(
            tags__icontains=tag
        )

    paginator = Paginator(posts_queryset, 6)

    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog.html', {
        'posts': posts,
        'active_tag': tag,
        'is_paginated': posts.has_other_pages(),
        'page_obj': posts,
    })


# ---------------- BLOG DETAIL (PRODUCTION SAFE) ----------------
def blog_detail(request, slug):
    post = get_object_or_404(
        BlogPost,
        slug=slug,
        status='published'
    )

    related = BlogPost.objects.filter(
        status='published'
    ).exclude(pk=post.pk)[:3]

    return render(request, 'blog_detail.html', {
        'post': post,
        'related': related
    })


# ---------------- CMS PAGE VIEW (10/10 CORE FEATURE) ----------------
def page_view(request, slug):
    page = get_object_or_404(Page, slug=slug)

    sections = page.sections.all().order_by('order')

    return render(request, 'page.html', {
        'page': page,
        'sections': sections
    })


# ---------------- CONTACT ----------------
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            msg = form.save()

            try:
                send_mail(
                    subject=f"[Jamarik] New enquiry: {msg.subject}",
                    message=(
                        f"From: {msg.name} <{msg.email}>\n"
                        f"Phone: {msg.phone}\n"
                        f"Service: {msg.service_interest}\n\n"
                        f"{msg.message}"
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.CONTACT_EMAIL],
                    fail_silently=False,
                )
            except Exception:
                pass

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True})

            messages.success(request, "Thank you! We'll get back to you within 24 hours.")
            return redirect('contact')

    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


# ---------------- LEGAL ----------------
def privacy_policy(request):
    return render(request, 'legal/privacy.html')


def terms_of_service(request):
    return render(request, 'legal/terms.html')


def cookie_policy(request):
    return render(request, 'legal/cookies.html')