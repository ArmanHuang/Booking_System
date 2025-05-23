from django.urls import path
from . import views
from django.contrib import admin
from .views import custom_login
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', custom_login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.custom_logout, name='logout'),  
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('booking/edit/<int:booking_id>/', views.booking_edit, name='booking_edit'),
    path('book/', views.book_room, name='book_room'),
    path('admin/', admin.site.urls),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('approve/<int:booking_id>/', views.approve_booking, name='approve_booking'),
    path('reject/<int:booking_id>/', views.reject_booking, name='reject_booking'),
    path('booking/cancel/<int:booking_id>/', views.booking_cancel, name='booking_cancel'),
    path('booking/delete/<int:booking_id>/', views.booking_delete, name='booking_delete'),
    path('profile/', views.profile_view, name='profile_view'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)