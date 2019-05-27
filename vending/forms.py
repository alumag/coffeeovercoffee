from django import forms

from vending.models import CoffeeType

class CustomModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name

class OrderCoffeeForm(forms.Form):
    customer_name = forms.CharField(label='Your name', max_length=100, widget=forms.TextInput(attrs={"class":"input100"}))
    coffee_type = CustomModelChoiceField(queryset=CoffeeType.objects.filter(available=True), to_field_name="code", widget=forms.Select(attrs={"class":"js-select2"}))

    def clean_customer_name(self):
        data = self.cleaned_data['customer_name']
        return data
    
    def clean_coffee_type(self):
        data = self.cleaned_data['coffee_type']
        return data
