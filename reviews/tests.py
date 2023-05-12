from django.test import TestCase
from django.urls import reverse
from faker import Faker
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from reviews.models import Review
from reviews.serializers import ReviewSerializer

# Create your tests here.


class ReviewsCreateTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {"email": "kyu@mail.com", "password":"123","nickname":"nick"}
        cls.review_data = {"title":"제목!","content":"내용","movie_code":222222,"movie_title":"가오갤3"}
        cls.user = User.objects.create_user("kyu@mail.com","123","nick")

    def setUp(self):
        self.access_token = self.client.post(reverse("token_obtain_pair"), self.user_data).data["access"]

    def test_fail_if_not_logged_in(self):
        url = reverse("review_list", args=[100])
        response = self.client.post(url, self.review_data)
        self.assertEqual(response.status_code, 401)

    def test_create_review(self):
        response = self.client.post(
            path=reverse("review_list", args=[100]),
            data=self.review_data,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )
        
        self.assertEqual(response.status_code, 200)

class ReviewReadTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.faker = Faker()
        cls.reviews = []
        for i in range(10):
            cls.user = User.objects.create_user(cls.faker.email(),cls.faker.word(),cls.faker.name())
            cls.reviews.append(Review.objects.create(title=cls.faker.sentence(),content=cls.faker.text(),user=cls.user))

    def test_get_review(self):
        for review in self.reviews:
            url = review.get_absolute_url()
            response = self.client.get(url)
            serializer = ReviewSerializer(review).data
            for key, value in serializer.items():
                self.assertEqual(response.data[key], value)