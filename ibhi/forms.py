from django import forms

class ArcherExplorerForm(forms.Form):
    api_key = forms.CharField()
    rows = forms.CharField()
    query = forms.CharField(widget=forms.Textarea)
    start_date_field = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    end_date_field = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))