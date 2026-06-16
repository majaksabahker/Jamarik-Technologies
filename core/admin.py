from django.contrib import admin
from .models import LegalPage
from .models import (
    Service, Solution, PortfolioProject, TeamMember,
    BlogPost, JobOpening, ContactMessage, Testimonial, Stat,
    Page, PageSection
)

# =========================
# CMS PAGES (NEW - CORE CMS)
# =========================
class PageSectionInline(admin.StackedInline):
    model = PageSection
    extra = 1


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "updated_at")
    search_fields = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [PageSectionInline]

admin.site.register(LegalPage)

# =========================
# SERVICES
# =========================
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon', 'is_featured', 'order', 'created_at']
    list_editable = ['is_featured', 'order']
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['order']


# =========================
# SOLUTIONS
# =========================
@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):
    list_display = ['title', 'tagline', 'is_featured', 'order']
    list_editable = ['is_featured', 'order']
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['order']


# =========================
# PORTFOLIO
# =========================
@admin.register(PortfolioProject)
class PortfolioProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_featured', 'order', 'created_at']
    list_filter = ['category', 'is_featured']
    search_fields = ['title']
    list_editable = ['is_featured', 'order']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['order']


# =========================
# TEAM
# =========================
@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'order']
    list_editable = ['order']
    search_fields = ['name', 'role']
    ordering = ['order']


# =========================
# BLOG (PRODUCTION CMS)
# =========================
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status', 'published_at', 'created_at']
    list_filter = ['status', 'published_at']
    search_fields = ['title', 'content', 'tags']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
    ordering = ['-published_at']
    list_per_page = 20

    actions = ['publish_posts']

    def publish_posts(self, request, queryset):
        for post in queryset:
            post.publish()
    publish_posts.short_description = "Publish selected posts"


# =========================
# JOBS
# =========================
@admin.register(JobOpening)
class JobOpeningAdmin(admin.ModelAdmin):
    list_display = ['title', 'department', 'type', 'location', 'is_active']
    list_filter = ['type', 'is_active']
    list_editable = ['is_active']
    search_fields = ['title', 'department']


# =========================
# CONTACT MESSAGES
# =========================
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    list_editable = ['is_read']
    search_fields = ['name', 'email', 'subject']
    readonly_fields = [
        'name', 'email', 'phone',
        'subject', 'message',
        'service_interest', 'created_at'
    ]


# =========================
# TESTIMONIALS
# =========================
@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'client_company', 'rating', 'is_featured', 'order']
    list_editable = ['is_featured', 'order']
    search_fields = ['client_name', 'client_company']
    ordering = ['order']


# =========================
# STATS
# =========================
@admin.register(Stat)
class StatAdmin(admin.ModelAdmin):
    list_display = ['label', 'value', 'suffix', 'order']
    list_editable = ['order']
    search_fields = ['label']
    ordering = ['order']