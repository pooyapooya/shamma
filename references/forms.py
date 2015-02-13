from django import forms
from django.forms import model_to_dict
from references.models import Reference


class CreateReferenceForm(forms.ModelForm):
    class Meta:
        model = Reference
        fields = ('name', 'url', 'description', 'reference_type')

    reference_type = forms.ChoiceField(choices=Reference.get_type_choices())

    def clean_reference_type(self):
        data = self.cleaned_data['reference_type']
        print self.instance
        return data

    def save(self, commit=True):
        ret = super(CreateReferenceForm, self).save(commit=False)
        if commit:
            reference_type = self.cleaned_data['reference_type']
            model_class = Reference.get_type_mapping()[reference_type]
            kwargs = model_to_dict(ret)
            ret = model_class(**kwargs)
            ret.save()
        return ret

