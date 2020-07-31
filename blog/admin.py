from django.contrib import admin
from blog.models import Post,Blogcomment
# Register your models here.

admin.site.register(Blogcomment)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    class Media:
        js = ('tinyinject.js',)
