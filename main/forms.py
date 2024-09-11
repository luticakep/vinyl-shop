from django.forms import ModelForm
from main.models import Product

class VinylEntryForm(ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price", "description", "quantity"]