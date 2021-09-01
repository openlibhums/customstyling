from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib import messages

from plugins.customstyling import forms, models
from journal import models as jm


def manager(request):
    template = 'customstyling/manager.html'
    context = {
        'journals': jm.Journal.objects.all(),
    }

    return render(request, template, context)


def manage_css(request, journal_id):
    journal = get_object_or_404(
        jm.Journal,
        pk=journal_id,
    )
    custom_styling, c = models.CustomStyling.objects.get_or_create(
        journal=journal,
    )
    form = forms.StylingForm(
        instance=custom_styling,
    )
    if request.POST:
        form = forms.StylingForm(
            request.POST,
            instance=custom_styling,
        )
        if form.is_valid():
            custom_styling = form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                'Saved.',
            )
            custom_styling.write_to_disk()
            return redirect(
                reverse(
                    'customstyling_manage_css',
                    kwargs={
                        'journal_id': journal.pk,
                    }
                )
            )
    template = 'customstyling/manage_css.html'
    context = {
        'journal': journal,
        'custom_styling': custom_styling,
        'form': form,
    }
    return render(request, template, context)
