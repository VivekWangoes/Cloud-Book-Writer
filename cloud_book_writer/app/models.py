from django.db import models
from .managers import UserManager
from django.contrib.auth.models import AbstractUser


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    ROLES = (
        ("Author", "Author"),
        ("Collaborator", "Collaborator"),
    )

    username = None
    email = models.EmailField(unique=True)
    roles = models.CharField(max_length=12, choices=ROLES, default="Author")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    object = UserManager()

    def __str__(self):
        return self.email


class BookModel(BaseModel):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    collaborators = models.ManyToManyField(User, related_name="collaborated_books")

    def __str__(self):
        return self.title


class Section(models.Model):
    title = models.CharField(max_length=100)
    book = models.ForeignKey(
        BookModel, on_delete=models.CASCADE, related_name="sections"
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="subsections",
    )
    content = models.TextField()

    def __str__(self):
        return self.title
