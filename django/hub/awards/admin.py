from django.contrib import admin
from models import Award


class AwardAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_display', 'created_at')

    def image_display(self, obj):
        return '<img src="{}" width="50" height="50" />'.format(obj.image.url)
    image_display.short_description = u'Imagem'
    image_display.allow_tags = True

admin.site.register(Award, AwardAdmin)
