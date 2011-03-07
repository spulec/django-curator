from django import forms

from dashboard.models import DashboardWidget

class DashboardWidgetForm(forms.ModelForm):

    class Meta:
        model = DashboardWidget

    """
    def __init__(self, *args, **kwargs):
        super(DashboardWidgetForm, self).__init__(*args, **kwargs)
       
        if kwargs.has_key('instance'):
            self.fields['datetime_field'] = forms.ChoiceField(choices=(), widget=forms.Select)
            instance = kwargs['instance']
            self.fields['datetime_field'].choices = instance.get_datetime_fields()
    """
