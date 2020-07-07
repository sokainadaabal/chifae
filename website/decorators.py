from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def wrapper_func(request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else :
            return view_func(request,*args,**kwargs)
    return wrapper_func

def admin_only(view_func):
    def wrapper_func(request,*args,**kwargs):
            if request.user.activite =="emp":
             return redirect('homeP')
            if request.user.activite == "cl":
              return redirect('homeC')
            else :
              return view_func(request,*args,**kwargs)
    return wrapper_func
