from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import URLForm
from .models import ShortenedURL


def home(request):
  if request.method == "POST":
    form = URLForm(request.POST)
    if form.is_valid():
      url = form.cleaned_data["url"]

      existing_url = ShortenedURL.objects.filter(url=url).first()
      if existing_url:
        shortened_url = existing_url
      else:
        shortened_url = ShortenedURL.objects.create(url=url)

      short_url = request.build_absolute_uri(
        reverse("redirect_url", args=[shortened_url.short_url])
      )

      return render(
        request,
        "home.html",
        {"form": URLForm(), "short_url": short_url, "url": url},
      )
  else:
    form = URLForm()

  return render(request, "home.html", {"form": form})


def redirect_url(request, short_url):
  url_obj = get_object_or_404(ShortenedURL, short_url=short_url)
  url_obj.click_count += 1
  url_obj.save()
  return redirect(url_obj.url)


def url_stats(request, short_url):
  url_obj = get_object_or_404(ShortenedURL, short_url=short_url)
  return render(request, "stats.html", {"url_obj": url_obj})
