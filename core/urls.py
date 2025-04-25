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
    
    path('chat/<str:username>/', views.chat_view, name='chat_view'),
    path('send_message/', views.send_message, name='send_message'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
