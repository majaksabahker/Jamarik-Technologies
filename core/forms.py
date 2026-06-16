from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'service_interest', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your full name', 'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'placeholder': 'your@email.com', 'class': 'form-input'}),
            'phone': forms.TextInput(attrs={'placeholder': '+256 700 000 000', 'class': 'form-input'}),
            'subject': forms.TextInput(attrs={'placeholder': 'How can we help?', 'class': 'form-input'}),
            'service_interest': forms.Select(
                attrs={'class': 'form-input'},
                choices=[
                    ('', 'Select a service'),
                    ('AI Solutions', 'AI Solutions'),
                    ('Web Development', 'Web Development'),
                    ('Mobile Apps', 'Mobile Apps'),
                    ('Cloud Services', 'Cloud Services'),
                    ('Data Analytics', 'Data Analytics'),
                    ('Cybersecurity', 'Cybersecurity'),
                    ('Other', 'Other'),
                ]
            ),
            'message': forms.Textarea(attrs={
                'placeholder': 'Tell us about your project...',
                'class': 'form-input',
                'rows': 5
            }),
        }