from django.test import TestCase
from django.urls import reverse
from accounts.models import CustomUser
from .models import Post
import secrets
import logging


def get_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger


logger = get_logger()


class HomePageTests(TestCase):

    def test_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('index'))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('index'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_home_page_contains_correct_html(self):
        response = self.client.get('/')
        self.assertContains(response, '<title>DataTau - Hacker News Clone - Data Science Newsboard</title>')

    def test_home_page_does_not_contain_incorrect_html(self):
        response = self.client.get('/')
        self.assertNotContains(
            response, 'Hi there! I should not be on the page.')


class ActionsTest(TestCase):

    def test_create_posts(self):

        logger.info('testing creating posts')

        user = CustomUser.objects.create(username=f"test_post",
                                         password=f"test_post")
        user.save()

        logger.info(f'testing creating posts for user: {user.username}')

        for i in range(100):
            title = secrets.token_urlsafe(50)
            url = 'https://test_site.test_domain/' + secrets.token_urlsafe(50)
            logger.info(f'creating post with title: {title} and url: {url}')

            post = Post(title=title,
                        url=url,
                        user=user)

            post.save()

    def test_create_users(self):
        for i in range(100):
            logger.info(f'creating test user {i}')
            user = CustomUser.objects.create(username=f"test_user_{i}",
                                             password=f"test_password_{i}")
            user.save()
