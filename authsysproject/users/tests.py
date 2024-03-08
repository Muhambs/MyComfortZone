from django.contrib.auth.models import User
from django.test import TestCase

from authsysproject.users.views import login_user


# Create your tests here.
# class LoginTest(TestCase):
#Dania Ighbaria+Shhd Jbareen
    # def test_login_user_get_request(self):
    #     request = self.factory.get('/login')
    #     response = login_user(request)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'login.html')
    #
    # def test_login_user_post_request_with_valid_credentials(self):
    #     user = User.objects.create_user(username='testuser', password='12345')
    #     self.client.login(username='testuser', password='12345')
    #     request = self.factory.post('/login', {'username': 'testuser', 'password': '12345'})
    #     response = login_user(request)
    #     self.assertEqual(response.status_code, 302)  # Redirect status code
    #     self.assertEqual(response.url, 'profile')
    #
    #
    # def test_login_user_post_request_with_invalid_credentials(self):
    #     request = self.factory.post('/login', {'username': 'wronguser', 'password': 'wrongpass'})
    #     response = login_user(request)
    #     self.assertEqual(response.status_code, 302)  # Redirect status code
    #     self.assertEqual(response.url, 'login')
    #     self.assertIn("wrong username or password", response.content.decode())

    # def test_login_with_unregistered_user(self):
    #     request = self.factory.post('/login', {'username': 'nonexistent', 'password': '12345'})
    #     response = login_user(request)
    #     self.assertEqual(response.status_code, 302)
    #     self.assertEqual(response.url, 'login')

    # def test_redirect_after_successful_login(self):
    #     user = User.objects.create_user(username='testuser2', password='12345')
    #     request = self.factory.post('/login', {'username': 'testuser2', 'password': '12345'})
    #     request.user = user
    #     response = login_user(request)
    #     self.assertRedirects(response, 'profile', status_code=302, target_status_code=200)


# class RegisterTest(TestCase):
    # def test_redirect_after_successful_registration(self):
    #     response = self.client.post('/register/',
    #                                 data={'username': 'user2', 'password1': 'Testpass123', 'password2': 'Testpass123'})
    #     self.assertRedirects(response, 'profile', status_code=302, target_status_code=200)

    # def test_automatic_login_after_registration(self):
    #     self.client.post('/register/',
    #                      data={'username': 'user3', 'password1': 'Testpass123', 'password2': 'Testpass123'})
    #     user = User.objects.get(username='user3')
    #     self.assertEqual(int(self.client.session['_auth_user_id']), user.pk)
    #
    # def test_invalid_registration_data_does_not_create_user(self):
    #     user_count_before = User.objects.count()
    #     response = self.client.post('/register/',
    #                                 data={'username': 'user', 'password1': 'Testpass123', 'password2': 'Wrongpass123'})
    #     user_count_after = User.objects.count()
    #     self.assertEqual(user_count_after, user_count_before)
    #     self.assertTrue('password2' in response.context['form'].errors)
    #
    # def test_valid_registration_data_creates_user(self):
    #     user_count_before = User.objects.count()
    #     response = self.client.post('/register/', data={'username': 'newuser', 'password1': 'Testpass123',
    #                                                     'password2': 'Testpass123'})
    #     user_count_after = User.objects.count()
    #     self.assertEqual(user_count_after, user_count_before + 1)
    #     self.assertRedirects(response, 'profile')
    #
    # def test_registration_page_loads_correctly(self):
    #     response = self.client.get('/register/')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'register.html')
	
	
	
	
	

# class LogoutTest(TestCase):
    # def test_logout_method_is_called(self):
    #     with patch('django.contrib.auth.logout') as mock_logout:
    #         self.client.get('/logout/')
    #         mock_logout.assert_called_once()
    #
    # def test_logout_without_being_logged_in(self):
    #     response = self.client.get('/logout/')
    #     self.assertRedirects(response, '/login/', status_code=302)
    #     user = auth.get_user(self.client)
    #     self.assertTrue(user.is_anonymous)
    #
    # def test_session_is_cleared_after_logout(self):
    #     self.client.login(username='testuser', password='password123')
    #     session_key_before = self.client.session.session_key
    #     self.client.get('/logout/')
    #     session_key_after = self.client.session.session_key
    #     self.assertNotEqual(session_key_before, session_key_after)
    #
    # def test_user_is_logged_out_successfully(self):
    #     self.client.login(username='testuser', password='password123')  # Log in a user
    #     self.client.get('/logout/')  # Logout the user
    #     user = auth.get_user(self.client)
    #     self.assertTrue(user.is_anonymous)
    #
    # def test_logout_redirects_to_login_page(self):
    #     response = self.client.get('/logout/')  # Assuming the logout URL is '/logout/'
    #     self.assertRedirects(response, '/login/', status_code=302, target_status_code=200)