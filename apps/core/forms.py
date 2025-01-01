from django import forms
from django_ace import AceWidget

from apps.core.models import Goal


class GoalForm(forms.ModelForm):
    json = forms.JSONField(widget=AceWidget(mode='json'))

    class Meta:
        model = Goal
        fields = '__all__'
