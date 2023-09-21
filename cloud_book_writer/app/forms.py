from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, BookModel, Section  # Subsection, SubsectionLink


class UserSignUp(UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "password1", "password2", "roles"]


class UserLogin(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class AddBook(ModelForm):
    class Meta:
        model = BookModel
        fields = ["title", "subtitle", "collaborators"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields["collaborators"].queryset = User.objects.exclude(id=user.id)


class AddSection(forms.Form):
    title = forms.CharField()
    book = forms.ModelChoiceField(queryset=BookModel.objects.none())
    parent = forms.ModelChoiceField(queryset=Section.objects.none(), required=False)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields["book"].queryset = BookModel.objects.filter(author=user.id)


class SectionForm(ModelForm):
    class Meta:
        model = Section
        fields = ["title", "content"]


# class AddSubSection(ModelForm):

#     class Meta:
#         model = Subsection
#         fields = "__all__"


# class AddSubSectionLink(ModelForm):

#     class Meta:
#         model = SubsectionLink
#         fields = "__all__"
