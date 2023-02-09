from django.db import models
from django.forms import model_to_dict

class Publications(models.Model):
    section = models.CharField(max_length=100, verbose_name="Sección")
    category = models.CharField(max_length=100, verbose_name="Categoria")
    publication = models.BooleanField(default=True)
    visible =  models.BooleanField(default=True)
    recent = models.BooleanField(default=True)
    type = models.CharField(max_length=100, verbose_name="Tipo")
    download = models.CharField(max_length=100, verbose_name="Descarga")
    name = models.CharField(max_length=100, verbose_name="Nombre")
    fiel = models.FileField(upload_to='archivo/%y/%m/%d', null=True, blank=True)
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.publication
    
    def toJSON(self):
        item = model_to_dict(self)
        return item


    class Meta:
        verbose_name = 'Publicación'
        verbose_name_plural = 'Publicaciones'
        db_table = 'publications'
        ordering = ['-id']
