from django.contrib import messages
from django.shortcuts import redirect
from .models import ConstructionPermission,ConstructionSite
decorator_with_arguments = lambda decorator: lambda *args, **kwargs: lambda func: decorator(func, *args, **kwargs)

@decorator_with_arguments
def custom_permission_required(function, perm):
    def _function(request, *args, **kwargs):
        if request.user.has_perm(perm):
            return function(request, *args, **kwargs)
        else:
            # messages.error(request, "You are not authorized to access thtis page")
            # request.user.message_set.create(message = "What are you doing here?!")
            # Return a response or redirect to referrer or some page of your choice
            return redirect("/unauthorized")
    return _function


# @decorator_with_arguments
def custom_construction_site_permission_required(function):
    def _function(request,*args, **kwargs):
        construction_site = ConstructionSite.objects.get(id = kwargs['id'])
        print(kwargs)
        perm = ConstructionPermission.objects.filter(user = request.user,constructionsite_permission=construction_site)
        print(perm)
        user_has_permission = True if perm else False
        if user_has_permission:
            return function(request, *args, **kwargs)
        else:
            # messages.error(request, "You are not authorized to access thtis page")
            # request.user.message_set.create(message = "What are you doing here?!")
            # Return a response or redirect to referrer or some page of your choice
            return redirect("/unauthorized")
    return _function

# def dec_with_arg(decorator):
#     def
