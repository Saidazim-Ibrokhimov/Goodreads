from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug':('title',)}


admin.site.register(Category)
admin.site.register(PostCategory)

