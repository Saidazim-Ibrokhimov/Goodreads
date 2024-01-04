from django.contrib import admin
from .models import *

# Register your models here.

class BookAdmin(admin.ModelAdmin):
	search_fields = ('title', 'isbn',)
	prepopulated_fields = {'slug':('title',)}

admin.site.register(Book, BookAdmin)


class EditionsAdmin(admin.ModelAdmin):
	pass 

admin.site.register(Editions, EditionsAdmin)


class AuthorAdmin(admin.ModelAdmin):
	search_fields = ('author__first_name', 'author__last_name')
	prepopulated_fields = {'slug':('first_name', 'last_name')}

admin.site.register(Author, AuthorAdmin)


class BookAuthorAdmin(admin.ModelAdmin):
	search_fields = ('author__first_name', 'author__last_name', 'book__title')

admin.site.register(BookAuthor, BookAuthorAdmin)


class BookReviewAdmin(admin.ModelAdmin):
	search_fields = ('user__username', 'book__title')

admin.site.register(BookReview, BookReviewAdmin)


class GenreAdmin(admin.ModelAdmin):
	search_fields = ('name',)

admin.site.register(Genre, GenreAdmin)


class BookGenreAdmin(admin.ModelAdmin):
	search_fields = ('book__title', 'genre__genre_name')

admin.site.register(BookGenre, BookGenreAdmin)

class ShelfAdmin(admin.ModelAdmin):
	search_fields = ('name', 'default_shelf',)
	list_display = ('name',)

admin.site.register(Shelf, ShelfAdmin)

class BookOnShelfAdmin(admin.ModelAdmin):
	search_fields = ('book__title', 'shelf__name',)


admin.site.register(BookOnShelf, BookOnShelfAdmin)