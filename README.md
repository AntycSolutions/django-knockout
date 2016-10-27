django-knockout
===

**[django-knockout](//github.com/AntycSolutions/django-knockout)** makes it super easy to use [knockout.js](//knockoutjs.com/) with your [Django](//www.djangoproject.com/) models. It's great for project with objects that have lots of different models, or models with lots of different fields, or both. It can be used in both prototyping complex applications and directly in the templates of simple ones. Supports forms and formsets via [Knockout pre-rendered](//github.com/ErikSchierboom/knockout-pre-rendered). Supports [Django Rest Framework](//django-rest-framework.org) and [jQuery](//jquery.com) by default, but these can be disabled.

Forked from [django-knockout-modeler](//github.com/Miserlou/django-knockout-modeler).

### Table of Contents

* [Requirements](#requirements)
    * [Optional](#optional)
* [Preview](#preview)
* [Quick Start](#quick-start)
* [Simple Usage](#simple-usage)
* [Programmatic Usage](#programmatic-usage)
* [ModelForm Usage](#modelform-usage)
* [Access Control](#access-control)
* [Sorting](#sorting)
* [Multi-Model Support](#multi-model-support)
* [Custom Data Support](#custom-data-support)
* [Settings](#settings)
* [Advanced Usage](#advanced-usage)
    * [Knockout Functions](#knockout-functions)
    * [Knockout Tags](#knockout-tags)

Requirements
---

It's most likely that django-knockout works with older versions than the following, if it does, please let me know.

* [Python](//python.org) 2.7 or 3.4+
* [Django](//djangoproject.com) 1.8
* [Knockout](//knockoutjs.com) 3.3+

### Optional

* [Knockout pre-rendered](//github.com/ErikSchierboom/knockout-pre-rendered) 0.5+
* [Django Rest Framework](//django-rest-framework.org) 3.3+
* [jQuery](//jquery.com) 2.1+

Preview
---

**django-knockout** (with Django Rest Framework) turns this:

```python
# models.py
class MyObject(models.Model):
    my_number = models.IntegerField()
    my_name = models.CharField()

# views.py
myobject_class = MyObject

# serializers.py
class MyObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MyObject
        fields = '__all__'

# api.py
class MyObjectViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.MyObjectSerializer
    metadata_class = metadata.KnockoutMetadata
    queryset = models.MyObject.objects.all()
    
# urls.py
router = routers.DefaultRouter()
router.register(r'myobjects', api.MyObjectViewSet, 'myobject')
urlpatterns += urls.url(r'^api/', urls.include(router.urls)),
```

Into this:

```javascript
var MyObjectViewModel = function (data) {
    var self = this;
    self.my_number = ko.observable(data.my_number);
    self.my_name = ko.observable(data.my_name);
}

var MyObjectListViewModel = function(data) {
    var self = this;
    self.myobjects = ko.observableArray(data);
}

var myobject_data = $.getJSON("/app/api/myobjects/").then(function(data) {
    var ko_data = ko.mapping.fromJS(data)();
    return new MyObjectListViewModel(ko_data);
});

function ko_bind_myobjectviewmodel() {
    var element = document.body;
    person_data.done(function(view_model) {
        ko.applyBindings(view_model, element);
    });    
}

person_options.done(ko_bind_myobjectviewmodel);
```

With this!

```html+django
{# template #}
{% load knockout_tags %}
{% knockout myobject_class %}
```

Quick Start
---

0. Install django-knockout 
    via git (and then make sure the subfolder knockout is available to your PYTHONPATH)
    ```bash
    git clone github.com/AntycSolutions/django-knockout
    ```
    ~~via pip~~
    // TODO (not currently on pip)
    ```bash
    pip install django-knockout
    ```

1. Add 'knockout' to your INSTALLED_APPS setting:

    ```python
    # settings.py
    INSTALLED_APPS = (
      ...
      'knockout',
      # django rest framework, can be disabled
      'restframework',
    )
    ```

2. Include knockout.js in your HTML:

    ```html+django
    {# template #}
    <script type='text/javascript' src='//cdnjs.cloudflare.com/ajax/libs/knockout/3.3.0/knockout-min.js'></script>
    <script type='text/javascript' src='//cdnjs.cloudflare.com/ajax/libs/knockout.mapping/2.4.1/knockout.mapping.js'></script>
    {# Optionally needed if you're using forms/formsets #}
    <script type='text/javascript' src='//cdnjs.cloudflare.com/ajax/libs/knockout-pre-rendered/0.5.0/knockout-pre-rendered.min.js'></script>
    {# jQuery, can be disabled #}
    <script type='text/javascript' src='//code.jquery.com/jquery-3.1.1.js'></script>
    ```

4. Knockout your QuerySet:

    ```html+django
    {# template #}
    {% load knockout_tags %}
    <script type="text/javascript">
        {% knockout my_objects %}
    </script>
    ```

6. Loop over your bound data like so:

    ```html+django
    {# template #}
    <div data-bind="foreach: myobjects">
        My Name: <span data-bind="value: my_name"></span>
        My Number: <span data-bind="value: my_number"></span>
    </div>
    ```

Simple Usage
---

**django-knockout** can be used directly in templates to generate knockout view models. 

First, import it!

```html+django
{# template #}
{% load knockout_tags %}
```

To get just the list view model, if you prefer to load your data from API's, like this:

```html+django
{# template #}
{% knockout_list_view_model myobject_class %}
```

or if you don't need a list view model just a regular view model:

```html+django
{# template #}
{% knockout_view_model myobject_class %}
```

And even just the bindings:

```html+django
{# template #}
{% knockout_bindings myobject_class %}
```

If you'd like to output the list utils (see below for more information):

```html+django
{# template #}
{% knockout_list_utils myobject_class %}
```

Programmatic Usage
---

First, import it!

```python
from knockout import ko
```

To get the whole template (like the `knockout` tag), you can do this:

```python
ko_string = ko.ko(MyObject)
```

Just the bindings

```python
ko_bindings_string = ko.ko_bindings(MyObject)
```

Just the List View Model

```python
ko_list_view_model_string = ko.ko_list_view_model(MyObject)
```

Just the View Model

```python
ko_view_model_string = ko.ko_view_model(MyObject)
```

list utils (see below for more information):

```python
ko_list_utils_string = ko.ko_list_utils(MyObject)
```

ModelForm Usage
---

Want to use Django forms to generate your html and knockout binds as well? Just use `KnockoutModelForm`:

```python
# forms.py
from knockout import forms

class MyObjectKnockoutModelForm(forms.KnockoutModelForm):
    ...
    class Meta:
        model = models.MyObject
        fields = '__all__'
```

Since Django forms output values we use Knockout pre-rendered to prevent double binding. This means we don't need django-knockout to get data via ajax.

```html+django
{# template #}
{% load knockout_tags %}
{% knockout myobject_class disable_ajax_data=True is_list=False %}

<form method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Submit</button>
</form>
```

which outputs:

```html
<p>
    <label for="id_my_number">My Number:</label>
    <input data-bind="init, value: my_number" id="id_my_number" maxlength="64" name="my_number" type="text" value="..." />
</p>
<p>
    <label for="id_my_name">My Name:</label>
    <input data-bind="init, value: my_name" id="id_my_name" maxlength="64" name="my_name" type="text" value="..." />
</p>
```

Custom fieldsets are also allowed at form level (see Access Control for model level):

```python
from knockout import forms

class MyObjectKnockoutModelForm(forms.KnockoutModelForm):
    ...
    @staticmethod
    def knockout_fields():
        return ['id', 'my_name', 'my_number', ...]
```

Access Control
---

If you don't want to expose your entire model to Knockout, you can define a function in your model:
```python
class MyObject(models.Model):
    ...
    @staticmethod
    def knockout_fields():
        return ['id', 'my_name', 'my_number', ...]
```

Sorting
---

django knockout provides some convenience methods (via `knockout_list_utils`/`ko_list_utils`) for manipulating your arrays:

```javascript
    self.addMyObjectViewModel = function(data) {
        self.persons.push(new MyObjectViewModel(data));
    };

    self.createMyObjectViewModel = function(data) {
        return new MyObjectViewModel(data);
    };

    self.removeMyObjectViewModel = function(data) {
        self.persons.remove(data);
    };

    self.destroyMyObjectViewModel = function(data) {
        self.persons.destroy(data);
    };

    self.deleteMyObjectViewModel = function(data) {
        var index = self.persons.indexOf(data);
        self.persons()[index].DELETE(true);
    }
```

* See [here](http://knockoutjs.com/documentation/observableArrays.html) for what the destroy function is for
* The data parameter for add/create is optional
* The delete function is for formsets

for sorting your data (see below for changing the comparator):

```javascript
self.sortMyObjectViewModelsAsc = function() {
    self.myobjects.sort(function(a, b) {
        var a_comparator = a.id();
        var b_comparator = b.id();
        if (!a_comparator) { a_comparator = undefined; }
        if (!b_comparator) { b_comparator = undefined; }
        var result = a_comparator>b_comparator?-1:a_comparator<b_comparator?1:0;

        return result;
    });
};

self.sortMyObjectViewModelsDesc = function() {
    self.myobjects.sort(function(a, b) {
        var a_comparator = a.id();
        var b_comparator = b.id();
        if (!a_comparator) { a_comparator = undefined; }
        if (!b_comparator) { b_comparator = undefined; }
        var result = a_comparator<b_comparator?-1:a_comparator>b_comparator?1:0;

        return result;
    });
};
```

Include a variation of this in your template:

```html+django
{# template #}
<button data-bind='click: sortMyObjectViewModelsAsc'>Sort Asc</button>
<button data-bind='click: sortMyObjectViewModelsDesc'>Sort Desc</button>
```

By default, it will use the object's 'id' field, but you can also define your own comparator like so:

```python
class MyObject(models.Model):
    ...
    @staticmethod
    def knockout_comparator(self):
        return 'my_name'  # or whichever field
```

If you don't define a comparator, 'id' must be available.

Multi-Model Support
---

django-knockout is all ready set up to be used with multiple types of data at the same time, as bindings can happen to specific objects via this generated function:

```javascript
function ko_bind() {
    var element_id = "myobjectviewmodel";
    var element = document.getElementById(element_id);
    
    ko.applyBindings(new MyObjectListViewModel(), element);
}
ko_bind();
```

which means that you somewhere in your HTML template, you will need to have an object with that id, like so:

```html+django
{# template #}
<div id="myobjectviewmodel">
    <div data-bind="foreach: myobjects">
        User <span data-bind="value: my_name"></span> is number <span data-bind="value: my_number"></span>.
    </div>
</div>
```

and add the paramter to the `knockout` tag:

```html+django
{# template #}
{% load knockout_tags %}
{% knockout myobject_class element_id="myobjectviewmodel" %}
```

Custom Data Support
---

Is django-knockout using the wrong url? Pass it into `knockout`/`ko` or `knockout_bindings`/`ko_bindings`:

```html+django
{# template #}
{% load knockout_tags %}
{% url 'app:myobject-list' as myobject_list_url %}
{% knockout myobject_class url=myobject_list_url %}
```

```python
from knockout import ko
ko.ko(MyObject, url='/app/api/myobjects')
```

Settings
---

The following settings are currently supported:

```python
# settings.py
DJANGO_KNOCKOUT = {
    'disable_jquery': False,  # default
    'disable_ajax_data': False,  # default
    'disable_ajax_options': False,  # default
}
```

* Don't like jQuery (or don't want to include another library)? Set `disable_jquery` to `True` and django-knockout will fallback to vanilla javascript `XMLHttpRequest`
* Don't like how django-knockout fetches data? Set `disable_ajax_data` to `True` and provide your own data (after knockout tags)
```javascript
var vm = ko.dataFor(document.body); // or
vm = ko.dataFor(document.getElementById(id)); // if you specified an element_id
vm.myobjects(data);
```
* Don't like how django-knockout fetches view model's fields? Set `disable_ajax_options` to `True` and setup your fields manually (before knockout tags)
```javascript
myobject_fields = {
    'my_number': null, // null required to become observable
    'my_name': null,
    'my_list': [], // [] required to become observableArray
    ...
}
```

Advanced Usage
---

Defaults not working out for you? Here's the parameters to template tags and ko functions:

#### Knockout Functions

```python
'''
    required:
        model_class: The class of model you want to knockout
        
    optional:
        element_id: The id of the element you want to bind your view model to
        context: We need this to lookup urls requiring app_name, not required if your urls don't require app_name, or you've specified an url
        url: The url to get ajax data/options from
        disable_ajax_data: If True, do not get ajax data (overrides disable_ajax_data setting), defaults to `disable_ajax_data` setting
        disable_ajax_options: If True, do not get ajax options (overrides disable_ajax_options setting), defaults to `disable_ajax_options` setting
        is_list: Controls whether or not to output a List View Model (True, default) or just a View Model (False)
'''
def ko(
    model_class,
    element_id=None,
    context=None,
    url=None,
    disable_ajax_data=None,
    disable_ajax_options=None,
    is_list=True,
)
```

```python
'''
    required:
        model_class: The class of model you want to knockout
        
    optional:
        element_id: The id of the element you want to bind your view model to
        context: We need this to lookup urls requiring app_name, not required if your urls don't require app_name, or you've specified an url
        url: The url to get ajax data/options from
        disable_ajax_data: If True, do not get ajax data (overrides disable_ajax_data setting), defaults to `disable_ajax_data` setting
        disable_ajax_options: If True, do not get ajax options (overrides disable_ajax_options setting), defaults to `disable_ajax_options` setting
        is_list: Controls whether or not to output a List View Model (True, default) or just a View Model (False)
'''
def ko_bindings(
    model_class,
    element_id=None,
    context=None,
    url=None,
    disable_ajax_data=None,
    disable_ajax_options=None,
    is_list=True,
)
```

```python
'''
    required:
        model_class: The class of model you want to knockout
        
    optional:
        context: We need this to lookup urls requiring app_name, not required if your urls don't require app_name, or you've specified an url
        url: The url to get ajax data/options from
        disable_ajax_options: If True, do not get ajax options (overrides disable_ajax_options setting), defaults to `disable_ajax_options` setting
        include_list_utils: default True, if False, django-knockout will skip rendering js util functions
'''
def ko_list_view_model(
    model_class,
    context=None,
    url=None,
    disable_ajax_options=None,
    include_list_utils=True,
)
```

```python
'''
    required:
        model_class: The class of model you want to knockout
        
    optional:
        context: We need this to lookup urls requiring app_name, not required if your urls don't require app_name, or you've specified an url
        url: The url to get ajax data/options from
        disable_ajax_options: If True, do not get ajax options (overrides disable_ajax_options setting), defaults to `disable_ajax_options` setting
'''
def ko_view_model(
    model_class,
    context=None,
    url=None,
    disable_ajax_options=None,
)
```

```python
'''
    required:
        model_class: The class of model you want to knockout
'''
def ko_list_utils(model_class)
```

#### Knockout Tags

Knockout template tags `knockout`, `knockout_list_view_model`, `knockout_bindings`, `knockout_view_model`, `knockout_list_utils` match up with their Knockout function equivalent, except their first required arg `model_class` can be a list of models, a QuerySet, a model's class, or an instance of a model. They also implicitly take in the context when called.

```html+django
{# template #}
<!--
    required:
        field: a Django Model Form field
        data_bind: variable to assign output to
-->
{% data_bind field as data_bind %}
```
