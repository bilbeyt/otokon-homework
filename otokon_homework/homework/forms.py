from homework.models import AnswerSheet
from django import forms


class AnswerSheetCreateForm(forms.ModelForm):
    class Meta:
        model = AnswerSheet
        fields = ("comment", "answers",)


class AnswerSheetUpdateForm(forms.ModelForm):
    class Meta:
        model = AnswerSheet
        fields = ("comment", "answers",)
