from django import forms
from django.forms import DateTimeInput

from main.models import Client, Mails

class StyleForm:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name in ('scheduled', 'end'):
                field.widget = DateTimeInput(attrs={'type': 'datetime-local', 'class' : 'form-control'})
            else:
                field.widget.attrs['class'] = 'form-control'
class UserForm(StyleForm, forms.ModelForm):

    class Meta:
        model = Client
        fields = ('avatar', 'name', 'email', 'comment')

class MailForm(StyleForm, forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['users'].queryset = Client.objects.filter(author=user)

    users = forms.ModelMultipleChoiceField(queryset=Client.objects.none(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Mails
        fields = ('users', 'theme', 'body', 'scheduled', 'periodic', 'end')

    def clean_periodic(self):
        cleaned_data = self.cleaned_data.get('periodic')

        if cleaned_data and cleaned_data > 360:
            raise forms.ValidationError('Значение не может быть больше 360')

        return cleaned_data

    def clean(self):
        cleaned_data = super().clean()
        field1 = cleaned_data.get('periodic')
        field2 = cleaned_data.get('end')

        if field1 and not field2:
            raise forms.ValidationError("Для использования периодичной рассылки требуется указание времени окончания рассылки")

        if field2 and not field1:
            raise forms.ValidationError("Интервал между рассылками не указан")

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.dynamic_periodic = self.cleaned_data['periodic']
        if commit:
            instance.save()
        return instance

class MailUpdateForm(StyleForm, forms.ModelForm):

    class Meta:
        model = Mails
        fields = ('theme', 'body',)