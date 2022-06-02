from django.db import models
from uuid import uuid4

# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    resume = models.TextField()
    rating = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)
    count_reviews = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{0} - {1}".format(self.title, self.year)

    class Meta:
        db_table = 'movies'

def movie_images_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/movie_id/<filename>
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid4(), ext)
    return 'movie_{0}/{1}'.format(instance.movie_id, filename)

class MovieImage(models.Model):
    path = models.FileField(upload_to=movie_images_directory_path)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='images')
    is_feature = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{0} - {1}".format(self.path, self.movie_id)

    class Meta:
        db_table = 'movie_images'

    # Function to delete the MovieImage in the storage folder
    def delete(self, using=None, keep_parents=False):
        self.path.storage.delete(self.path.name)
        super().delete()
