from django.views.generic import TemplateView
from web.models import BarometroTuristico 

class Eniot(TemplateView):
    template_name = 'web/paginas/eniot/eniot.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pdf =  most_recent_register = BarometroTuristico.objects.latest('fecha_registro')
        distinct_years = BarometroTuristico.objects.values('yearPDF').distinct().order_by('yearPDF')
        years_list = [item['yearPDF'] for item in distinct_years]
        context['years'] = years_list
        context['pdf'] = pdf
        return context