from django.contrib import admin
from . models import Category,Option,Question,Quiz

# Register your models here.

admin.site.register(Category)
admin.site.register(Option)
admin.site.register(Question)
admin.site.register(Quiz)
