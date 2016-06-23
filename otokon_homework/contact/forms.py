from django import forms
from contact.models import Message


class MessageCreateForm(forms.ModelForm):
    class Meta:
        model = Message
        exclude = ["send_user", "to_user", "slug", "is_answered"]


class MessageUpdateForm(forms.ModelForm):
    class Meta:
        model = Message
        exclude = ["send_user", "to_user", "slug", "is_answered"]
