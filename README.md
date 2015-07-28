django-knockout
===

**[django-knockout](//github.com/AntycSolutions/django-knockout)** makes it super easy to use [knockout.js](//knockoutjs.com/) with your [Django](//www.djangoproject.com/) models. It's great for project with objects that have lots of different models, or models with lots of different fields, or both. It can be used in both prototyping complex applications and directly in the templates of simple ones. Supports forms and formsets via the [Knockout pre-rendered library](//github.com/ErikSchierboom/knockout-pre-rendered).

Forked from [django-knockout-modeler](https://github.com/Miserlou/django-knockout-modeler).

Python 3.4  
Django 1.8  
Knockout 3.3  
Knockout pre-rendered 0.5

**django-knockout** turns this:

```python
# models.py
class MyObject(models.Model):
    my_number = models.IntegerField()
    my_name = models.CharField()
    
# views.py
my_objects = MyObject.objects.all()
```

Into this:

```javascript
var MyObjectData = {
    "myobject": [
        {"my_number": 666,
         "my_name": "Gabe Newell"}
    ]
};

var MyObject = function (data) {
    var self = this;
    
    self.my_number = ko.observable();
    self.my_name = ko.observable();
}

var MyObjectViewModel = function(data) {
    var self = this;
    
    self.myobjects = ko.observableArray(ko.utils.arrayMap(
        data.myobjects
        function(data) {
            return new MyObject(data);
        });

    self.addMyObject = function() {
        self.myobjects.push(new MyObject());
    };
    
    self.removeMyObject = function(data){
        self.myobjects.remove(data)
    };
}

ko.applyBindings(new MyObjectViewModel(), document.getElementById("myobjectviewmodel"));
```

With just this!

```django
{# template #}
{{ my_objects|knockout }}
```

Quick Start
---

0. Install django-knockout // TODO (not currently on pip)  
    via git (and then make sure the subfolder knockout is available to your PYTHONPATH)
    ```bash
    git clone github.com/AntycSolutions/django-knockout
    ```
    via pip
    ```bash
    pip install django-knockout
    ```

1. Add 'knockout' to your INSTALLED_APPS setting:

    ```python
    # settings.py
    INSTALLED_APPS = (
      ...
      'knockout',
    )
    ```

2. Include knockout.js in your HTML:

    ```django
    {# template #}
    <script type='text/javascript' src='//cdnjs.cloudflare.com/ajax/libs/knockout/3.3.0/knockout-min.js'></script>
    // Optionally needed if you're using forms/formsets
    <script type='text/javascript' src='//cdnjs.cloudflare.com/ajax/libs/knockout-pre-rendered/0.5.0/knockout-pre-rendered.min.js'></script>
    ```

4. Knockout your QuerySet:

    ```django
    {# template #}
    {% load knockout %}
    <script>
        {{ my_objects|knockout }}
    </script>
    ```

6. Loop over your bound data like so:

    ```django
    {# template #}
    <div id="myobjectviewmodel">
        <div data-bind="foreach: myobjects">
            My Name: <span data-bind="value: my_name"></span>
            My Number: <span data-bind="value: my_number"></span>
        </div>
    </div>
    ```

Simple Usage
---

**django-knockout** can be used directly in templates to generate knockout models and knockout-ready data, or either one you choose. To put a QuerySet directly into a django template as a Knockout object, you can do this:

```django
{# template #}
{{ my_objects|knockout }}
```

To get the data object by itself, you can do this:

```django
{# template #}
{{ my_objects|knockout_data }}
```

Similarly, you can get just the model, if you prefer to load your data from apis, like this:

```django
{# template #}
{{ my_objects|knockout_model }}
```

And even just the bindings:

```django
{# template #}
{% knockout_bindings my_objects %}
```

Progammatic Usage
---

First, import it!

```python
from knockout.ko import ko, ko_data, ko_model
```

To get the whole template, you can do this:

```python
ko_string = ko(MyObject.__class__, queryset)
# or
ko_string = ko(MyObject.__class__, None)
```

And to get just the data string you can do this..

```python
ko_string = ko_data(MyObject.__class__)
```

And, surprisingly, you can do the same for the model string:

```python
ko_string = ko_model(MyObject.__class__)
```

Custom fieldsets are also allowed (see Access Control):
```python
class MyObject():
    ...
    def knockout_fields(self):
        return ['my_name', 'my_number', ...]
        
knockout_model = KnockoutModel(MyObject.__class__)

ko_string = ko(MyObject.__class__, queryset, knockout_model)
```

Access Control
---

If you don't want to expose your entire model to Knockout, you can define a function in your model:

```python
def knockout_fields(self):
    return ['id', 'my_name', 'my_number', ...]
```

By default, it uses MyObject._meta.get_fields(). For computed properties, you can use python's \__property__ function.

Sorting
----------

django-knockout provides some convenient methods for sorting your data (see below for changing the comparator): 

```javascript
self.sortMyObjectsAsc = function() {
    self.myobjects.sort(function(a, b) {
        var a_comparator = a.id();
        var b_comparator = b.id();
        if (!a_comparator) { a_comparator = undefined; }
        if (!b_comparator) { b_comparator = undefined; }
        var result = a_comparator>b_comparator?-1:a_comparator<b_comparator?1:0;

        sorted = true;

        return result;
    });
};

self.sortMyObjectsDesc = function() {
    self.myobjects.sort(function(a, b) {
        var a_comparator = a.id();
        var b_comparator = b.id();
        if (!a_comparator) { a_comparator = undefined; }
        if (!b_comparator) { b_comparator = undefined; }
        var result = a_comparator<b_comparator?-1:a_comparator>b_comparator?1:0;

        sorted = true;

        return result;
    });
};
```

Include this in your template:

```django
{# template #}
<button data-bind='click: sortMyObjectsAsc'>Sort Asc</button>
<button data-bind='click: sortMyObjectsDesc'>Sort Desc</button>
```

By default, it will use the object's 'id' field, but you can also define your own comparator like so:

```python
def comparator(self):
    return 'my_name'  # or whichever field
```

If you don't define a comparator, 'id' must be in your knockout_fields.

Multi-Model Support
----------

django-knockout is all ready set up to be used with multiple types of data at the same time, as bindings happen to specific objects:

```javascript
ko.applyBindings(new MyObjectViewModel(), document.getElementById('myobjectviewmodel'));
```

which means that you somewhere in your HTML template, you will need to have an object with that id, like so:

```django
{# template #}
<div id="myobjectviewmodel">
    <div data-bind="foreach: my_objects">
        User <span data-bind="value: my_name"></span> is number <span data-bind="value: my_number"></span>.
    </div>
</div>
```

This is handy for prototyping, but more advanced applications may want to use the [master ViewModel](http://stackoverflow.com/a/9294752/1135467) technique instead.

Multi-Data Support
----------

If you're using multiple QuerySets of the same type, you'll need to define a custom name for the data variables.

```django
{# template #}
{{ my_objects|knockout_data:'CustomMyObjectData' }}
# and
{% knockout_bindings my_objects data_variable='CustomMyObjectData' %}
```

Issues
-------

There's probably a lot more that can be done to improve this. Please file issues if you find them!
