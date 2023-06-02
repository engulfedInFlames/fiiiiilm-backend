from django.urls import reverse
from rest_framework.test import APITestCase
from users.models import User


# class ReviewsCreateTest(APITestCase):
#     @classmethod
#     def setUpTestData(cls):
#         cls.user_data = {"email": "kyu@mail.com", "password": "123"}
#         cls.review_data = {
#             "title": "kyu title",
#             "content": "내요오오옹",
#             "movie_code": 2222222,
#         }
#         cls.user = User.objects.create_user("kyu@mail.com", "123")

#     def setUp(self):
#         self.access_token = self.client.post(
#             reverse("token_obtain_pair"), self.user_data
#         ).data["access"]

#     def test_fail_if_not_logged_in(self):
#         url = reverse("review_list")
#         response = self.client.post(url, self.review_data)
#         self.assertEqual(response.status_code, 401)

#     def test_create_review(self):
#         response = self.client.post(
#             path=reverse("review_list"),
#             data=self.review_data,
#             HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
#         )
#         self.assertEqual(response.data["message"], "작성완료")
#         self.assertEqual(response.status_code, 200)
