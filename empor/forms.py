from django.forms.models import BaseModelFormSet

class RequiredFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super(RequiredFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False
