from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required

from plugins.customstyling import forms
from journal import models as jm


@staff_member_required
def manager(request):
    template = 'customstyling/manager.html'
    if request.journal:
        return redirect(reverse(
            'customstyling_manage_css',
            kwargs={ 'journal_id': request.journal.pk},
        ))

    context = {
        'journals': jm.Journal.objects.all(),
    }

    return render(request, template, context)


@staff_member_required
def manage_css(request, journal_id):
    journal = get_object_or_404(
        jm.Journal,
        pk=journal_id,
    )
    form = forms.StylingForm(
        journal=journal
    )
    if request.POST:
        form = forms.StylingForm(
            request.POST,
            journal=journal
        )
        if form.is_valid():
            form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                'Saved.',
            )
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
        'form': form,
    }
    return render(request, template, context)
