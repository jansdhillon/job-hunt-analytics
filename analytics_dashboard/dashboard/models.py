from django.db import models
from django.utils import timezone

class Company(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Application(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    application_number = models.CharField(max_length=10, blank=True, null=True)
    date_applied = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=[
        ('pending', 'Pending'),
        ('rejected', 'Rejected'),
        ('interview', 'Interview'),
        ('offer', 'Offer'),
        ('accepted', 'Accepted')
    ], default='pending')

    def __str__(self):
        return f"Application {self.application_number} at {self.company.name}"

class CoverLetter(models.Model):
    application = models.OneToOneField(Application, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    file_path = models.FileField(upload_to='cover_letters/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cover Letter for {self.application.company.name}"

class Resume(models.Model):
    application = models.OneToOneField(Application, on_delete=models.CASCADE)
    file_path = models.FileField(upload_to='resumes/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Resume for {self.application.company.name}"
