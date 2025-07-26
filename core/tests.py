from django.test import TestCase

# Create your tests here.

# for adding dummy data
from django.contrib.auth.models import User
from .models import *
from django.utils import timezone
import random

# Create Users (mix of students and lawyers)
def create_dummy_data():

    # Create lawyer users
    lawyer_data = [
        {
            'username': 'ahossain',
            'email': 'arif.hossain@lawfirm.bd',
            'first_name': 'Arif',
            'last_name': 'Hossain',
            'password': 'lawyer123',
            'specialization': 'Corporate Law',
            'experience_years': 10,
            'bio': 'Expert in company law, contracts, and business compliance across Bangladesh.',
            'available': True
        },
        {
            'username': 'fkhan',
            'email': 'fatema.khan@lawfirm.bd',
            'first_name': 'Fatema',
            'last_name': 'Khan',
            'password': 'lawyer123',
            'specialization': 'Family Law',
            'experience_years': 8,
            'bio': 'Providing compassionate legal support for family disputes, divorce, and inheritance matters.',
            'available': True
        },
        {
            'username': 'srahman',
            'email': 'shafiq.rahman@lawfirm.bd',
            'first_name': 'Shafiq',
            'last_name': 'Rahman',
            'password': 'lawyer123',
            'specialization': 'Labor Law',
            'experience_years': 12,
            'bio': 'Focused on labor rights, workplace safety, and employment law in Bangladeshi industries.',
            'available': False
        },
        {
            'username': 'nislam',
            'email': 'nazia.islam@lawfirm.bd',
            'first_name': 'Nazia',
            'last_name': 'Islam',
            'password': 'lawyer123',
            'specialization': 'Criminal Law',
            'experience_years': 15,
            'bio': 'Experienced in criminal defense, representing clients in courts across Bangladesh.',
            'available': True
        },
        {
            'username': 'tsiddique',
            'email': 'tanvir.siddique@lawfirm.bd',
            'first_name': 'Tanvir',
            'last_name': 'Siddique',
            'password': 'lawyer123',
            'specialization': 'Property Law',
            'experience_years': 9,
            'bio': 'Helping clients with property disputes, land registration, and real estate transactions.',
            'available': True
        },
        {
            'username': 'srahman2',
            'email': 'sabina.rahman@lawfirm.bd',
            'first_name': 'Sabina',
            'last_name': 'Rahman',
            'password': 'lawyer123',
            'specialization': 'Environmental Law',
            'experience_years': 7,
            'bio': 'Advocating for environmental protection and compliance with Bangladesh environmental regulations.',
            'available': True
        },
        {
            'username': 'hmolla',
            'email': 'hasan.molla@lawfirm.bd',
            'first_name': 'Hasan',
            'last_name': 'Molla',
            'password': 'lawyer123',
            'specialization': 'Tax Law',
            'experience_years': 11,
            'bio': 'Providing expert advice on tax compliance and dispute resolution for businesses and individuals.',
            'available': False
        },
        {
            'username': 'rakther',
            'email': 'rahiha.akther@lawfirm.bd',
            'first_name': 'Rahiha',
            'last_name': 'Akther',
            'password': 'lawyer123',
            'specialization': 'Human Rights Law',
            'experience_years': 13,
            'bio': 'Committed to defending human rights and social justice issues within Bangladesh.',
            'available': True
        },
        {
            'username': 'ahaque',
            'email': 'azizul.haque@lawfirm.bd',
            'first_name': 'Azizul',
            'last_name': 'Haque',
            'password': 'lawyer123',
            'specialization': 'Immigration Law',
            'experience_years': 10,
            'bio': 'Specialist in immigration, visas, and work permits for Bangladeshi nationals abroad.',
            'available': True
        },
        {
            'username': 'mchowdhury',
            'email': 'mina.chowdhury@lawfirm.bd',
            'first_name': 'Mina',
            'last_name': 'Chowdhury',
            'password': 'lawyer123',
            'specialization': 'Education Law',
            'experience_years': 6,
            'bio': 'Providing legal assistance to educational institutions and students on policy and compliance matters.',
            'available': False
        },
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
        # student = random.choice(student_objects)
        lawyer = random.choice(lawyer_objects)
        message = random.choice(request_messages)
        status = random.choice(status_options)
        
        # Create a time delta between -14 and 0 days from now
        days_ago = random.randint(0, 14)
        request_date = timezone.now() - timezone.timedelta(days=days_ago)
        
        hire_request = HireRequest.objects.create(
            # student=student,
            lawyer=lawyer,
            message=message,
            status=status,
            date_requested=request_date
        )

    print("Dummy data created successfully!")

# Run this function to create all dummy data
# create_dummy_data()