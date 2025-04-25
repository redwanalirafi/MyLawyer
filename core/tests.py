from django.test import TestCase

# Create your tests here.

# for adding dummy data
from django.contrib.auth.models import User
from models import *
from django.utils import timezone
import random

# Create Users (mix of students and lawyers)
def create_dummy_data():
    # Create student users
    student_users = [
        {'username': 'student1', 'email': 'student1@university.edu', 'first_name': 'Alex', 'last_name': 'Johnson', 'password': 'student123'},
        {'username': 'student2', 'email': 'student2@university.edu', 'first_name': 'Taylor', 'last_name': 'Smith', 'password': 'student123'},
        {'username': 'student3', 'email': 'student3@university.edu', 'first_name': 'Jordan', 'last_name': 'Williams', 'password': 'student123'},
        {'username': 'student4', 'email': 'student4@university.edu', 'first_name': 'Casey', 'last_name': 'Brown', 'password': 'student123'},
        {'username': 'student5', 'email': 'student5@university.edu', 'first_name': 'Morgan', 'last_name': 'Davis', 'password': 'student123'},
    ]
    
    student_objects = []
    for student_data in student_users:
        user = User.objects.create_user(
            username=student_data['username'],
            email=student_data['email'],
            password=student_data['password']
        )
        user.first_name = student_data['first_name']
        user.last_name = student_data['last_name']
        user.save()
        
        # Create profile for student
        profile = Profile.objects.create(
            user=user,
            is_active=True
        )
        student_objects.append(user)
    
    # Create lawyer users
    lawyer_data = [
        {
            'username': 'lawyer1', 
            'email': 'lawyer1@legalfirm.com', 
            'first_name': 'James', 
            'last_name': 'Wilson',
            'password': 'lawyer123',
            'specialization': 'Academic Misconduct',
            'experience_years': 8,
            'bio': 'Specialized in helping students navigate academic integrity issues and university disciplinary proceedings.',
            'available': True
        },
        {
            'username': 'lawyer2', 
            'email': 'lawyer2@legalfirm.com', 
            'first_name': 'Emily', 
            'last_name': 'Rodriguez',
            'password': 'lawyer123',
            'specialization': 'Housing Law',
            'experience_years': 5,
            'bio': 'Expert in landlord-tenant disputes, lease reviews, and housing discrimination cases for students.',
            'available': True
        },
        {
            'username': 'lawyer3', 
            'email': 'lawyer3@legalfirm.com', 
            'first_name': 'Michael', 
            'last_name': 'Lee',
            'password': 'lawyer123',
            'specialization': 'Student Visa Issues',
            'experience_years': 12,
            'bio': 'Focused on immigration law related to student visas, work permits, and related legal matters.',
            'available': False
        },
        {
            'username': 'lawyer4', 
            'email': 'lawyer4@legalfirm.com', 
            'first_name': 'Sarah', 
            'last_name': 'Martinez',
            'password': 'lawyer123',
            'specialization': 'Employment Law',
            'experience_years': 7,
            'bio': 'Assists students with workplace issues including discrimination, harassment, and wage disputes.',
            'available': True
        },
        {
            'username': 'lawyer5', 
            'email': 'lawyer5@legalfirm.com', 
            'first_name': 'David', 
            'last_name': 'Thompson',
            'password': 'lawyer123',
            'specialization': 'Criminal Defense',
            'experience_years': 15,
            'bio': 'Experienced in defending students facing criminal charges and helping them navigate the legal system.',
            'available': True
        },
        {
            'username': 'lawyer6', 
            'email': 'lawyer6@legalfirm.com', 
            'first_name': 'Jessica', 
            'last_name': 'Garcia',
            'password': 'lawyer123',
            'specialization': 'Intellectual Property',
            'experience_years': 9,
            'bio': 'Specialized in copyright issues, patent applications, and protecting student innovations and creations.',
            'available': False
        }
    ]
    
    lawyer_objects = []
    for data in lawyer_data:
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.save()
        
        # Create lawyer profile
        lawyer_profile = LawyerProfile.objects.create(
            user=user,
            specialization=data['specialization'],
            experience_years=data['experience_years'],
            bio=data['bio'],
            available=data['available']
        )
        lawyer_objects.append(lawyer_profile)
    
    # Create hire requests
    request_messages = [
        "I need help with a housing dispute with my landlord. They are refusing to return my security deposit.",
        "I'm facing academic misconduct allegations and need legal representation for my university hearing.",
        "Could you please help me review my employment contract for an internship?",
        "I'm having issues with my student visa and need urgent legal advice.",
        "Need assistance with a copyright issue related to my research project."
    ]
    
    status_options = ['pending', 'accepted', 'rejected']
    
    for _ in range(10):  # Create 10 random hire requests
        student = random.choice(student_objects)
        lawyer = random.choice(lawyer_objects)
        message = random.choice(request_messages)
        status = random.choice(status_options)
        
        # Create a time delta between -14 and 0 days from now
        days_ago = random.randint(0, 14)
        request_date = timezone.now() - timezone.timedelta(days=days_ago)
        
        hire_request = HireRequest.objects.create(
            student=student,
            lawyer=lawyer,
            message=message,
            status=status,
            date_requested=request_date
        )

    print("Dummy data created successfully!")

# Run this function to create all dummy data
# create_dummy_data()