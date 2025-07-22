from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',views.home,name="home"),
    path('login/',views.user_login,name="login"),
    path('register/',views.user_register,name="register"),
    # path('complete_signup/',views.complete_profile,name="complete_profile"),
    path('logout/',views.user_logout,name="logout"),
    path('dashboard/',views.dashboard,name="dashboard"),

    path('lawyers/',views.view_lawyers,name="view_lawyers"),
    path('hire_lawyer/<int:lawyer_id>/', views.hire_lawyer, name="hire_lawyer"),
    path('my_requests/', views.my_requests, name="my_requests"),
    path('send_message/', views.send_message, name="send_message"),
    path('profile/settings/', views.profile_settings, name="profile_settings"),
    path('lawyer/dashboard/', views.lawyer_dashboard, name='lawyer_dashboard'),

    path('hire-request/<int:request_id>/accept/', views.accept_request, name='accept_request'),
    path('hire-request/<int:request_id>/reject/', views.reject_request, name='reject_request'),
    
    path('client/<int:client_id>/', views.client_profile, name='client_profile'),
    path('client/<int:client_id>/end-relationship/', views.end_relationship, name='end_relationship'),
    path('client/generate/<int:client_id>', views.generate_report, name='generate_report'),
    
    path('chat/<str:username>/', views.chat_view, name='chat_view'),
    path('send_message/', views.send_message, name='send_message'),
    path('get_messages/', views.get_messages, name='get_messages'),
    path('send_message2/', views.send_message2, name='send_message2'),

    # Admin Dashboard
    path('admin-panel/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # User Management
    path('admin-panel/users/', views.user_list, name='admin_user_list'),
    path('admin-panel/users/<int:user_id>/', views.user_detail, name='admin_user_detail'),
    path('admin-panel/users/<int:user_id>/edit/', views.edit_user, name='admin_edit_user'),
    path('admin-panel/users/<int:user_id>/delete/', views.delete_user, name='admin_delete_user'),
    path('admin-panel/users/<int:user_id>/make-lawyer/', views.make_lawyer, name='admin_make_lawyer'),
    path('admin-panel/users/<int:user_id>/remove-lawyer/', views.remove_lawyer, name='admin_remove_lawyer'),
    path('admin-panel/users/<int:user_id>/toggle-status/', views.toggle_user_status, name='admin_toggle_user_status'),
    
    # Lawyer Management
    path('admin-panel/lawyers/', views.lawyer_list, name='admin_lawyer_list'),
    
    # Request Management
    path('admin-panel/hire-requests/', views.hire_request_list, name='admin_hire_request_list'),
    
    # Relationship Management
    path('admin-panel/relationships/', views.relationship_list, name='admin_relationship_list'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
