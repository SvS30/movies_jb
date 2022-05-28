from django.contrib import admin

from Apps.Genre.models import Genre, GenreMovie

# Register your models here.

class GenreAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "updated_at")

class GenreMovieAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "updated_at")

admin.site.register(Genre, GenreAdmin)
admin.site.register(GenreMovie, GenreMovieAdmin)