from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from .models import Quest, User, Contact, Answer_response
from .forms import MyUserCreationForm, CreateQuestForm, UserForm


def loginPage(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "email or password does not exist")

    context = {"page": page}
    return render(request, "base/login.html", context)


def logoutUser(request):
    logout(request)
    return redirect("home")


def registerPage(request):
    form = MyUserCreationForm()

    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = user.email.lower()
            user.username = user.email
            user.save()
            login(request, user)
            return redirect("home")
        else:
            messages.error(
                request,
                "An error occurred during registration. Your email might be already is use or your password does not meet the requirements. Password must contain at least 1 capital letter, 1 number, can't be to similar to name/email and  and should consist of at least 8 characters. ",
            )

    context = {"form": form}
    return render(request, "base/register.html", context)


def home(request):
    # quests = Quest.objects.all()
    users = User.objects.all()

    q = request.GET.get("q") if request.GET.get("q") != None else ""

    quests = Quest.objects.filter(Q(name__icontains=q))

    set_of_completed = set()
    for quest in quests:
        if request.user in quest.users.all():
            set_of_completed.add(quest.id)

    quest_count = quests.count()

    context = {
        "quests": quests,
        "users": users,
        "set_of_completed": set_of_completed,
        "quest_count": quest_count,
    }
    return render(request, "base/home.html", context)


def ranking(request):
    users = User.objects.all()
    context = {"users": users}
    return render(request, "base/ranking.html", context)


@login_required(login_url="login")
def quest(request, pk):
    quest = Quest.objects.get(id=pk)

    users = quest.users.all()

    completed = False
    if request.method == "POST":
        quest.users.add(request.user)

        response = "Unfortunately, your answer was wrong"
        if request.POST.get("body").lower() == quest.answer.lower():
            request.user.all_time_score += quest.value
            request.user.current_score += quest.value
            response = "Congratulations! Your answer was correct!"

        Answer_response.objects.create(
            user=request.user, quest=quest, response=response
        )

        quest.save()
        request.user.save()

    if request.user in users:
        completed = True

    response = ""
    for i in Answer_response.objects.all():
        if i.user == request.user and i.quest == quest:
            response = i.response

    context = {"quest": quest, "completed": completed, "response": response}
    return render(request, "base/quest.html", context)


@login_required(login_url="login")
def createQuest(request):
    form = CreateQuestForm()
    if request.method == "POST":
        form = CreateQuestForm(request.POST, request.FILES)
        # Quest.objects.create(
        #     creator=request.user,
        #     name=request.POST.get("name"),
        #     question=request.POST.get("question"),
        #     image=request.POST.get("image"),
        #     audio=request.POST.get("audio"),
        #     answer=request.POST.get("answer"),
        #     value=request.POST.get("value"),
        # )

        if form.is_valid():
            quest = form.save(commit=False)
            quest.creator = request.user
            form.save()
            return redirect("home")

    context = {"form": form}
    return render(request, "base/create_quest.html", context)


@login_required(login_url="login")
def editQuest(request, pk):
    quest = Quest.objects.get(id=pk)
    form = CreateQuestForm(instance=quest)
    context = {"form": form}
    if request.method == "POST":
        form = CreateQuestForm(request.POST, request.FILES, instance=quest)
        if form.is_valid():
            form.save()
            return redirect("home")
    return render(request, "base/create_quest.html", context)


def deleteQuest(request, pk):
    quest = Quest.objects.get(id=pk)

    if request.method == "POST":
        for i in Answer_response.objects.all():
            if (
                i.user == request.user
                and i.quest == quest
                and i.response == "Congratulations! Your answer was correct!"
            ):
                request.user.current_score -= quest.value

        request.user.save()
        quest.delete()

        return redirect("home")

    context = {"obj": quest}
    return render(request, "base/delete.html", context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)

    if request.method == "POST":
        Contact.objects.create(
            follows=user,
            followed_by=request.user,
        )

    follows = set()
    followed_by = set()
    for contact in Contact.objects.all():
        if contact.followed_by == user:
            follows.add(contact.follows)
        if contact.follows == user:
            followed_by.add(contact.followed_by)
    context = {"user": user, "followed_by": followed_by, "follows": follows}
    return render(request, "base/profile.html", context)


def followPage(request, pk):
    user = User.objects.get(id=pk)
    follows = set()
    followed_by = set()
    for contact in Contact.objects.all():
        if contact.followed_by == user:
            follows.add(contact.follows)
        if contact.follows == user:
            followed_by.add(contact.followed_by)
    context = {"user": user, "followed_by": followed_by, "follows": follows}
    return render(request, "base/followPage.html", context)


def editUser(request, pk):
    user = request.user
    form = UserForm(instance=user)

    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("user-profile", pk=user.id)

    context = {"form": form}
    return render(request, "base/edit-user.html", context)


###
