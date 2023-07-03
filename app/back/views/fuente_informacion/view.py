from django.shortcuts import render, redirect, get_object_or_404
from back.models import *
from django.views.generic import ListView, TemplateView


class FuentesInfoView (TemplateView):

    template_name = 'back/fuente-informacion/list.html'
    # context_object_name = 'fuentes_informacion'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Fuentes de información'
        context['d_route'] = 'Fuentes de información > Dashboard'
        return context    