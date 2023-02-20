from django.views.generic import View , TemplateView
from django.http import FileResponse , Http404
from django.conf import settings

import os

class PdfView(View):
    def get(self, request):
        file_path = os.path.join(settings.BASE_DIR,'static','docs','protocolo_alba', 'example.pdf')

        with open(file_path, 'rb') as pdf:
            try:
                return FileResponse(open(file_path, 'rb'), content_type='application/pdf')
            except FileNotFoundError:
                raise Http404()
            

class ProtocoloAlbaView(TemplateView):
    template_name = 'web/paginas/protocoloalba/protocoloalba.html'
