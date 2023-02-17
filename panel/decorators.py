from django.shortcuts import redirect


def unAuthenticatedUser(funct):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            return funct(request, *args, **kwargs)

    return wrapper_func