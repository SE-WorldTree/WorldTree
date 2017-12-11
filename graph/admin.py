from django.contrib import admin

# Register your models here.
from graph.models import edge, node

admin.site.register(node)
admin.site.register(edge)
