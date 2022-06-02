from django.contrib import admin

from Apps.Movie.models import Movie, MovieImage

# Register your models here.

class MovieAdmin(admin.ModelAdmin):
    readonly_fields = ("rating", "count_reviews", "created_at", "updated_at")

class MovieImageAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "updated_at")


admin.site.register(Movie, MovieAdmin)
admin.site.register(MovieImage, MovieImageAdmin)
