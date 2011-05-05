from django import forms

from curator.models import DashboardWidget
from curator.utils import get_datetime_fields

class DashboardWidgetForm(forms.ModelForm):

    class Meta:
        model = DashboardWidget
        exclude = ('order', 'height', 'width')
        widgets = {
            'datetime_field': forms.Select(),
        }
    """    
    def __init__(self, *args, **kwargs):
        super(DashboardWidgetForm, self).__init__(*args, **kwargs)
       
        if kwargs.has_key('instance'):
            self.fields['datetime_field'] = forms.ChoiceField(choices=(), widget=forms.Select)
            instance = kwargs['instance']
            self.fields['datetime_field'].choices = get_datetime_fields(instance.model)
    """
