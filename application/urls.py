from django.conf import settings
from django.urls import path
from .views import *


urlpatterns = [
    path("", home, name="home"),
    path("unauthorized", unauthorized, name="unauthorized"),
    path("users/", list_users, name="users"),
    path("create-user/", create_user, name="create-user"),
    path("update-user/<int:id>/", update_user, name="update-user"),
    path("delete-user/<int:id>/", delete_user, name="delete-user"),
    path("constructionsite-access/<int:id>/", construction_access, name="constructionsite-access"),
    path("constructionsite-input/<int:id>/", ConstructionsiteInput, name="constructionsite-input"),
    path("constructionsite-output/<int:id>/", ConstructionsiteOutput, name="constructionsite-output"),
    path(
        "constructionsite/create",
        create_construction_site,
        name="create-constructionsite",
    ),
    path(
        "constructionsite/edit/<int:id>/",
        edit_constructionsite,
        name="edit-constructionsite",
    ),
    path(
        "constructionsite/delete/<int:id>/",
        delete_constructionsite,
        name="delete-constructionsite",
    ),
    path(
        "dashboard/constructionsite/<int:id>/",
        dashboard_constructionsite,
        name="dashboard-constructionsite",
    ),
    path(
        "export/constructionsite/<int:construction_site_id>/",
        export_constructionsite,
        name="export-construction-site",
    ),
    path("categories/", category_page, name="categories"),
    path("categories/create", create_category, name="create-category"),
    path("categories/edit/<int:id>/", edit_category, name="edit-category"),
    path("categories/delete/<int:id>/", delete_category, name="delete-category"),
    path(
        "categories_list_json/",
        CategoryListJson.as_view(),
        name="category_list_json",
    ),
    path("products/", product_page, name="products"),
    path("products/create", create_product, name="create-product"),
    path("products/edit/<int:id>/", edit_product, name="edit-product"),
    path("products/delete/<int:id>/", delete_product, name="delete-product"),
    path(
        "products_list_json/",
        ProductListJson.as_view(),
        name="products_list_json",
    ),
    path("inputs/", input_page, name="inputs"),
    path("inputs/export/", export_inputs, name="export-inputs"),
    path("inputs/<int:construction_site_id>/create", create_input, name="create-input"),
    path("inputs/edit/<int:id>/", edit_input, name="edit-input"),
    path("inputs/delete/<int:id>/", delete_input, name="delete-input"),
    path(
        "inputs_list_json/",
        InputListJson.as_view(),
        name="inputs_list_json",
    ),
    path("outputs/", output_page, name="outputs"),
    path("outputs/export/", export_outputs, name="export-outputs"),
    path(
        "outputs/<int:construction_site_id>/create", create_output, name="create-output"
    ),
    path("outputs/edit/<int:id>/", edit_output, name="edit-output"),
    path("outputs/delete/<int:id>/", delete_output, name="delete-output"),
    path(
        "outputs_list_json/",
        OutputListJson.as_view(),
        name="outputs_list_json",
    ),
    path("stocks/", stocks_page, name="stocks"),
    path("stocks/create", create_stock, name="create-stock"),
    path("stocks/edit/<int:id>/", edit_stock, name="edit-stock"),
    path("stocks/delete/<int:id>/", delete_stock, name="delete-stock"),
    path(
        "stocks_list_json/",
        StockListJson.as_view(),
        name="stocks_list_json",
    ),
]
