from django.contrib.auth.models import User
from django.test import TestCase

from authsysproject.users.views import login_user


# Create your tests here.
# class LoginTest(TestCase):


 
 
 
 
 
 
# class RegisterTest(TestCase):
    
	
	
	
	
	

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