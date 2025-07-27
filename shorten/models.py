import random
import string

from django.db import models


class ShortenedURL(models.Model):
  url = models.URLField(max_length=2000)
  short_url = models.CharField(max_length=10, unique=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  click_count = models.PositiveIntegerField(default=0)

  def save(self, *args, **kwargs):
    if not self.short_url:
      self.short_url = self.generate_short_url()
    super().save(*args, **kwargs)

  def generate_short_url(self):
    length = 6
    characters = string.ascii_letters + string.digits
    while True:
      short_url = "".join(random.choice(characters) for _ in range(length))
      if not ShortenedURL.objects.filter(short_url=short_url).exists():
        return short_url

  def __str__(self):
    return f"{self.url} -> {self.short_url}"
