import random
from django.urls import reverse
from rest_framework.test import APITestCase
from faker import Faker

from .models import User


class UserAPITest(APITestCase):
    @classmethod
    def setUpTestData(self):
        """
        클래스 변수 USER_DATA를 바탕으로 `USER`에 `User` 객체를 할당합니다. 또한, `test_follow_user` 함수를 위해서 10명의 사용자를 임의 생성합니다.
        """
        self.faker = Faker()

        self.USER_DATA = {
            "email": self.faker.free_email(),
            "password": self.faker.pystr(),
            "nickname": self.faker.profile(fields=["username"]).get("username"),
            "intro": self.faker.sentence(),
            "avatar": self.faker.image_url(),
        }

        created_user = User.objects.create_user(
            email=self.USER_DATA["email"],
            password=self.USER_DATA["password"],
        )
        self.USER = created_user

    def test_from_signup_to_update_user(self):
        """
        회원가입 기능, 토큰 기반 로그인 기능, 사용자 정보 업데이트 기능을 테스트합니다.
        """

        # 회원가입 기능을 테스트합니다.
        user_email = self.faker.free_email()
        user_password = self.faker.pystr()
        request_user_data = {
            "email": user_email,
            "password1": user_password,
            "password2": user_password,
            "nickname": self.faker.profile(fields=["username"]).get("username"),
            "intro": self.faker.sentence(),
            "avatar": self.faker.image_url(),
        }

        url = reverse("user_view")
        response = self.client.post(
            url,
            request_user_data,
        )
        self.assertEqual(response.status_code, 201)

        # 토큰 기반 로그인 기능을 테스트합니다.
        url = reverse("token_obtain_pair")
        response = self.client.post(
            url,
            {
                "email": user_email,
                "password": user_password,
            },
        )
        keys = response.json().keys()
        self.assertEqual("access" in keys, True)

        # 사용자 정보 업데이트 기능을 테스트합니다.
        access_token = (response.json())["access"]
        not_updated_user = User.objects.get(email=user_email)

        new_user_password = self.faker.pystr()
        new_request_user_data = {
            "password1": user_password,
            "password2": new_user_password,
            "nickname": self.faker.profile(fields=["username"]).get("username"),
            "intro": self.faker.sentence(),
            "avatar": self.faker.image_url(),
        }

        not_updated_user_pk = not_updated_user.pk
        url = reverse(
            "user_detail_view",
            kwargs={"pk": not_updated_user_pk},
        )
        response = self.client.put(
            url,
            new_request_user_data,
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )

        updated_user = User.objects.get(email=user_email)

        self.assertEqual(
            response.status_code,
            200,
        )
        self.assertEqual(
            updated_user.check_password(new_user_password),
            True,
        )
        self.assertEqual(
            updated_user.nickname,
            new_request_user_data["nickname"],
        )
        self.assertEqual(
            updated_user.intro,
            new_request_user_data["intro"],
        )
        self.assertEqual(
            updated_user.avatar,
            new_request_user_data["avatar"],
        )

    def test_get_me(self):
        """
        사용자 데이터를 가지고 올 수 있는지를 테스트합니다.
        """

        url = reverse("token_obtain_pair")
        response = self.client.post(
            url,
            {
                "email": self.USER_DATA["email"],
                "password": self.USER_DATA["password"],
            },
        )
        access_token = (response.json())["access"]

        url = reverse("me")
        response = self.client.get(
            url,
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        keys = (response.json()).keys()
        self.assertEqual("pk" in keys, True)

    def test_follow_user(self):
        """
        `setUp`에서 생성된 10명의 사용자들을 대상으로 팔로우 기능을 테스트합니다.
        """

        for _ in range(10):
            User.objects.create(
                email=self.faker.free_email(),
                password=self.faker.pystr(),
                nickname=self.faker.profile(fields=["username"]).get("username"),
                intro=self.faker.sentence(),
                avatar=self.faker.image_url(),
            )

        # 권한 획득을 위해 액세스 토큰을 받아 옵니다.
        url = reverse("token_obtain_pair")
        response = self.client.post(
            url,
            {
                "email": self.USER_DATA["email"],
                "password": self.USER_DATA["password"],
            },
        )

        access_token = (response.json())["access"]

        start = 1
        end = User.objects.count()
        count = random.randint(start, end)
        user_pk_list = []

        for _ in range(count):
            random_pk = random.randint(start, end)
            user_pk_list.append(random_pk)

        # 팔로우 기능을 테스트합니다.
        for pk in user_pk_list:
            url = reverse(
                "follow_view",
                kwargs={"pk": pk},
            )
            response = self.client.get(
                url,
                HTTP_AUTHORIZATION=f"Bearer {access_token}",
            )
            self.assertEqual(response.status_code, 200)

        # 팔로우 취소 기능을 테스트합니다.
        for pk in user_pk_list:
            url = reverse(
                "follow_view",
                kwargs={"pk": pk},
            )
            response = self.client.get(
                url,
                HTTP_AUTHORIZATION=f"Bearer {access_token}",
            )
            self.assertEqual(response.status_code, 200)
