# The Vinyl Vault

## Assignment 2

http://kayla-soraya-vinylshop.pbp.cs.ui.ac.id/

### Steps
#### Step 1: Creating virtual environment
1. After creating vinyl-shop directory, we need to create a virtual enviroment for isolating the packages and dependencies from the apllication to avoid conflicts between projects by running the following command.
```
python -m venv env
```

2. Activate the virtual environment with the following command.
```
env\Scripts\activate
```

#### Step 2: Creating Django project
1. After activating the virtual environment, we need to add some dependencies which is modules to speed up development but require careful management to ensure compatibility. 

2. Create `requirements.txt` file and add this dependencies
```
django
gunicorn
whitenoise
psycopg2-binary
requests
urllib3
```

3. Install those dependencies by running this command.
```
pip install -r requirements.txt
```

4. Create Django project with the name `vinyl_shop` using this command.
```
django-admin startproject vinyl_shop .
```

#### Step 3: Creating an application in the project
1. Now, we need to create an application with the name `main` in the project. Run this command and after that a new directory with the name `main` will be created. 
```
python manage.py startapp main
```

2. Open `settings.py` inside `vinyl_shop` directory and add `'main'` to the `INSTALLED_APPS` variable.

3. Add a new directory called `templates` inside the `main` application.

4. Create a new file `main.html` inside 'templates' and add this inside the file
```html
<h1>The Vinyl Vault</h1>

<h5>NPM: </h5>
<p>{{ npm }}</p> 
<h5>Name: </h5>
<p>{{ name }}</p> 
<h5>Class: </h5>
<p>{{ class }}</p> 
```
This code is used to display values in variables that have been defined before. 

5. Open `views.py` in main application and add the following code.
```py
from django.shortcuts import render

def show_main(request):
    context = {
        'npm' : '2306256381',
        'name': 'Kayla Soraya Djakaria',
        'class': 'KKI'
    }

    return render(request, "main.html", context)
```
As I explained in the previous step, this code has a dictionary(context) which has data that will be send to the html template.

#### Step 4: Modifying models.py in main application
1. Open `models.py` in the main directory application.

2. Fill the file with the following code.
```py
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    quantity = models.IntegerField()
```
Explanation:
`models.Model` is used to define models in Django.
`Product` is the name of model that I use.
`name`, `price`, `description`, `quantity` are the attributes in the model for my application.

#### Step 5: Configuring URL for the main application
1. Create `urls.py` inside the `main` directory and fill with this.
```py
from django.urls import path
from main.views import show_main

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
]
```
Inside the `urlpatterns`, `path` is used to define the URL pattern and `show_main` function will be displayed when the corresponding URL is accessed.

#### Step 6: Configuring the project URL
1. Open `urls.py` inside `vinyl_shop` directory
```py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls'))
]
```
In the code above, `include` is used to import URL from other apps. The URL path is an empty string because we want to access the main page directly

### Client request flow
<img src="/pictures/diagram.png">

The client sends a request to the server by using a URL and then Django recieves the request to `urls.py` to match the requested one. `views.py` is used to call the corresponding function that matches the URL and process it to the databases. If data manipulation is needed, then Django's ORM,`models.py`, is used to interact with the database. After the processing is done, `template` or the HTML will generate the final content by sending it as an HTTP response to the client.

### Git in software development
When developing software, Git is essential. Software developers use it extensively because it makes it simple for them to collaborate, manage code across branches, and keep track of changes. Git keeps track of every commit we make, enabling developers to view their earlier versions of the code. To improve teamwork, Git also connects with local repositories. 

### Why using Django for learning software development?
Pyhton serves as the foundation for Django, making it an excellent starting point for those new to web frameworks. It has clear documentation, which is crucial for learners. Additionally, other frameworks (like Spring Boot, Flask, etc.) require more setup and lack built-in features, while others have extensive configuration and a steep learning curve. Therefore, Django is perfect for beginners to learn software development.

### Django model as an ORM
Django model is called Object Relational Mapping (ORM) because it can be used to interact with data from various relational databases such as SQLite, PostgreSQL, MySQL, and Oracle. Using an ORM API, Django enables us to add, remove, modify, and query objects. It allows you to work with your data more intuitively by mapping your Python classes to database tables. This simplifies and streamlines database management and querying.


## Assignment 3

### Steps
#### Step 1: Creating form input data
1. Create a new file `forms.py` in `main` which will consists of the form structure
```py
from django.forms import ModelForm
from main.models import Product

class VinylEntryForm(ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price", "description", "quantity"]
```

2. In the `views.py` add `from django.shortcuts import render, redirect` and then create a new function for adding the new product.
```py
def create_product(request):
    form = VinylEntryForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_product.html", context)
```

3. After that, we want to show the added product in the main page. Change the `show_main` in `views.py`.
```py
def show_main(request):
    vinyl_entries = Product.objects.all()

    context = {
        'name': 'Kayla Soraya Djakaria',
        'class': 'KKI',
        'product_entries': vinyl_entries,
    }

    return render(request, "main.html", context)
```

4. Add the URL path in `urls.py` 
```py 
path('create-product', create_product, name='create_product'),
```

5. Lastly, we need to create a new html file for when we create new product and also add new code in the `main.html` which will display the data in the form.

#### Step 2: Returning Data in XML, JSON, XML by ID, JSON by ID
1. In the `views.py` and add this.
```py
from django.http import HttpResponse
from django.core import serializers
```

2. Then we can just add the function for returning data in XML and JSON
```py
def show_xml(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
```

#### Step 3: Create URL routing for each views
1. Open `urls.py` and import the function that we just created.
```py
from main.views import show_xml, show_json, show_xml_by_id, show_json_by_id
```

2. Add the URL path to the `urlpatterns` to access the function that was imported.
```py
path('xml/', show_xml, name='show_xml'),
path('json/', show_json, name='show_json'),
path('xml/<str:id>/', show_xml_by_id, name='show_xml_by_id'),
path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
```

### Why we need data delivery in implementing a platform?
Data delivery is important to the platform because it guarantees that the appropriate data is received by the required users and components at the appropriate time. It facilitates real-time access, enables system component coordination, and enhances user experience by delivering accurate, timely information. 

### XML or JSON? Why JSON is more popular than XML?
I personally think JSON is better than XML since it has more readable syntax. Additionally, JSON is more popular than XML because JSON is more simple and efficient and has better alignment with modern web application.

### `is_valid()` in Django
The usage of `is_valid()`method in Django, for example `form.is_valid()`, is used to validate the input from the form. We need that method because by using `is_valid()` prevent invalid data processing. If the form data is invalid, this method helps by adding thorough error messages to the form's errors attribute for each field that failed validation.

### `csrf_token` in creating form in Django
`csrf_token` is a token that functions as a security system and ensures that the form is coming from an actual user. The token is automatically generated by Django to prevent attacks. If we don't use `csrf_token`, attackers could execute unauthorized actions as it was coming from the user and could lead to security breaches. 

### Postman results
### JSON
<img src="/pictures/json.png">

### JSON by ID
<img src="/pictures/json_id.png">

### XML
<img src="/pictures/xml.png">

### XML by ID
<img src="/pictures/xml_id.png">