from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Quest, User


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["name", "email", "password1", "password2"]


class CreateQuestForm(ModelForm):
    class Meta:
        model = Quest
        fields = ["name", "question", "image", "audio", "answer", "value"]
        # fields = "__all__"
        # exclude = ["host", "participants"]


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["avatar", "name", "email", "bio"]
