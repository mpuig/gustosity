# -*- coding: utf-8 -*-

from django import forms
from apps.account.models import UserProfile


class UserProfileForm(forms.ModelForm):

    first_name = forms.CharField(label=u'First name', max_length=30, required=False)

    last_name = forms.CharField(label=u'Last name', max_length=30, required=False)

    class Meta:

        # fields = ('first_name',)
        exclude = 'user', 'account_type'
        model = UserProfile

    def __init__(self, *args, **kw):
        """ A bit of hackery to get the first name and last name at the top of the form instead
            at the end. """
        super(UserProfileForm, self).__init__(*args, **kw)
        self.fields['first_name'].initial = self.instance.user.first_name
        self.fields['last_name'].initial = self.instance.user.last_name

        # Put the first and last name at the top
        new_order = self.fields.keyOrder[:-2]
        new_order.insert(0, 'first_name')
        new_order.insert(1, 'last_name')
        self.fields.keyOrder = new_order

    def save(self, *args, **kw):
        """ Override the save method to save the first and last name to the user field. """
        super(UserProfileForm, self).save(*args, **kw)
        self.instance.user.first_name = self.cleaned_data.get('first_name')
        self.instance.user.last_name = self.cleaned_data.get('last_name')
        self.instance.user.save()
