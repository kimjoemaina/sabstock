from django import forms
from .models import *
from django_select2 import forms as s2forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from bootstrap_datepicker_plus import widgets as date_widgets
from django.utils.translation import gettext as _
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class NameWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "name__icontains",
    ]


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class CreateUserForm(forms.ModelForm):
    user_permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.filter(
            Q(content_type__app_label="application")
            | Q(content_type__app_label="authentication"),
        ),
        widget=s2forms.Select2MultipleWidget,
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "user_permissions", "password"]


class UpdateUserForm(forms.ModelForm):
    user_permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.filter(
            Q(content_type__app_label="application")
            | Q(content_type__app_label="authentication"),
        ),
        widget=s2forms.Select2MultipleWidget,
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "user_permissions"]


class InputForm(forms.ModelForm):
    # date = forms.DateField(widget=DateTimePickerInput())

    class Meta:
        model = Input
        exclude = ["construction_site"]
        widgets = {
            "product": NameWidget,
            "date": date_widgets.DatePickerInput(options={"format": "MM/DD/YYYY"}),
        }


class OutputForm(forms.ModelForm):
    class Meta:
        model = Output
        exclude = ["construction_site"]
        widgets = {
            "product": NameWidget,
            "date": date_widgets.DatePickerInput(options={"format": "MM/DD/YYYY"}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        widgets = {
            "category": NameWidget,
           
        }


class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = "__all__"
        widgets = {
            "product": NameWidget,
        }


class ConstructionSiteForm(forms.ModelForm):
    class Meta:
        model = ConstructionSite
        fields = ["name"]


class ConstructionpermissionForm(forms.ModelForm):
    constructionsite_permission = forms.ModelMultipleChoiceField(
        queryset=ConstructionSite.objects.all(),
        widget=s2forms.Select2MultipleWidget,
    )
    user = forms.ModelChoiceField(queryset=User.objects.all(),disabled=True)

    class Meta:
        model = ConstructionPermission
        fields = ["user", "constructionsite_permission"]