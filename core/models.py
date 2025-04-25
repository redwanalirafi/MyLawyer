from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class LawyerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    specialization = models.CharField(max_length=100)
    experience_years = models.PositiveIntegerField()
    bio = models.TextField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.specialization}"

class HireRequest(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hire_requests')
    lawyer = models.ForeignKey(LawyerProfile, on_delete=models.CASCADE)
    message = models.TextField()
    date_requested = models.DateTimeField(auto_now_add=True)
    status_choices = [('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected'),  ('completed', 'Completed')]
    status = models.CharField(max_length=10, choices=status_choices, default='pending')

    def __str__(self):
        return f"HireRequest from {self.student.username} to {self.lawyer.user.username}"
    

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['sent_at']
    
    def __str__(self):
        return f"From {self.sender.username} to {self.recipient.username} at {self.sent_at}"
    
class ClientRelationship(models.Model):
    lawyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lawyer_relationships')
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_relationships')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    status_choices = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('terminated', 'Terminated')
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='active')
    termination_reason_choices = [
        ('case_completed', 'Case Completed'),
        ('client_request', 'Client Requested'),
        ('conflict_of_interest', 'Conflict of Interest'),
        ('other', 'Other')
    ]
    termination_reason = models.CharField(max_length=50, choices=termination_reason_choices, null=True, blank=True)
    termination_notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Relationship between {self.lawyer.username} and {self.client.username}"