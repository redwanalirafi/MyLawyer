from datetime import timezone
import json
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .forms import HireRequestForm
from django.db.models import Q, Count
from django.http import JsonResponse

# Create your views here.

def home(request):
    return render(request,"home.html")

# @login_required
# def dashboard(request):
#     return render(request,"dashboard_user.html")

def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            print("Login OK")
            login(request, user)
            messages.success(request, f"Login successful! Welcome back, {username} 🎉")
            return redirect("dashboard")  # Redirect to home page after login
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect("login")  # Stay on login page if authentication fails

    return render(request, "login.html")  # Render login page if method is GET


def user_logout(request):
    logout(request)
    storage = messages.get_messages(request)
    for _ in storage:
        pass
    messages.success(request, "You have been logged out successfully.")
    return redirect("login")


def user_register(request):
    if request.method == "POST":
        try:
            print("POST")
            username = request.POST["username"]
            email = request.POST["email"]
            password1 = request.POST["password1"]
            password2 = request.POST["password2"]

            if password1 != password2:
                messages.error(request, "Passwords do not match!")
                return render(request, "register.html")

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already taken!")
                print("already exists")
                return render(request, "register.html")

            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()

            profile = Profile.objects.create(user=user, is_active=True) 
            profile.save()

            login(request, user) 
            messages.success(request, "Account created successfully!")
            print("profile created")
            return redirect("home") 
        except Exception as e:
            print(e)

    return render(request, "register.html")


def view_lawyers(request):

    lawyers = LawyerProfile.objects.filter(available=True)
    return render(request, "lawyers.html", {'lawyers': lawyers})

@login_required
def hire_lawyer(request, lawyer_id):
    lawyer = get_object_or_404(LawyerProfile, id=lawyer_id)
    
    # Check if the lawyer is available
    if not lawyer.available:
        messages.error(request, "This lawyer is currently unavailable.")
        return redirect('view_lawyers')
    
    # Check if there's an existing pending request
    existing_request = HireRequest.objects.filter(
        student=request.user,
        lawyer=lawyer,
        status='pending'
    ).exists()
    
    if existing_request:
        messages.info(request, "You already have a pending request with this lawyer.")
        return redirect('my_requests')
    
    if request.method == 'POST':
        form = HireRequestForm(request.POST)
        if form.is_valid():
            hire_request = form.save(commit=False)
            hire_request.student = request.user
            hire_request.lawyer = lawyer
            hire_request.save()
            messages.success(request, f"Your hire request has been sent to {lawyer.user.get_full_name() or lawyer.user.username}.")
            return redirect('my_requests')
    else:
        form = HireRequestForm()
    
    return render(request, 'hire_lawyer.html', {
        'lawyer': lawyer,
        'form': form
    })

@login_required
def my_requests(request):
    requests = HireRequest.objects.filter(student=request.user).order_by('-date_requested')
    return render(request, 'my_requests.html', {'requests': requests})

@login_required
def dashboard(request):
    try:
        lawyer_profile = request.user.lawyerprofile
        return redirect('lawyer_dashboard')
    except LawyerProfile.DoesNotExist:
        pass  # user is a student

    # Get recent requests (limit to 5)
    recent_requests = HireRequest.objects.filter(
        student=request.user
    ).order_by('-date_requested')[:5]
    
    # Get count of pending and accepted requests
    pending_requests = HireRequest.objects.filter(
        student=request.user, 
        status='pending'
    ).count()
    
    accepted_requests = HireRequest.objects.filter(
        student=request.user, 
        status='accepted'
    ).count()
    
    # Get lawyers with accepted requests for messaging
    accepted_lawyers = []
    lawyer_requests = HireRequest.objects.filter(
        student=request.user,
        status='accepted'
    ).select_related('lawyer', 'lawyer__user')
    
    for hire_request in lawyer_requests:
        # Get messages for this lawyer
        messages_list = Message.objects.filter(
            Q(sender=request.user, recipient=hire_request.lawyer.user) | 
            Q(sender=hire_request.lawyer.user, recipient=request.user)
        ).order_by('sent_at')
        
        # Count unread messages
        unread_count = Message.objects.filter(
            sender=hire_request.lawyer.user,
            recipient=request.user,
            is_read=False
        ).count()
        
        lawyer_data = {
            'id': hire_request.lawyer.id,
            'user': hire_request.lawyer.user,
            'messages': messages_list,
            'unread_count': unread_count
        }
        
        accepted_lawyers.append(lawyer_data)
    
    # Get total unread messages
    unread_messages = sum(lawyer['unread_count'] for lawyer in accepted_lawyers)
    
    context = {
        'recent_requests': recent_requests,
        'pending_requests': pending_requests,
        'accepted_requests': accepted_requests,
        'accepted_lawyers': accepted_lawyers,
        'unread_messages': unread_messages
    }
    
    return render(request, 'dashboard.html', context)

@login_required
def send_message(request):
    if request.method == 'POST':
        lawyer_id = request.POST.get('lawyer_id')
        message_content = request.POST.get('message')
        
        # Validate the lawyer and check if there's an accepted request
        try:
            lawyer = LawyerProfile.objects.get(id=lawyer_id)
            
            # Check if there's an accepted request
            hire_request = HireRequest.objects.filter(
                student=request.user,
                lawyer=lawyer,
                status='accepted'
            ).exists()
            
            if not hire_request:
                return JsonResponse({'success': False, 'error': 'No active case with this lawyer'})
            
            # Create and save the message
            message = Message(
                sender=request.user,
                recipient=lawyer.user,
                content=message_content
            )
            message.save()
            
            return JsonResponse({'success': True})
            
        except LawyerProfile.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Lawyer not found'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@login_required
def profile_settings(request):
    if request.method == 'POST':
        # Handle form submission (update email, username, etc.)
        # For example:
        new_email = request.POST.get('email')
        if new_email:
            request.user.email = new_email
            request.user.save()
            messages.success(request, "Your profile has been updated successfully.")
        return redirect('profile_settings')
    
    return render(request, 'profile_settings.html')

@login_required
def lawyer_dashboard(request):
    try:
        lawyer_profile = request.user.lawyerprofile
    except LawyerProfile.DoesNotExist:
        return redirect('dashboard')  # not a lawyer, redirect to student dashboard

    pending_requests = HireRequest.objects.filter(
        lawyer=lawyer_profile, 
        status='pending'
    ).select_related('student')

    accepted_requests = HireRequest.objects.filter(
        lawyer=lawyer_profile, 
        status='accepted'
    ).select_related('student')

    conversations = []
    for hire_request in accepted_requests:
        student_user = hire_request.student
        messages_list = Message.objects.filter(
            Q(sender=request.user, recipient=student_user) |
            Q(sender=student_user, recipient=request.user)
        ).order_by('sent_at')

        unread_count = Message.objects.filter(
            sender=student_user,
            recipient=request.user,
            is_read=False
        ).count()

        conversations.append({
            'student': student_user,
            'messages': messages_list,
            'unread_count': unread_count,
        })

    context = {
        'pending_requests': pending_requests,
        'accepted_requests': accepted_requests,
        'conversations': conversations,
    }
    return render(request, 'lawyer_dashboard.html', context)

@login_required
def accept_request(request, request_id):
    hire_request = get_object_or_404(HireRequest, id=request_id, lawyer__user=request.user)
    hire_request.status = 'accepted'
    hire_request.save()
    messages.success(request, 'You have accepted the request.')
    return redirect('lawyer_dashboard')

@login_required
def reject_request(request, request_id):
    hire_request = get_object_or_404(HireRequest, id=request_id, lawyer__user=request.user)
    hire_request.status = 'rejected'
    hire_request.save()
    messages.info(request, 'You have rejected the request.')
    return redirect('lawyer_dashboard')



@login_required
def client_profile(request, client_id):
    """
    View a client's profile information
    Only accessible to lawyers who have an accepted hire request with this client
    """
    client = get_object_or_404(User, id=client_id)
    
    # Check if the lawyer has an accepted hire request with this client
    if not HireRequest.objects.filter(
        lawyer__user=request.user, 
        student=client, 
        status='accepted'
    ).exists():
        messages.error(request, "You don't have permission to view this client's profile.")
        return redirect('lawyer_dashboard')
    
    # Get client details
    try:
        profile = client.profile
    except Profile.DoesNotExist:
        profile = None
    
    # Get case history
    hire_request = HireRequest.objects.get(
        lawyer__user=request.user,
        student=client,
        status='accepted'
    )
    
    # Get all messages between lawyer and client
    message_history = Message.objects.filter(
        (Q(sender=request.user) & Q(recipient=client)) |
        (Q(sender=client) & Q(recipient=request.user))
    ).order_by('sent_at')
    
    # Get consultation history (if you have a model for this)
    consultations = []  # Replace with actual query if you have a Consultation model
    
    context = {
        'client': client,
        'profile': profile,
        'hire_request': hire_request,
        'message_history': message_history,
        'consultations': consultations,
    }
    return render(request, 'client_profile.html', context)


@login_required
def end_relationship(request, client_id):
    if request.method == 'POST':
        client = get_object_or_404(User, id=client_id)
        
        # Update hire request status
        hire_request = get_object_or_404(HireRequest, 
                                         student=client, 
                                         lawyer__user=request.user, 
                                         status='accepted')
        
        hire_request.status = 'completed'  # or add a new status like 'terminated' to your model choices
        hire_request.save()
        
        messages.success(request, f"Your relationship with {client.get_full_name() or client.username} has been marked as completed.")
        return redirect('lawyer_dashboard')  # Adjust to your actual dashboard URL name
    
    return redirect('client_profile', client_id=client_id)


@login_required
def chat_view(request, username):
    other_user = get_object_or_404(User, username=username)

    messages = Message.objects.filter(
        sender__in=[request.user, other_user],
        recipient__in=[request.user, other_user]
    )

    # Mark unread messages as read
    Message.objects.filter(sender=other_user, recipient=request.user, is_read=False).update(is_read=True)

    return render(request, 'chat/chat.html', {
        'messages': messages,
        'other_user': other_user,
    })

@login_required
def send_message(request):
    if request.method == "POST":
        content = request.POST.get('content')
        recipient_id = request.POST.get('recipient_id')
        recipient = get_object_or_404(User, id=recipient_id)
        message = Message.objects.create(
            sender=request.user,
            recipient=recipient,
            content=content
        )
        return JsonResponse({
            'status': 'ok',
            'message': message.content,
            'timestamp': message.sent_at.strftime("%H:%M"),
        })
    return JsonResponse({'status': 'fail'})