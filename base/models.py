from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import validate_file_size


class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True, blank=True)
    all_time_score = models.DecimalField(max_digits=100, decimal_places=0, default=0)
    current_score = models.DecimalField(max_digits=100, decimal_places=0, default=0)
    avatar = models.ImageField(
        null=True, default="avatar.svg", validators=[validate_file_size]
    )

    # following = models.ManyToManyField("self", blank=True)

    USERNAME_FIELD = (
        "email"  # comment this line while creating superUser bcs username is necessary
    )
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ["-current_score", "-all_time_score", "-name"]


class Contact(models.Model):
    follows = models.ForeignKey(
        User, related_name="rel_from_set", on_delete=models.CASCADE, null=True
    )
    followed_by = models.ForeignKey(
        User, related_name="rel_to_set", on_delete=models.CASCADE, null=True
    )
    created = models.DateTimeField(auto_now_add=True, db_index=True)


class Quest(models.Model):
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    #
    users = models.ManyToManyField(User, related_name="users", blank=True)
    value = models.DecimalField(max_digits=4, decimal_places=0, default=250)
    name = models.CharField(max_length=200)
    question = models.TextField(default="question")
    answer = models.TextField(default="answer")
    # text_answer = models.TextField(null=True, blank=True)
    #
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    #
    image = models.FileField(null=True, blank=True, validators=[validate_file_size])
    audio = models.FileField(null=True, blank=True, validators=[validate_file_size])

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-created", "-updated"]


class Answer_response(models.Model):
    user = models.ForeignKey(
        User, related_name="user", on_delete=models.CASCADE, null=True
    )
    quest = models.ForeignKey(
        Quest, related_name="quest", on_delete=models.CASCADE, null=True
    )
    response = models.TextField(default="")
