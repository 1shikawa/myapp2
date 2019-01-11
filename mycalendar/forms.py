from django import forms
from .models import Schedule


class BS4ScheduleForm(forms.ModelForm):
    """Bootstrapに対応するためのModelForm"""

    class Meta:
        model = Schedule
        fields = ('LargeItem', 'MiddleItem', 'SmallItem', 'kosu', 'summary', 'memo')  # , 'start_time', 'end_time')

        # すべてのfieldのclass属性に'form-control'を指定する
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field in self.fields.values():
                field.widget.attrs['class'] = 'form-control'  # Bootstrap4対応

        # widgets = {
        #     'SmallItem': forms.CharField(attrs={
        #         'class': 'form-control',
        #     }),
        # }

        # def clean_end_time(self):
        #     kosu = self.cleaned_data['kosu']
        #     if kosu <= 1:
        #         raise forms.ValidationError(
        #             '工数は2以上で入れてね'
        #         )
        #     return kosu


# 一括新規登録用のFormSet
BS4ScheduleNewFormSet = forms.modelformset_factory(
    Schedule, form=BS4ScheduleForm, extra=5
)

# 一括編集用のFormSet
BS4ScheduleEditFormSet = forms.modelformset_factory(
    Schedule, form=BS4ScheduleForm, extra=0, can_delete=True
)
