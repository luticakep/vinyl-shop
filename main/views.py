from django.shortcuts import render

# Create your views here.
def show_main(request):
    context = {
        'npm' : '2306256381',
        'name': 'Kayla Soraya Djakaria',
        'class': 'KKI'
    }

    return render(request, "main.html", context)