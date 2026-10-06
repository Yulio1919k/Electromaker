from django.db import models


class Platform(models.Model):
    name = models.CharField(max_length=80)
    description = models.TextField()
    image_url = models.URLField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Project(models.Model):
    DIFFICULTY = [('Easy', 'Easy'), ('Moderate', 'Moderate'), ('Difficult', 'Difficult'), ('Expert', 'Expert')]
    title = models.CharField(max_length=200)
    summary = models.TextField()
    author = models.CharField(max_length=60)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY)
    category = models.CharField(max_length=60)
    platform = models.ForeignKey(Platform, null=True, blank=True, on_delete=models.SET_NULL)
    image_url = models.URLField(blank=True)

    class Meta:
        ordering = ['-id']

    @property
    def badge(self):
        return self.difficulty

    def __str__(self):
        return self.title


class Post(models.Model):
    """Entradas del blog y de los videos (el campo tag define la sección de Videos)."""
    title = models.CharField(max_length=200)
    summary = models.TextField()
    author = models.CharField(max_length=60)
    kind = models.CharField('type', max_length=20)
    category = models.CharField(max_length=60)
    platform = models.ForeignKey(Platform, null=True, blank=True, on_delete=models.SET_NULL)
    tag = models.CharField(max_length=20, blank=True, help_text='potw, educator, podcast o vacío')
    image_url = models.URLField(blank=True)

    class Meta:
        ordering = ['-id']

    @property
    def badge(self):
        return self.kind

    def __str__(self):
        return self.title
