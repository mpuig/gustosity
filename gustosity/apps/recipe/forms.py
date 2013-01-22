# encoding: utf-8
from django import forms
from apps.recipe.models import Recipe, Step


class RecipeForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'span12'}))
    summary = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'span12'}))
    source = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'span12'}))
    #servings = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'span2'}))
    #num_portions = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'span2'}))
    #prep_minutes = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'span2'}))
    #cook_minutes = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'span2'}))
    #inactive_prep_minutes = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'span2'}))

    class Meta:
        model = Recipe
        exclude = ('created_at', 'user', 'username', 'total_views', 'total_likes',
            'slug', 'ingredients', 'tips',)

    def get_form_kwargs(self):
        # pass "user" keyword argument with the current user to your form
        kwargs = super(RecipeForm, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class RecipeDetailsForm(forms.ModelForm):

    class Meta:
        model = Recipe
        exclude = ('created_at', 'user', 'username', 'total_views', 'total_likes',
            'slug', 'name', 'summary', 'source', 'original_image', 'tips')


class StepForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'input-xxlarge'}))
    hash = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = Step
        exclude = ('recipe', 'order',)
