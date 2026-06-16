from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('solutions/', views.solutions, name='solutions'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('careers/', views.careers, name='careers'),
    path('blog/', views.blog, name='blog'),
    path('contact/', views.contact, name='contact'),

    path('portfolio/<slug:slug>/', views.portfolio_detail, name='portfolio_detail'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),

    path('legal/privacy/', views.privacy_policy, name='privacy_policy'),
    path('legal/terms/', views.terms_of_service, name='terms_of_service'),
    path('legal/cookies/', views.cookie_policy, name='cookie_policy'),

    path('<slug:slug>/', views.page_view, name='page'),
]