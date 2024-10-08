# The Vinyl Vault

[PWS APPLICATION](http://kayla-soraya-vinylshop.pbp.cs.ui.ac.id/)

<details>
<Summary><b>Assignment 2</b></summary>

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
</details>

<details>
<Summary><b>Assignment 3</b></summary>

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
</details>

<details>
<Summary><b>Assignment 4</b></summary>

### Steps
#### Step 1: Register, login, logout
1. In the `views.py`, I created several functions that's used to register, login, and logout to the application. I also imported `UserCreationForm` which is a built in form and `messages` to give messages after the user successfully create an account. 
```py
def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
   if request.method == 'POST':
      form = AuthenticationForm(data=request.POST)

      if form.is_valid():
        user = form.get_user()
        login(request, user)
        response = HttpResponseRedirect(reverse("main:show_main"))
        response.set_cookie('last_login', str(datetime.datetime.now()))
        return response

   else:
      form = AuthenticationForm(request)
   context = {'form': form}
   return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response
```
2. Since the page for registering, login, and main page is different, I create an additional html page which is `login.html` and `register.html`.
3. In `urls.py`, add the URL path to access the functions.
```py
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
```
4. After we create the login function, when we open the link, it is supposed to be the login page, not the main page. Therefore we need to add this to the top of `show_main` function, so that the main page can only be accessed after the user logs in.
```py
@login_required(login_url='/login')
```

#### Step 2: Connects models `Product` and `User`
1. Add `from django.contrib.auth.models import User` to the `models.py`.
2. After that, add this line inside class `Product` to ensure that every models need to have a relationship with a user.
```py
user = models.ForeignKey(User, on_delete=models.CASCADE)
```
3. Open views.py, modify the code in `create_product`
```py
def create_product(request):
    form = VinylEntryForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        vinyl_entry = form.save(commit=False)
        vinyl_entry.user = request.user
        vinyl_entry.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_product.html", context)
```
`form.save(commit=False)` prevents Django from immediately saving the product to database

#### Step 3: Display logged in user details such as username and apply cookies to the application's main page
1. To display the last login we need to add some changes. In the `show_main` function, add this code snipet inside context variable.
```py
'last_login': request.COOKIES['last_login'],
```
2. After that, modify the main page and add this at the very last of the code.
```py
<h5>Last login session: {{ last_login }}</h5>
```
2. In the `show_main`, change the values of `vinyl_entries` and `context`.
```py
def show_main(request):
    vinyl_entries = Product.objects.filter(user=request.user)
    context = {
         'name': request.user.username,
    }
```
We filter the `vinyl_entries` so that only products created with the corresponding account will be displayed and the name shown in main page will be the username of the logged-in user.

### Difference between `HttpResponseRedirect()` and `redirect()`
`HttpResponseRedirect()` can only be a url. While `redirect()` can accept a model, view, or url as its argument. It is easier to use `redirect()` to perform redirects.

### How `Product` model is linked with `User`?
In Django, model can be linked with a user by using a foreign key. 
user = models.ForeignKey(User, on_delete=models.CASCADE)
This will create a one-to-many relationship or one user can have multiple products. 

### Difference between authentication and authorization
Authentication means the process of verifying a user, while authorization comes after authentication and gives actions that user can access. When a user logs in, Django verifies the user's credentials (authentication), and then store's the session ID in cookie, and then Django will checks what the user is allowed to do (authorization). Django implement authentication by providing a built-in views and forms to handle user login, register, and logout, such as UserCreationForm and LoginView. While for authorization, Django uses User and Group models to control access to views and models, such as @login_required.

### How Django remember logged-in users?
Django uses session cookies to keep track of users who are currently logged in. Django generates a session ID upon user login and saves it in a cookie. Django will use the ID to confirm the user's identity on each request after that, enabling the user to stay signed in.
Cookies can also be used as trackers for browsing activity and to keep shopping carts full. But not all cookies are secure; some can be used for malicious intent. Therefore, we require some settings, such as HttpOnly or Secure flags, to secure cookies.
</details>

<details>
<Summary><b>Assignment 5</b></summary>

### Steps
1. For the edit and delete product, I made the functions with id as the parameter inside `views.py`.
```py
def edit_product(request, id):
    product = Product.objects.get(pk=id)
    form = VinylEntryForm(request.POST or None, instance=product)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('main:show_main'))

    context = {'form': form}
    return render(request, "edit_product.html", context)

def delete_product(request, id):
    product = Product.objects.get(pk=id)
    product.delete()
    return HttpResponseRedirect(reverse('main:show_main'))
```
2. For the design, I use Tailwind, and I customize the login, register, main, add product, and edit product pages. I also consider the conditions; if there is no product, it'll show an image and a message. Otherwise, it will show the products inside the product card. Each product card consists of the name of the product, description, price, quantity, and two buttons for edit and delete. For the edit and delete button, I set the position to be at the bottom right of the card. I also created a navigation bar that is responsive to different device sizes.

### Priority order of CSS selectors
1. Inline styles, the styles which applied directly to an element using `style` attribute.
2. ID selectors, the styles applied using an element's `id` attribute.
3. Class selector, example: `.class` and `:hover`
4. Element selector and pseudo-elements, example: `div`, `p`, `h1`
5. Universal selector, using `*`

### Why does responsive design become an important concept in web application development?
Responsive design is an essential part of web applications because it guarantees a website works properly across different screen sizes. Not only that, it improves the user experience and can captrure broader audience(mobile and dekstop user).
Example of application that have implemented responsive web design: Google, Amazon, Youtube.
Example of application that have not implemented responsive web design: SCELE, SIAK NG. 

### Difference between margin, border, and padding
Margin is the outermost space and creates space between each elements. Margin ca be implement for each side of the element(top, right, bottom, left).
Border wraps around padding and the content and it can have different styles, color, or thickness. We can implement it by defining the style for each or all sides.
Padding is inside the element's border and creates space between content and the border. Padding has the same implementation like margin.

### The concept and use of flex box and grid layout 
Flex box is a one-dimensional model for arranging elements in a row or column. This is suits the most for creating navigation bar, item's allignment, and buttons.
Grid layout allows is a two-dimensional system to arrange items in a grid layout. The use of grid are for full-page website or section with different sizes  of elements. 
</details>

<details>
<Summary><b>Assignment 6</b></summary>

### Steps
#### Step 1: Create function to add product with AJAX
1. In the `views.py`, I create this function
```py
@csrf_exempt
@require_POST
def create_product_ajax(request):
    name = strip_tags(request.POST.get("name"))
    price = request.POST.get("price")
    description = strip_tags(request.POST.get("description"))
    quantity = request.POST.get("quantity")
    user = request.user

    new_product = Product(
        name=name,
        price=price,
        description=description,
        quantity=quantity,
        user=user
    )
    new_product.save()

    return HttpResponse(b"CREATED", status=201)
```
The `strip_tags` is for sanitizing the input data to prevent XSS attack.
`POST` is used to send data to the server.
2. In the `urls.py`, add the URL path to access the function.
```py
    path('create-product-ajax/', create_product_ajax, name='create_product_ajax'),
```

#### Step 2: Displaying Product with `fetch()` API
1. In the `views.py`, I change the first line of show_json and show_xml to filter the data based on the logged in user.
```py
data = Product.objects.filter(user=request.user)
```
2. In the `main.html`, I remove the line `{% if not product_entries %}` until `{% endif %}` and add this code to display the products.
```html
<div id="product_cards"></div>
```
3. In the same file, I create a script blog to fetch the data from the server, display it in the product card, and hide the product card.
```html
<script>
    function addProduct() {
    fetch("{% url 'main:create_product_ajax' %}", {
      method: "POST",
      body: new FormData(document.querySelector('#Form')),
    })
    .then(response => refreshProduct())

    document.getElementById("Form").reset(); 
    hideModal();

    return false;
  }

  async function getProduct(){
      return fetch("{% url 'main:show_json' %}").then((res) => res.json())
  }
  
  async function refreshProduct() {
    document.getElementById("product_cards").innerHTML = "";
    document.getElementById("product_cards").className = "";
    const Product = await getProduct();
    let htmlString = "";
    let classNameString = "";

    if (Product.length === 0) {
        classNameString = "flex flex-col items-center justify-center min-h-[24rem] p-6";
        htmlString = `
            <div class="flex flex-col items-center justify-center min-h-[24rem] p-6">
                <img src="{% static 'image/no_product.png' %}" alt="Sad face" class="w-32 h-32 mb-4"/>
                <p class="text-center text-gray-600 mt-4">There is no product in Vinyl Vault.</p>
            </div>
        `;
    }
    else {
        classNameString = "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 w-full items-stretch"
        Product.forEach((item) => {
            const name = DOMPurify.sanitize(item.fields.name);
            const description = DOMPurify.sanitize(item.fields.description);
            htmlString += `
            ...
            `;
        });
    }
    document.getElementById("product_cards").className = classNameString;
    document.getElementById("product_cards").innerHTML = htmlString;
  }
</script>
```
#### Step 3: Creating Modal
1. In the `main.html`, I create a modal for adding product including its button.
```html
  <div id="crudModal" tabindex="-1" aria-hidden="true" class="hidden fixed inset-0 z-50 w-full flex items-center justify-center bg-gray-800 bg-opacity-50 overflow-x-hidden overflow-y-auto transition-opacity duration-300 ease-out">
    <div id="crudModalContent" class="relative bg-white rounded-lg shadow-lg w-5/6 sm:w-3/4 md:w-1/2 lg:w-1/3 mx-4 sm:mx-0 transform scale-95 opacity-0 transition-transform transition-opacity duration-300 ease-out">
      <!-- Modal header -->
      <div class="flex items-center justify-between p-4 border-b rounded-t">
        <h3 class="text-xl font-semibold text-gray-900">
          Add Product
        </h3>
        <button type="button" class="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm p-1.5 ml-auto inline-flex items-center" id="closeModalBtn">
          <svg aria-hidden="true" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
            <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path>
          </svg>
          <span class="sr-only">Close modal</span>
        </button>
      </div>
      <!-- Modal body -->
      <div class="px-6 py-4 space-y-6 form-style">
        <form id="Form">
          <div class="mb-4">
            <label for="name" class="block text-sm font-medium text-gray-700">Name</label>
            <input type="text" id="name" name="name" class="mt-1 block w-full border border-gray-300 rounded-md p-2 hover:border-amber-900" required>
          </div>
          <div class="mb-4">
            <label for="price" class="block text-sm font-medium text-gray-700">Price</label>
            <input type="number" id="price" name="price" class="mt-1 block w-full border border-gray-300 rounded-md p-2 hover:border-amber-900" required>
          </div>
          <div class="mb-4">
            <label for="description" class="block text-sm font-medium text-gray-700">Description</label>
            <textarea id="description" name="description" rows="3" class="mt-1 block w-full h-52 resize-none border border-gray-300 rounded-md p-2 hover:border-amber-900 hover:border-2 transition duration-200" required></textarea>
          </div>
          <div class="mb-4">
            <label for="quantity" class="block text-sm font-medium text-gray-700">Quantity</label>
            <input type="number" id="quantity" name="quantity" class="mt-1 block w-full border border-gray-300 rounded-md p-2 hover:border-amber-900" required>
          </div>
        </form>
      </div>
      <!-- Modal footer -->
      <div class="flex flex-col space-y-2 md:flex-row md:space-y-0 md:space-x-2 p-6 border-t border-gray-200 rounded-b justify-center md:justify-end">
        <button type="button" class="bg-gray-500 hover:bg-gray-600 text-white font-bold py-2 px-4 rounded-lg" id="cancelButton">Cancel</button>
        <button type="submit" id="submit" form="Form" class="bg-amber-800 hover:bg-amber-900 text-white font-bold py-2 px-4 rounded-lg">Save</button>
      </div>
    </div>
  </div>
```
```html
<button data-modal-target="crudModal" data-modal-toggle="crudModal" class="btn bg-amber-800 hover:bg-amber-900 text-white font-bold py-2 px-4 rounded-lg transition duration-300 ease-in-out transform hover:-translate-y-1 hover:scale-105" onclick="showModal();">
        Add New Product by AJAX
      </button>
```

2. In the same file, I create a script blog to show and hide the modal.
```html
<script>
...
    const modal = document.getElementById('crudModal');
    const modalContent = document.getElementById('crudModalContent');

    function showModal() {
        modal.classList.remove('hidden'); 
        setTimeout(() => {
            modalContent.classList.remove('opacity-0', 'scale-95');
            modalContent.classList.add('opacity-100', 'scale-100');
        }, 50); 
    }

    function hideModal() {
        modalContent.classList.remove('opacity-100', 'scale-100');
        modalContent.classList.add('opacity-0', 'scale-95');

        setTimeout(() => {
            modal.classList.add('hidden');
        }, 150); 
    }

    document.getElementById("cancelButton").addEventListener("click", hideModal);
    document.getElementById("closeModalBtn").addEventListener("click", hideModal);
    document.getElementById("Form").addEventListener("submit", (e) => {
        e.preventDefault();
        addProduct();
    })
</script>
```

### Benefits of using JavaScript in developing web applications
1. Enhancing user experience
2. Interactivity
3. Asynchronous communication
4. Real-time updates

### Why we need to use await when we call fetch()?
Because `fetch()` is an asynchronous function, it returns a promise. We can wait for the promise to be fulfilled and receive the server's answer by utilizing await. If we don't use await, the response will not be returned.

### The use of `csrf_exempt` decorator on the view used for AJAX POST
`csrf_exempt` is used to exempt the view from CSRF verification. This is useful when we want to use AJAX POST request to send data to the server. By using `csrf_exempt`, we can bypass the CSRF verification and send the data to the server without any problem.

### Why can't the sanitization be done just in the front-end?
Sanitization should be done in the back-end because the front-end can be manipulated by the user. The user can get around the sanitization and send dangerous data to the server if we simply perform sanitization on the front end. Thus, in order to guarantee the safety and security of the data, we must do back-end sanitization.

</details>