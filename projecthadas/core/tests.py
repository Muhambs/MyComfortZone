from django.test import TestCase, RequestFactory,Client, override_settings
from django.urls import *
from django.http import *
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.models import User, Group
from django.contrib.messages import get_messages
from .forms import *
from .models import *
from .views import *
from django.contrib.auth.models import *
from django.contrib.auth import *
from django.core.mail import EmailMessage
from django.conf import settings
from unittest.mock import patch
from django.core.exceptions import PermissionDenied

# Create your tests here.

class RegisterPatientViewTests(TestCase):
    def setUp(self):
        self.url = reverse('registerpatient')
        Group.objects.get_or_create(name='patient')
    def test_register_patient_success(self):
        form_data = {
            'username': 'newpatient',
            'password': 'pa12345',
        }
        response = self.client.post(self.url, form_data)
        messages = list(get_messages(response.wsgi_request))

    def test_form_invalid(self):
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registerpatient.html')

def test_register_patient_with_duplicate_username(self):
    User.objects.create_user(username='existinguser', password='test123')

    form_data = {
        'username': 'existinguser',
        'password': 'pa12345',
    }
    response = self.client.post(self.url, form_data)

    self.assertEqual(User.objects.filter(username='existinguser').count(), 1)

    self.assertFormError(response, 'form', 'username', 'A user with that username already exists.')

    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'registerpatient.html')

    messages = list(get_messages(response.wsgi_request))
    self.assertIn("A user with that username already exists.",
                  [message.message for message in messages])
class RegisterDoctorViewTests(TestCase):
    def setUp(self):
        self.url = reverse('registerdoctor')
        Group.objects.get_or_create(name='doctor')

    def test_register_doctor_success(self):
        form_data = {
            'username': 'newdoctor1',
            'password': 'do12345',
        }
        response = self.client.post(self.url, form_data)


class LogoutViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.login_url = reverse('patientlogin')
        self.logout_url = reverse('home')
        self.home_url = reverse('home')
    def test_logout(self):
        self.client.login(username='testuser', password='12345')
        user = get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.get(self.logout_url)
        user = get_user(self.client)


class UserProfileModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
    def test_create_user_profile(self):
        # Check if a profile already exists for the user
        if not UserProfile.objects.filter(user=self.user).exists():
            UserProfile.objects.create(user=self.user)
        else:
            print("Profile already exists for the user.")

        self.assertTrue(UserProfile.objects.filter(user=self.user).exists())
    def test_user_profile_string_representation(self):
        if not UserProfile.objects.filter(user=self.user).exists():
            UserProfile.objects.create(user=self.user)
        else:
            print("Profile already exists for the user.")

        user_profile = UserProfile.objects.get(user=self.user)
        expected_string_representation = f'{self.user.username} Profile'


class EditProfileViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.factory = RequestFactory()

    def test_editprofile_GET(self):
        request = self.factory.get('/editprofile/')
        request.user = self.user
        response = editprofile(request)
        self.assertEqual(response.status_code, 200)

    def test_editprofile_POST(self):
        request = self.factory.post('/editprofile/', data={'some_field': 'some_value'})
        request.user = self.user

class PatientLoginViewTest(TestCase):
    def setUp(self):
        self.url = reverse('patientlogin')
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        Profile.objects.create(user=self.user, is_patient=True)

    def test_patient_login_valid_credentials(self):
        response = self.client.post(self.url, {'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, 302)  # Check for redirect after successful login

    def test_patient_login_invalid_credentials(self):
        response = self.client.post(self.url, {'username': 'invaliduser', 'password': 'invalidpassword'})
        self.assertEqual(response.status_code, 200)  # Check for status code 200 (login form rendered)

    def test_patient_login_no_profile(self):
        self.user.profile.delete()
        response = self.client.post(self.url, {'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, 200)

    def test_patient_login_not_patient(self):
        self.user.profile.is_patient = False
        self.user.profile.save()
        response = self.client.post(self.url, {'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, 200)


class DoctorLoginViewTest(TestCase):
    def setUp(self):
        self.url = reverse('doctorlogin')
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        Profile.objects.create(user=self.user, is_doctor=True)

    def test_doctor_login_valid_credentials(self):
        response = self.client.post(self.url, {'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, 302)

    def test_doctor_login_invalid_credentials(self):
        response = self.client.post(self.url, {'username': 'invaliduser', 'password': 'invalidpassword'})
        self.assertEqual(response.status_code, 200)

    def test_doctor_login_no_profile(self):
        self.user.profile.delete()
        response = self.client.post(self.url, {'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, 200)

    def test_doctor_login_not_doctor(self):
        self.user.profile.is_doctor = False
        self.user.profile.save()
        response = self.client.post(self.url, {'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, 200)

class ChatViewTest(TestCase):
    def test_chat_view(self):
        response = self.client.get(reverse('chat'))


class RoomViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.room = Room.objects.create(name='test_room')

    def test_room_view(self):
        client = Client()
        response = client.get(reverse('room', kwargs={'room': self.room.name}), {'username': self.user.username})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'room.html')
        self.assertEqual(response.context['username'], self.user.username)
        self.assertEqual(response.context['room'], self.room.name)
        self.assertEqual(response.context['room_details'], self.room)

class SendViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.room_id = 1
    def test_send_message(self):
        message_data = {
            'message': 'Test message',
            'username': 'testuser',
            'room_id': self.room_id
        }
        response = self.client.post(reverse('send'), message_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Message.objects.filter(value='Test message', user='testuser', room=self.room_id).exists())

class GetMessagesViewTest(TestCase):
    def setUp(self):
        self.room = Room.objects.create(name='test_room')
        self.user = User.objects.create(username='test_user')
        self.message1 = Message.objects.create(value='Message 1', user=self.user, room=self.room)
        self.message2 = Message.objects.create(value='Message 2', user=self.user, room=self.room)

    def test_get_messages(self):
        response = self.client.get(reverse('getMessages', kwargs={'room': self.room.name}))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('messages', data)
        messages = data['messages']

class BookAppointmentViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')

    def test_book_appointment_POST(self):
        self.client.login(username='testuser', password='testpassword')
        form_data = {
            'appointment_date': '2024-04-10',
            'reason': 'Regular checkup'
        }
        response = self.client.post(reverse('book_appointment'), form_data)


class ViewAppointmentsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.doctor = User.objects.create_user(username='doctor', password='testpassword', email='doctor@example.com')
        self.patient = User.objects.create_user(username='patient', password='testpassword', email='patient@example.com')
        self.client.force_login(self.doctor)
        self.appointment1 = Appointment.objects.create(doctor=self.doctor, patient=self.patient, status='accepted', appointment_time='2024-04-08 10:00:00')
        self.appointment2 = Appointment.objects.create(doctor=self.doctor, patient=self.patient, status='pending', appointment_time='2024-04-09 11:00:00')

    def test_view_appointments(self):
        response = self.client.get(reverse('view_appointments'))
        self.assertEqual(response.status_code, 200)
        appointments = response.context['appointments']
        accepted_appointments_ids = response.context['accepted_appointments_ids']
        self.assertQuerysetEqual(appointments, Appointment.objects.filter(doctor=self.doctor).order_by('appointment_time'), transform=lambda x: x)
        self.assertEqual(list(accepted_appointments_ids), [self.appointment1.id])

class UpdateAppointmentStatusTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.doctor = User.objects.create_user(username='doctor', password='testpassword', email='doctor@example.com')
        self.patient = User.objects.create_user(username='patient', password='testpassword', email='patient@example.com')
        self.client.force_login(self.doctor)
        self.appointment = Appointment.objects.create(doctor=self.doctor, patient=self.patient, status='pending', appointment_time='2024-04-08 10:00:00')

    def test_update_appointment_status_accepted(self):
        response = self.client.post(reverse('update_appointment_status', args=[self.appointment.id, 'accepted']))
        self.assertRedirects(response, reverse('view_appointments'))
        self.appointment.refresh_from_db()
        self.assertEqual(self.appointment.status, 'accepted')

    def test_update_appointment_status_rejected(self):
        response = self.client.post(reverse('update_appointment_status', args=[self.appointment.id, 'rejected']))
        self.assertRedirects(response, reverse('view_appointments'))
        with self.assertRaises(Appointment.DoesNotExist):
            self.appointment.refresh_from_db()


class DeleteAppointmentTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.doctor = User.objects.create_user(username='doctor', password='testpassword', email='doctor@example.com')
        self.patient = User.objects.create_user(username='patient', password='testpassword', email='patient@example.com')
        self.client.force_login(self.doctor)
        self.appointment = Appointment.objects.create(doctor=self.doctor, patient=self.patient, appointment_time='2024-04-08 10:00:00')

    def test_delete_appointment(self):
        initial_count = Appointment.objects.count()
        response = self.client.post(reverse('delete_appointment', args=[self.appointment.id]))
        self.assertRedirects(response, reverse('view_appointments'))
        self.assertEqual(Appointment.objects.count(), initial_count - 1)

class MediaViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword', email='test@example.com')
        self.client.force_login(self.user)

    def test_get_media_page(self):
        response = self.client.get(reverse('media'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'media.html')


class UpdateAppointmentStatusTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.doctor_user = User.objects.create_user(username='doctor', email='doctor@example.com', password='password')
        self.patient_user = User.objects.create_user(username='patient', email='patient@example.com',
                                                     password='password')
        self.appointment = Appointment.objects.create(doctor=self.doctor_user, patient=self.patient_user)

    @patch.object(EmailMessage, 'send')
    @patch('core.views.get_object_or_404')
    def test_rejected_status(self, mock_get_object_or_404, mock_email_send):
        mock_get_object_or_404.return_value = self.appointment
        request = self.factory.post(reverse('update_appointment_status', args=[self.appointment.id, 'rejected']))
        request.user = self.doctor_user
        response = update_appointment_status(request, self.appointment.id, 'rejected')
        self.assertEqual(Notification.objects.count(), 1)
        self.assertEqual(Notification.objects.first().receiver, self.patient_user)
        self.assertTrue(mock_email_send.called)
        self.assertEqual(response.status_code, 302)  # Redirects to view_appointments

    @patch.object(EmailMessage, 'send')
    @patch('core.views.get_object_or_404')
    def test_accepted_status(self, mock_get_object_or_404, mock_email_send):
        mock_get_object_or_404.return_value = self.appointment
        request = self.factory.post(reverse('update_appointment_status', args=[self.appointment.id, 'accepted']))
        request.user = self.doctor_user

        response = update_appointment_status(request, self.appointment.id, 'accepted')

        self.assertEqual(Notification.objects.count(), 1)
        self.assertEqual(Notification.objects.first().receiver, self.patient_user)
        self.assertTrue(mock_email_send.called)
        self.assertEqual(response.status_code, 302)  # Redirects to view_appointments

    @patch('core.views.get_object_or_404')
    def test_invalid_status(self, mock_get_object_or_404):
        mock_get_object_or_404.return_value = self.appointment
        request = self.factory.post(reverse('update_appointment_status', args=[self.appointment.id, 'invalid_status']))
        request.user = self.doctor_user

class NotificationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', email='test@example.com', password='password123')
        self.notification = Notification.objects.create(receiver=self.user, message='Test notification')

    def test_notification_creation(self):
        self.assertEqual(self.notification.receiver, self.user)
        self.assertEqual(self.notification.message, 'Test notification')
        self.assertFalse(self.notification.is_read)
        self.assertIsNotNone(self.notification.created_at)

class SubmitRatingViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = 'django.contrib.messages.middleware.MessageMiddleware'
    def test_submit_rating_post(self):
        user = User.objects.create_user(username='test_user', email='test@example.com', password='password123')
        post_data = {
            'rating': 5,
        }
        request = self.factory.post('/submit-rating/', post_data)
        request.user = user
        request.META['MIDDLEWARE'] = self.middleware
        storage = get_messages(request)
        messages = [str(message) for message in storage]


class RatingsSummaryViewTest(TestCase):
    def test_ratings_summary(self):
        WebsiteRating.objects.create(rating=5)
        WebsiteRating.objects.create(rating=4)
        WebsiteRating.objects.create(rating=3)
        response = self.client.get(reverse('ratings_summary'))
        rating_summaries = response.context['rating_summaries']
        actual_order = list(rating_summaries.values_list('rating', flat=True))
        expected_order = [5, 4, 3]

class ViewDoctorsViewTest(TestCase):
    def setUp(self):
        self.patient_user = User.objects.create_user(username='patient', password='test123')
        self.patient_profile = Profile.objects.create(user=self.patient_user)
        self.doctor_user = User.objects.create_user(username='doctor', password='test456')
        self.doctor_profile = Profile.objects.create(user=self.doctor_user, is_doctor=True, education='MD', roomchat='Room 101')
        self.factory = RequestFactory()

    def test_view_doctors_as_patient(self):
        request = self.factory.get(reverse('view_doctors'))
        request.user = self.patient_user
        response = view_doctors(request)
        self.assertEqual(response.status_code, 200)

class ReportBugViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_report_bug_get(self):
        request = self.factory.get(reverse('report_bug'))
        request.user = self.user
        response = report_bug(request)
        self.assertEqual(response.status_code, 200)

    def test_report_bug_post(self):
        request = self.factory.post(reverse('report_bug'), data={'description': 'Test bug report'})
        request.user = self.user
        response = report_bug(request)


class DeleteBugReportViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.bug_report = BugReport.objects.create(description='Test bug report', user=self.user)

    def test_delete_bug_report(self):
        url = reverse('delete_bug_report', args=[self.bug_report.id])
        request = self.factory.post(url)
        request.user = self.user
        middleware = SessionMiddleware(lambda x: None)
        middleware.process_request(request)
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = delete_bug_report(request, self.bug_report.id)
        self.assertEqual(response.status_code, 302)