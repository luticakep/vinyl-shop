# The Vinyl Vault

## Assignment 2

Click here to see my app

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

3. 


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

### Git in software development
When developing software, Git is essential. Software developers use it extensively because it makes it simple for them to collaborate, manage code across branches, and keep track of changes. Git keeps track of every commit we make, enabling developers to view their earlier versions of the code. To improve teamwork, Git also connects with local repositories. 

### Why using Django for learning software development?
Pyhton serves as the foundation for Django, making it an excellent starting point for those new to web frameworks. It has clear documentation, which is crucial for learners. Additionally, other frameworks (like Spring Boot, Flask, etc.) require more setup and lack built-in features, while others have extensive configuration and a steep learning curve. Therefore, Django is perfect for beginners to learn software development.

### Django model as an ORM
Django model is called Object Relational Mapping (ORM) because it can be used to interact with data from various relational databases such as SQLite, PostgreSQL, MySQL, and Oracle. Using an ORM API, Django enables us to add, remove, modify, and query objects. It allows you to work with your data more intuitively by mapping your Python classes to database tables. This simplifies and streamlines database management and querying.