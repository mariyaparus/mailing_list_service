from django import forms

from mailing.models import Client, Message, Mailing


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'


class MessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Message
        fields = '__all__'


class MailingForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Mailing
        fields = '__all__'
        exclude = ('user',)
        widgets = {
            'message': forms.Select,
            'client': forms.CheckboxSelectMultiple,
        }


class MailingModeratorForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['status', ]
