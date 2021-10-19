from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required

from plugins.customstyling import forms, models
from journal import models as jm


@staff_member_required
def manager(request):
    cjs_list = models.CrossJournalStylesheet.objects.all()
    template = 'customstyling/manager.html'
    if request.journal:
        return redirect(reverse(
            'customstyling_manage_css',
            kwargs={'journal_id': request.journal.pk},
        ))

    context = {
        'journals': jm.Journal.objects.all(),
        'cjs_list': cjs_list,
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


@staff_member_required
def manage_press_css(request):
    form = forms.StylingForm()
    if request.POST:
        form = forms.StylingForm(
            request.POST,
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
                    'customstyling_manage_press_css',
                )
            )

    template = 'customstyling/manage_css.html'
    context = {
        'form': form,
    }
    return render(request, template, context)


@staff_member_required
def manage_cross_journal_stylesheets(request, stylesheet_id=None):
    stylesheet = None
    if stylesheet_id:
        stylesheet = get_object_or_404(
            models.CrossJournalStylesheet,
            pk=stylesheet_id,
        )
    form = forms.CrossJournalStylingForm(
        instance=stylesheet,
    )
    if request.POST:
        form = forms.CrossJournalStylingForm(
            request.POST,
            instance=stylesheet,
        )
        if form.is_valid():
            stylesheet = form.save()
            form.save_m2m()

            return redirect(
                reverse(
                    'customstyling_edit_lcjsc',
                    kwargs={
                        'stylesheet_id': stylesheet.pk,
                    }
                )
            )

    template = 'customstyling/manage_cross_journal_stylesheet.html'
    context = {
        'stylesheet': stylesheet,
        'form': form,
    }
    return render(
        request,
        template,
        context,
    )
