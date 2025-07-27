from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator


class URLForm(forms.Form):
  url = forms.URLField(
    max_length=2000,
    widget=forms.URLInput(
      attrs={
        "class": "form-control",
        "placeholder": "Enter your URL here...",
        "required": True,
      }
    ),
    label="URL to Shorten",
  )

  def clean_url(self):
    url = self.cleaned_data["url"]
    if not url.startswith(("http://", "https://")):
      url = "https://" + url

    validator = URLValidator()
    try:
      validator(url)
    except ValidationError:
      raise forms.ValidationError("Please enter a valid URL.")

    return url
