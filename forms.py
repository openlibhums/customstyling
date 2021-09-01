from django import forms

from plugins.customstyling import models


class StylingForm(forms.ModelForm):
    class Meta:
        model = models.CustomStyling
        exclude = ('journal',)
