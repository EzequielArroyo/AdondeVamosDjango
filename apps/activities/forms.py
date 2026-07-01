from django import forms
from apps.activities.models import Activity


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['title', 'description', 'date', 'location', 'max_participants']
        
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "date": forms.DateTimeInput(
                attrs={"type": "datetime-local", "class": "form-control"}
            ),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "max_participants": forms.NumberInput(attrs={"class": "form-control", "min": 1})
        }