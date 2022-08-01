from django.apps import apps
from django.http import JsonResponse
from django.views import View


class ChangeStateView(View):
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        transition_name = kwargs.get("transition")
        instance = self.get_object()
        if not hasattr(instance, transition_name):
            return JsonResponse(
                {"error": "The transition %s does not exists." % transition_name},
                status=400,
            )
        transition = getattr(instance, transition_name)
        transition(**self.get_kwargs_transition())
        instance.save()
        return JsonResponse(
            {"message": "The transition %s executed successfully" % transition_name},
            status=200,
        )

    def get_kwargs_transition(self):
        return {"user": self.request.user}

    def get_object(self):
        app_name = self.kwargs.get("app")
        model_name = self.kwargs.get("model")
        pk_or_slug = self.kwargs.get("pk")
        model_class = apps.get_model(app_name, model_name)
        return model_class.objects.get(pk=pk_or_slug)
