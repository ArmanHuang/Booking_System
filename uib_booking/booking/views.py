from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth import login, logout
from django.template.loader import get_template
from django.http import HttpResponse

from .models import MeetingRoom, Booking
from .forms import EmailAuthenticationForm, ProfileForm, BookingForm, CustomUserCreationForm, UserForm


def is_admin(user):
    return user.is_staff



def home_view(request):
    return render(request, 'booking/home.html')


@login_required
def profile_view(request):
    return render(request, 'booking/profile_view.html', {'profile': request.user.profile})


@login_required
def profile_edit(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('user_dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    return render(request, 'booking/profile_edit.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


@login_required
def booking_cancel(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if request.method == 'POST' and booking.status in ['pending', 'approved']:
        booking.status = 'canceled'
        booking.save()
        messages.success(request, 'Booking canceled successfully.')
    return redirect('user_dashboard')


@login_required
def booking_delete(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if request.method == 'POST':
        booking.delete()
        messages.success(request, 'Booking deleted successfully.')
    return redirect('user_dashboard')


def custom_login(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if request.user.is_staff:
                return redirect('/admin/')
            return redirect('user_dashboard')
        messages.error(request, "Invalid email or password.")
    else:
        form = EmailAuthenticationForm()
    return render(request, 'booking/login.html', {'form': form})


@login_required
def user_dashboard(request):
    rooms = MeetingRoom.objects.filter(is_active=True)
    bookings = Booking.objects.filter(user=request.user).order_by('-date')
    return render(request, 'booking/user_dashboard.html', {
        'rooms': rooms,
        'bookings': bookings,
    })


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('user_dashboard')
        messages.error(request, "There was an error creating your account. Please check the form.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'booking/sign_up.html', {'form': form})


@login_required
def book_room(request):
    rooms = MeetingRoom.objects.filter(is_active=True)
    if request.method == 'POST':
        room_id = request.POST.get('room')
        date_ = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        purpose = request.POST.get('purpose')
        room = get_object_or_404(MeetingRoom, pk=room_id)

        conflict = Booking.objects.filter(
            room=room,
            date=date_,
            start_time__lt=end_time,
            end_time__gt=start_time,
            status='approved',
        ).exists()

        if conflict:
            messages.error(request, 'This room is already booked for the selected time.')
        else:
            Booking.objects.create(
                user=request.user,
                room=room,
                date=date_,
                start_time=start_time,
                end_time=end_time,
                purpose=purpose,
                status='pending',
            )
            messages.success(request, 'Booking successful, waiting for admin approval.')
            return redirect('user_dashboard')

    return render(request, 'booking/book_room.html', {'rooms': rooms})


@login_required
def booking_edit(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    rooms = MeetingRoom.objects.all()

    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, "Booking updated successfully.")
            return redirect('user_dashboard')
        messages.error(request, "Please fix the errors below.")
    else:
        form = BookingForm(instance=booking)

    return render(request, 'booking/booking_edit.html', {
        'form': form,
        'booking': booking,
        'rooms': rooms,
        'selected_room': booking.room,
        'selected_date': form['date'].value() or '',
        'selected_start_time': form['start_time'].value() or '',
        'selected_end_time': form['end_time'].value() or '',
    })


@user_passes_test(is_admin)
def admin_dashboard(request):
    bookings = Booking.objects.all().order_by('-date')
    return render(request, 'booking/admin_dashboard.html', {'bookings': bookings})


@user_passes_test(is_admin)
def approve_booking(request, booking_id):
    if request.method == 'POST':
        booking = get_object_or_404(Booking, id=booking_id)
        booking.status = 'approved'
        booking.save()
        messages.success(request, 'Booking approved.')
    return redirect('admin_dashboard')


@user_passes_test(is_admin)
def reject_booking(request, booking_id):
    if request.method == 'POST':
        booking = get_object_or_404(Booking, id=booking_id)
        booking.status = 'rejected'
        booking.save()
        messages.warning(request, 'Booking rejected.')
    return redirect('admin_dashboard')


@login_required
def custom_logout(request):
    logout(request)
    return redirect('home')
