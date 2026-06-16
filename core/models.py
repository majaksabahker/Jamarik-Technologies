from django.db import models
from django.utils import timezone
from django.utils.text import slugify


# =========================
# TAGS (for Blog system)
# =========================
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, db_index=True)

    def __str__(self):
        return self.name


# =========================
# SERVICES
# =========================
class Service(models.Model):
    ICON_CHOICES = [
        ('brain', 'AI & Machine Learning'),
        ('globe', 'Web Development'),
        ('smartphone', 'Mobile Apps'),
        ('cloud', 'Cloud Solutions'),
        ('shield', 'Cybersecurity'),
        ('bar-chart', 'Data Analytics'),
    ]

    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=30, choices=ICON_CHOICES, default='brain')

    short_description = models.CharField(max_length=200)
    full_description = models.TextField()

    is_featured = models.BooleanField(default=False, db_index=True)
    order = models.PositiveIntegerField(default=0, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']
        indexes = [
            models.Index(fields=['is_featured']),
        ]

    def __str__(self):
        return self.title


# =========================
# SOLUTIONS
# =========================
class Solution(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    tagline = models.CharField(max_length=150)
    description = models.TextField()

    image = models.ImageField(upload_to='solutions/%Y/%m/', blank=True, null=True)

    is_featured = models.BooleanField(default=False, db_index=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


# =========================
# TECHNOLOGY STACK
# =========================
class Technology(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


# =========================
# PORTFOLIO
# =========================
class PortfolioProject(models.Model):
    CATEGORY_CHOICES = [
        ('ai', 'AI / ML'),
        ('web', 'Web'),
        ('mobile', 'Mobile'),
        ('data', 'Data'),
        ('fintech', 'Fintech'),
        ('health', 'HealthTech'),
    ]

    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    description = models.TextField()

    tech_stack = models.ManyToManyField(Technology, blank=True)

    image = models.ImageField(upload_to='portfolio/%Y/%m/', blank=True, null=True)

    live_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)

    is_featured = models.BooleanField(default=False, db_index=True)
    order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


# =========================
# TEAM
# =========================
class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    bio = models.TextField()

    image = models.ImageField(upload_to='team/%Y/%m/', blank=True, null=True)

    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)

    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


# =========================
# BLOG (PRODUCTION READY CMS)
# =========================
class BlogPost(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published')
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, db_index=True)

    excerpt = models.CharField(max_length=300)
    content = models.TextField()

    image = models.ImageField(upload_to='blog/%Y/%m/', blank=True, null=True)

    author = models.CharField(max_length=100, default='Jamarik Technologies Ltd Team')

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', db_index=True)

    tags = models.ManyToManyField('Tag', blank=True)

    # SEO (PRODUCTION STANDARD)
    meta_title = models.CharField(max_length=220, blank=True)
    meta_description = models.CharField(max_length=300, blank=True)

    published_at = models.DateTimeField(null=True, blank=True, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_at']
        indexes = [
            models.Index(fields=['status', 'published_at']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # AUTO SLUG (CRITICAL FOR PRODUCTION)
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1

            while BlogPost.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def publish(self):
        if self.status != 'published':
            self.status = 'published'
            self.published_at = timezone.now()
            self.save(update_fields=['status', 'published_at'])


# =========================
# JOBS
# =========================
class JobOpening(models.Model):
    TYPE_CHOICES = [
        ('full-time', 'Full-Time'),
        ('part-time', 'Part-Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
    ]

    title = models.CharField(max_length=100)
    department = models.CharField(max_length=100)

    location = models.CharField(max_length=100, default='Kampala, Uganda / Remote')

    type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    description = models.TextField()
    requirements = models.TextField()

    is_active = models.BooleanField(default=True, db_index=True)

    posted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-posted_at']

    def __str__(self):
        return f"{self.title} ({self.department})"


# =========================
# CONTACT
# =========================
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)

    subject = models.CharField(max_length=200)
    message = models.TextField()

    service_interest = models.CharField(max_length=100, blank=True)

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} — {self.subject}"


#Edit page by admin Jamarik Technologies Ltd
class Page(models.Model):
    slug = models.SlugField(unique=True)  # home, about, services
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class PageSection(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name="sections")
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    content = models.TextField()

    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        
# =========================
# TESTIMONIALS
# =========================
class Testimonial(models.Model):
    client_name = models.CharField(max_length=100)
    client_role = models.CharField(max_length=100)
    client_company = models.CharField(max_length=100)

    testimonial = models.TextField()

    rating = models.PositiveSmallIntegerField(default=5)

    image = models.ImageField(upload_to='testimonials/%Y/%m/', blank=True, null=True)

    is_featured = models.BooleanField(default=True)

    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.client_name} — {self.client_company}"

# models.py
from django.db import models

class LegalPage(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
# STATS
class Stat(models.Model):
    label = models.CharField(max_length=80)
    value = models.CharField(max_length=30)
    suffix = models.CharField(max_length=10, blank=True)

    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.value}{self.suffix} {self.label}"