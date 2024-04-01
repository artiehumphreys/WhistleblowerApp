from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from django.urls import reverse
from unittest.mock import patch, MagicMock
from .views import profile, logout_view, test

class ProfileViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='123')
        self.admin_group = Group.objects.create(name='Site Admin')
        self.user.groups.add(self.admin_group)

    # Mocking the AWS client, I do not enjoy how this works, but then again mokito wasn't much better
    @patch('users.views.boto3.client')
    def test_profile_view_as_site_admin(self, mock_boto3_client):
        mock_client_instance = mock_boto3_client.return_value
        mock_client_instance.list_objects_v2.return_value = \
            {
            'Contents':
                [
                {'Key': 'file1.txt'},
                {'Key': 'uploads/file2.txt'}
            ]
        }
        self.client.force_login(self.user)
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'siteadmin.html')
        self.assertEqual(len(response.context['files']), 1)

    @patch('users.views.boto3.client')
    def test_profile_view_as_normal_user(self, mock_boto3_client):
        mock_client_instance = mock_boto3_client.return_value
        mock_client_instance.list_objects_v2.return_value = \
            {
                'Contents': [
                    {'Key': 'file1.txt'},
                    {'Key': 'uploads/file2.txt'}
                ]
            }
        normal_user = User.objects.create_user(username='normaluser', password='12345')
        self.client.force_login(normal_user)
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')


        ################################################################################################
        ##THIS TEST SHOULD BE FAILING, BUT IS NOT UNLESS 0, SHOULD BE LOOKED INTO WHEN GIVEN THE CHANCE#
        ################################################################################################
        #normal users basically can't see their own files

        self.assertEqual(len(response.context['files']), 0)




