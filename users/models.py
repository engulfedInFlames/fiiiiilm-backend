from django.db import models
from django.conf import settings
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


"""
User 모델 수정하면 좋을 사항
1. AbstractBaseUser vs AbstractUser
ID로 username을 쓸 것인지, 이메일을 사용할 것인지 혹은 필드 몇 개 추가하는 간단한 수정이 필요할 때는 AbstracUser를 사용하고, 완전히 새로운 User 모델을 생성하고 싶을 때는 AbstractBaseUser를 사용한다.

2. 오버라이딩
has_perms, has_module_perms와 같은 메소드를 오버라이딩 하는 것이 아니라면 굳이 코드를 명기할 필요가 없다.

"""


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )

    nickname = models.CharField("닉네임", max_length=20, unique=True)
    intro = models.TextField("자기소개", null=True, blank=True)
    profile_img = models.ImageField("프로필 이미지", blank=True, upload_to="media/profile_img/%Y/%m", default="default.png")
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    following = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="followers",
        blank=True,
        verbose_name="팔로워",
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "User"

    def __str__(self):
        return self.nickname

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin
