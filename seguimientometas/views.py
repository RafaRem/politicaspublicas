from django.views.generic import TemplateView


class RenderView(TemplateView):
    template_name = ".html"
