from django.shortcuts import redirect
from functools import wraps


def superuser_required(to, *args, **kwargs):
    def decorator(func):
        @wraps(func)
        def wrapper(request):
            user = request.user
            if user is None or not user.is_superuser:
                return redirect(to, *args, **kwargs)
            return func(request)

        return wrapper

    return decorator
