from django import forms

class ArcherExplorerForm(forms.Form):
    api_key = forms.CharField()
    rows = forms.CharField()
    query = forms.CharField(widget=forms.Textarea)
