from django import forms

from . import choices


class QueryForm(forms.Form):
    people = forms.ChoiceField(choices=choices.PEOPLE, label='Search for', required=False)
    gender = forms.ChoiceField(choices=choices.GENDER, label='Gender', required=False)
    interested_in = forms.ChoiceField(choices=choices.INTERESTED_IN, label='Interested in', required=False)
    relationship = forms.ChoiceField(choices=choices.RELATIONSHIP, label='Relationship status', required=False)
    interest = forms.CharField(max_length=100, required=False)
    location = forms.ChoiceField(choices=choices.LOCATION, label='Location', required=False)
    location_query = forms.CharField(max_length=100, required=False)
    company = forms.ChoiceField(choices=choices.COMPANY, label='Company', required=False)
    company_query = forms.CharField(max_length=100, required=False)
    school = forms.ChoiceField(choices=choices.SCHOOL, label='School', required=False)
    school_query = forms.CharField(max_length=100, required=False)
    job_title = forms.CharField(max_length=100, required=False)
    language = forms.CharField(max_length=100, required=False)
    major = forms.CharField(max_length=100, required=False)
    born = forms.ChoiceField(choices=choices.BORN, label='Born', required=False)
    # Date
    born_year = forms.CharField(max_length=100, required=False)
    born_month = forms.ChoiceField(choices=choices.MONTHS, label='Month', required=False)
    # Range
    born_range_from = forms.CharField(max_length=100, required=False)
    born_range_to = forms.CharField(max_length=100, required=False)
    name = forms.CharField(max_length=100, required=False)
    limit = forms.CharField(max_length=100, required=False)
