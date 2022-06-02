from django.contrib import admin

from Apps.UserActions.models import Favorite, Review

# Register your models here.

class ReviewAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "updated_at")

class MovieFavoriteAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "updated_at")


admin.site.register(Review, ReviewAdmin)
admin.site.register(Favorite, MovieFavoriteAdmin)
