from django.contrib import admin

from .models import Modules, Articles, ArticleDetail, Comment, Favour

# Register your models here.

admin.site.register(Modules)
admin.site.register(Articles)
admin.site.register(ArticleDetail)
admin.site.register(Comment)
admin.site.register(Favour)