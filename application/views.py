from django_datatables_view.base_datatable_view import BaseDatatableView
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
    get_list_or_404,
    HttpResponse,
)
from .models import *
from .forms import *
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from itertools import chain
from django.db import transaction
from django.utils.html import escape
import pandas as pd
from django.contrib.auth import get_user_model
from authentication.models import User as UserClass
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from application.decorators import custom_permission_required, custom_construction_site_permission_required
from django.utils.translation import gettext_lazy as _


User : UserClass = get_user_model()

@login_required
def unauthorized(request):
    return render(request, "application/pages/unauthorized.html")

@login_required
@custom_permission_required('application.view_constructionsite')
def home(request):
    context = {}
    qs = ConstructionSite.objects.all()
    context["sites"] = qs
    return render(request, "application/pages/home.html", context)

@login_required
@custom_permission_required('authentication.view_user')
def list_users(request):
    context = {}
    users = User.objects.all()
    context["users"] = users
    return render(request, "application/pages/users.html", context)

@login_required
@custom_permission_required('authentication.add_user')
def create_user(request):
    context = {}

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            instance: UserClass = form.save(commit=False)
            instance.set_password(instance.password)
            instance.save()
            form.save_m2m()
            
            return redirect(reverse("create-user"))
        
    form = CreateUserForm()
    context["form"] = form
    return render(request, "application/pages/create-user.html", context)

@login_required
@custom_permission_required('authentication.change_user')
def update_user(request, id):
    context = {}

    instance : UserClass = get_object_or_404(User, pk=id)

    if request.method == "POST":
        form = UpdateUserForm(request.POST, instance=instance)
        if form.is_valid():
            instance: UserClass = form.save(commit=False)
            instance.set_password(instance.password)
            instance.save()
            form.save_m2m()
            return redirect(reverse("update-user", kwargs={'id':instance.pk}))
        
    form = UpdateUserForm(instance=instance)

    context["user"] = instance
    context["form"] = form
    return render(request, "application/pages/update-user.html", context)

@login_required
@custom_permission_required('authentication.delete_user')
def delete_user(request, id):
    instance = get_object_or_404(User, pk=id)
    if request.user != instance:
        instance.delete()
        messages.success(request, "Deleted Successfully")
    else:
        messages.error(request, "Unable to delete because you are trying to delete yourself")
    
    return redirect(reverse("create-user"))


@login_required
@custom_permission_required('application.see_dashboard')
@custom_construction_site_permission_required
def dashboard_constructionsite(request, id):
    context = {}
    print('inside view')
    instance: ConstructionSite = get_object_or_404(ConstructionSite, pk=id)
    context["site"] = instance
    return render(request, "application/pages/dashboard-constructionsite.html", context)


@login_required
@custom_permission_required('application.export_constructionsite')
def export_constructionsite(request, construction_site_id):
    instance: ConstructionSite = get_object_or_404(
        ConstructionSite, pk=construction_site_id
    )

    filename = f"{instance.name}_export.xlsx"

    df = pd.DataFrame(instance.merge_input_output)

    writer = pd.ExcelWriter(filename, engine="xlsxwriter")

    df.to_excel(writer, sheet_name="Sheet1", index=False)

    writer.close()

    with open(filename, "rb") as file:
        response = HttpResponse(file.read(), content_type="application/vnd.ms-excel")
        response["Content-Disposition"] = f"attachment; filename={filename}"
        return response


@login_required
@custom_permission_required('application.export_inputs')
def export_inputs(request):
    df = pd.DataFrame(
        list( 
            Input.objects.select_related("construction_site").values(
                "id",
                "date",
                "product__name",
                "unity",
                #"initial_stock",
                "qty_input",
                "source",
                "numeroCon",
                "bonrecept",
                "comments",
                "construction_site__name",
            )
        )
    )
    filename = f"inputs_export.xlsx"

    writer = pd.ExcelWriter(filename, engine="xlsxwriter")

    df.to_excel(writer, sheet_name="Sheet1", index=False)

    writer.close()

    with open(filename, "rb") as file:
        response = HttpResponse(file.read(), content_type="application/vnd.ms-excel")
        response["Content-Disposition"] = f"attachment; filename={filename}"
        return response


@login_required
@custom_permission_required('application.export_outputs')
def export_outputs(request):
    df = pd.DataFrame(
        list(
            Output.objects.select_related("construction_site").values(
                "date",
                "product__name",
                "unity",
                "qty_output",
                "level",
                "appartment",
                "exit_coupon",
                "construction_site__name",
            )
        )
    )
    filename = f"outputs_export.xlsx"

    writer = pd.ExcelWriter(filename, engine="xlsxwriter")

    df.to_excel(writer, sheet_name="Sheet1", index=False)

    writer.close()

    with open(filename, "rb") as file:
        response = HttpResponse(file.read(), content_type="application/vnd.ms-excel")
        response["Content-Disposition"] = f"attachment; filename={filename}"
        return response


@login_required
@custom_permission_required('application.view_category')
def category_page(request):
    return render(request, "application/pages/categories.html")


@login_required
@custom_permission_required('application.add_category')
def create_category(request):
    form = CategoryForm()

    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse("categories"))

    return render(request, "application/pages/category-form.html", {"form": form})


@login_required
@custom_permission_required('application.change_category')
def edit_category(request, id):
    instance = get_object_or_404(Category, pk=id)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect(reverse("categories"))
    else:
        form = CategoryForm(instance=instance)
    return render(request, "application/pages/category-form.html", {"form": form})


@login_required
@custom_permission_required('application.delete_category')
def delete_category(request, id):
    instance = get_object_or_404(Category, pk=id)
    instance.delete()

    return redirect(reverse("categories"))


class CategoryListJson(BaseDatatableView):
    model = Category
    columns = ["name"]
    # order_columns = ["-id"]

    max_display_length = 100

    def filter_queryset(self, qs):
        search = self.request.GET.get("search[value]", None)
        return super().filter_queryset(qs)


@login_required
@custom_permission_required('application.view_product')
def product_page(request):
    return render(request, "application/pages/products.html")


@login_required
@custom_permission_required('application.add_product')
def create_product(request):
    form = ProductForm()

    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse("products"))

    return render(request, "application/pages/product-form.html", {"form": form})


@login_required
@custom_permission_required('application.change_product')
def edit_product(request, id):
    instance = get_object_or_404(Product, pk=id)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect(reverse("products"))
    else:
        form = ProductForm(instance=instance)
    return render(request, "application/pages/product-form.html", {"form": form})


@login_required
@custom_permission_required('application.delete_product')
def delete_product(request, id):
    instance = get_object_or_404(Product, pk=id)
    instance.delete()

    return redirect(reverse("products"))


class ProductListJson(BaseDatatableView):
    model = Product
    #columns = ["name", "reference" "category"]
    # order_columns = ["-id"]
   



    max_display_length = 100

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(Q(name__contains=search))
        return qs
    def get_filter_method(self):
        return self.FILTER_ICONTAINS
    # def filter_method(self):

    #     return self.FILTER_ICONTAINS


@login_required
@custom_permission_required('application.view_input')
def input_page(request):
    return render(request, "application/pages/inputs.html")


@login_required
@custom_permission_required('application.add_input')
def create_input(request, construction_site_id):
    form = InputForm()

    if request.method == "POST":
        form = InputForm(request.POST)
        if form.is_valid():
            instance: Input = form.save(commit=False)
            instance.construction_site = get_object_or_404(
                ConstructionSite, pk=construction_site_id
            )
            instance.save()
            return redirect(reverse("inputs"))

    return render(request, "application/pages/input-form.html", {"form": form})


@login_required
@custom_permission_required('application.change_input')
def edit_input(request, id):
    instance = get_object_or_404(Input, pk=id)
    if request.method == "POST":
        form = InputForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect(reverse("inputs"))
    else:
        form = InputForm(instance=instance)
    return render(request, "application/pages/input-form.html", {"form": form})


@login_required
@custom_permission_required('application.delete_input')
def delete_input(request, id):
    instance = get_object_or_404(Input, pk=id)
    instance.delete()

    return redirect(reverse("inputs"))


class InputListJson(BaseDatatableView):
    model = Input
    # columns = ["name", "reference" "category"]
    # order_columns = ["-id"]

    max_display_length = 100

    def render_column(self, row, column):
        # We want to render user as a custom column
        if column == "category":
            # escape HTML for security reasons
            print(row.product.category)
            return escape("{0}".format(row.product.category))
        else:
            return super(InputListJson, self).render_column(row, column)

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(product__name__contains=search)

        return qs
@login_required
@custom_permission_required('application.view_output')
def output_page(request):
    return render(request, "application/pages/outputs.html")


@login_required
@custom_permission_required('application.add_output')
def create_output(request, construction_site_id):
    form = OutputForm()

    if request.method == "POST":
        form = OutputForm(request.POST)
        if form.is_valid():
            instance: Output = form.save(commit=False)
            instance.construction_site = get_object_or_404(
                ConstructionSite, pk=construction_site_id
            )
            instance.save()
            return redirect(reverse("outputs"))

    return render(request, "application/pages/output-form.html", {"form": form})


@login_required
@custom_permission_required('application.change_output')
def edit_output(request, id):
    instance = get_object_or_404(Output, pk=id)
    if request.method == "POST":
        form = OutputForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect(reverse("outputs"))
    else:
        form = OutputForm(instance=instance)
    return render(request, "application/pages/output-form.html", {"form": form})


@login_required
@custom_permission_required('application.delete_output')
def delete_output(request, id):
    instance = get_object_or_404(Output, pk=id)
    instance.delete()

    return redirect(reverse("outputs"))


class OutputListJson(BaseDatatableView):
    model = Output
    # columns = ["name", "reference" "category"]
    # order_columns = ["-id"]

    max_display_length = 100

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(product__name__contains=search)

        return qs

@login_required
@custom_permission_required('application.view_stock')
def stocks_page(request):
    return render(request, "application/pages/stocks.html")


@login_required
@custom_permission_required('application.add_stock')
def create_stock(request):
    form = StockForm()

    if request.method == "POST":
        form = StockForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse("stocks"))

    return render(request, "application/pages/stock-form.html", {"form": form})


@login_required
@custom_permission_required('application.change_stock')
def edit_stock(request, id):
    instance = get_object_or_404(Stock, pk=id)
    if request.method == "POST":
        form = StockForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect(reverse("stocks"))
    else:
        form = StockForm(instance=instance)
    return render(request, "application/pages/stock-form.html", {"form": form})


@login_required
@custom_permission_required('application.delete_stock')
def delete_stock(request, id):
    instance = get_object_or_404(Stock, pk=id)
    instance.delete()

    return redirect(reverse("stocks"))


class StockListJson(BaseDatatableView):
    model = Stock
    # columns = ["name", "reference" "category"]
    # order_columns = ["-id"]

    max_display_length = 100

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        #print("search value is ", search)
        if search:
            qs = qs.filter(product__name__contains=search)

        return qs

@login_required
@custom_permission_required('application.add_constructionsite')
def create_construction_site(request):
    form = ConstructionSiteForm()

    if request.method == "POST":
        form = ConstructionSiteForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse("home"))

    return render(
        request, "application/pages/constructionsite-form.html", {"form": form}
    )


@login_required
@custom_permission_required('application.change_constructionsite')
def edit_constructionsite(request, id):
    instance = get_object_or_404(ConstructionSite, pk=id)
    if request.method == "POST":
        form = ConstructionSiteForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect(reverse("home"))
    else:
        form = ConstructionSiteForm(instance=instance)
    return render(
        request, "application/pages/constructionsite-form.html", {"form": form}
    )


@login_required
@custom_permission_required('application.delete_constructionsite')
def delete_constructionsite(request, id):
    instance = get_object_or_404(ConstructionSite, pk=id)
    instance.delete()

    return redirect(reverse("home"))


@login_required
def construction_access(request, id):
    context = {}
    # instance = get_object_or_404(ConstructionPermission, user=id)
    user_id = User.objects.get(id=id)
    try:
        instance = ConstructionPermission.objects.get(user=user_id)
    except ConstructionPermission.DoesNotExist:
        instance = ConstructionPermission(user=user_id)
        instance.save()

    if request.method == "POST":
        form = ConstructionpermissionForm(request.POST or None, instance = instance)
        if form.is_valid():
            form.save()
        context["form"] = form
        return render(request, 'application/pages/Constructionsite-access.html', context)
    form = ConstructionpermissionForm(instance=instance)
    context["form"] = form
    return render(request, 'application/pages/Constructionsite-access.html', context)


@login_required
def ConstructionsiteInput(request, id):
    try:
        input_data = ConstructionSite.objects.get(pk=id)
        site_input_data = Input.objects.filter(construction_site=input_data.id)
        return render(request, 'application/pages/Constructionsite-input.html',{"site_input_data":site_input_data})
    except:
        pass

    return render(request,'application/pages/Constructionsite-input.html')

@login_required
def ConstructionsiteOutput(request, id):
    try:
        output_data = ConstructionSite.objects.get(pk=id)
        site_output_data = Output.objects.filter(construction_site=output_data.id)
        return render(request, 'application/pages/Constructionsite-output.html',{"site_output_data":site_output_data})
    except:
        pass

    return render(request,'application/pages/Constructionsite-output.html')