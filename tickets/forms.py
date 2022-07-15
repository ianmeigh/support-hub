from django import forms
from .models import Ticket
from django_summernote.fields import SummernoteWidget


# Ticket Creation Form for Staff
class StaffTicketCreationForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = (
            "type",
            "category",
            "title",
            "description",
            "ticket_image",
        )

        widgets = {
            "description": SummernoteWidget(),
        }
