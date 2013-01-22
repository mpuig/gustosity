# -*- coding: utf-8 -*-

from django.conf.urls.defaults import url, patterns

from apps.contact_form import views, forms

urlpatterns = patterns('', url(r'^$',
                       views.ContactFormView.as_view(template_name='contact_form/contact.html',
                       form_class=forms.BasicContactForm), name='contact'), url(r'^completed/$',
                       views.CompletedPage.as_view(), name='completed'))
