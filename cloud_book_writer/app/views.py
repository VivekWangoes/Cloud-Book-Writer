from django.shortcuts import render, redirect
from django.views import View
from .forms import (
    UserSignUp,
    UserLogin,
    AddBook,
    AddSection,
    SectionForm,
)  # , AddSubSection, AddSubSectionLink
from django.contrib.auth import login, authenticate, logout
from .models import BookModel, Section
from django.db.models import Q
from config.permissions import CustomLoginAuthor, CustomLoginCollaborator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http.response import JsonResponse

# Create your views here.


class SignUp(View):
    def get(self, request):
        form = UserSignUp()
        return render(request, "sign-up.html", {"form": form})

    def post(self, request):
        form = UserSignUp(request.POST)
        role = request.POST["roles"]
        if form.is_valid():
            user = form.save()
            user.groups = role
            user.save()
            return redirect("login")
        return redirect("/")


class Login(View):
    def get(self, request):
        form = UserLogin()
        return render(request, "login.html", {"form": form})

    def post(self, request):
        form = UserLogin(request.POST)
        email = request.POST["email"]
        password = request.POST["password"]
        if form.is_valid():
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                if user.roles == "Author":
                    return redirect("author")
                return redirect("collab")
        return redirect("login")


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("/")


class Author(CustomLoginAuthor, View):
    def get(self, request):
        book = BookModel.objects.filter(author=request.user)
        return render(request, "author.html", {"book": book})


class CreateBook(CustomLoginAuthor, View):
    def get(self, request, id=None):
        if id:
            book = BookModel.objects.filter(id=id).first()
            initial_collaborator = [
                collaborator.id for collaborator in book.collaborators.all()
            ]
            form = AddBook(
                user=request.user,
                initial={"title": book.title, "collaborators": initial_collaborator},
            )
            return render(request, "addbook.html", {"form": form})
        form = AddBook(user=request.user)
        return render(request, "addbook.html", {"form": form})

    def post(self, request, id=None):
        # add Book
        if id != None:
            form = AddBook(request.POST, user=request.user)
            if form.is_valid():
                user = form.save(commit=False)
                user.author = request.user
                user.save()

        else:
            book = BookModel.objects.filter(id=id).first()
            form = AddBook(request.POST, user=request.user, instance=book)
            if form.is_valid():
                user = form.save(commit=False)
                user.author = request.user
                user.save()
        return redirect("create-book")


class CreateSection(CustomLoginAuthor, View):
    def get(self, request):
        form = AddSection(user=request.user)
        return render(request, "section.html", {"form": form})

    def post(self, request):
        form = AddSection(request.POST, user=request.user)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            print(cleaned_data)
            model = Section(**cleaned_data)
            model.save()
            return redirect("author")
        return redirect("section")


class Collaborator(CustomLoginCollaborator, View):
    def get(self, request):
        # get list of books he is collaborating on
        books = BookModel.objects.filter(collaborators=request.user)
        context = {"books": books}
        return render(request, "collab.html", context)

    def post(self, request):
        pass


class Book(LoginRequiredMixin, View):
    def get(self, request, id=None):
        if id:
            books = BookModel.objects.filter(id=id)
            if books:
                return render(request, "book.html", {"books": books})
        else:
            books = BookModel.objects.filter(
                Q(author=request.user) | Q(collaborators=request.user)
            )
            return render(request, "book.html", {"books": books})


class ViewEditSection(LoginRequiredMixin, View):
    def get(self, request, id=None):
        if id:
            section = Section.objects.get(id=id)
            form = SectionForm(
                initial={"title": section.title, "content": section.content}
            )
            context = {"section": section, "form": form}
            return render(request, "section.html", context)

    def post(self, request, id=None):
        section = Section.objects.filter(id=id).first()
        form = SectionForm(request.POST, instance=section)
        if form.is_valid():
            form.save()
            if request.user.roles == "Author":
                return redirect("author")
            return redirect("collab")
        return redirect("edit-section")


from django.core import serializers


def load_sections(request):
    book_id = request.GET.get("book_id")
    book = BookModel.objects.filter(id=book_id).first()
    sections = book.sections.values("id", "title")
    return JsonResponse(list(sections), safe=False)


def get_related_sections(section):
    related_sections = Section.objects.filter(
        Q(id=section.id)
        | Q(parent=section)
        | Q(parent__parent=section)
        | Q(parent__parent__parent=section)
    )
    return related_sections
