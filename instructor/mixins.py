from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator

def tagged_view(tag):
    def wrapper(cls):
        methods = ['get', 'post', 'put', 'patch', 'delete']
        for method in methods:
            if hasattr(cls, method):
                cls = method_decorator(
                    swagger_auto_schema(tags=[tag]),
                    name=method
                )(cls)
        return cls
    return wrapper
