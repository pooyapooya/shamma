from django import forms
from django.forms import model_to_dict
from tinymce.widgets import TinyMCE
from references.models import Reference


class CreateReferenceForm(forms.ModelForm):
    class Meta:
        model = Reference
        fields = ('reference_type', 'name', 'url', 'description',)
        widgets = {
            'description': TinyMCE(),
        }

    reference_type = forms.ChoiceField(choices=Reference.get_type_choices(), widget=forms.RadioSelect())

    def save(self, commit=True):
        ret = super(CreateReferenceForm, self).save(commit=False)
        if commit:
            reference_type = self.cleaned_data['reference_type']
            model_class = Reference.get_type_mapping()[reference_type]
            kwargs = model_to_dict(ret)
            ret = model_class(**kwargs)
            ret.save()
        return ret

