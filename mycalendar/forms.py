from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm, UserCreationForm, PasswordChangeForm
)
from django.contrib.auth import get_user_model
from .models import Schedule
import datetime


class BS4ScheduleForm(forms.ModelForm):
    """Bootstrapに対応するためのModelForm"""

    class Meta:
        model = Schedule
        fields = ('LargeItem','MiddleItem','SmallItem','kosu','summary', 'memo')#, 'start_time', 'end_time')

        # widgets = {
        #     'summary': forms.TextInput(attrs={
        #         'class': 'form-control',
        #     }),
        #     'description': forms.Textarea(attrs={
        #         'class': 'form-control',
        #     }),
        #     'start_time': forms.TextInput(attrs={
        #         'class': 'form-control',
        #     }),
        #     'end_time': forms.TextInput(attrs={
        #         'class': 'form-control',
        #     }),
        # }

    # def clean_end_time(self):
    #     start_time = self.cleaned_data['start_time']
    #     end_time = self.cleaned_data['end_time']
    #     if end_time <= start_time:
    #         raise forms.ValidationError(
    #             '終了時間は、開始時間よりも後にしてください'
    #         )
    #     return end_time


BS4ScheduleNewFormSet = forms.modelformset_factory(
    Schedule, form=BS4ScheduleForm, extra=5
)

BS4ScheduleEditFormSet = forms.modelformset_factory(
    Schedule, form=BS4ScheduleForm, extra=0, can_delete=True
)



class MyPasswordChangeForm(PasswordChangeForm):
    """パスワード変更フォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'  # Bootstrap4対応