
{% if ajax_options %}
    var {{ model_fields_var }};

    {% if jquery %}
        var {{ model_options_var }} = $.ajax({
            url: "{{ url }}",
            type: 'OPTIONS',
            success: function(data) {
                // console.log('OPTIONS', data);
                {{ model_fields_var }} = data.POST;
            },
        });
    {% else %}
        var {{ model_options_var }} = new Promise(function(resolve, reject) {
            var xhr = new XMLHttpRequest();
            xhr.open('OPTIONS', "{{ url }}");
            xhr.setRequestHeader("Accept", "application/json");
            xhr.onload = function() {
                if (xhr.status == 200) {
                    var data = JSON.parse(xhr.responseText);
                    {{ model_fields_var }} = ko.mapping.fromJS(data.POST);
                    resolve();
                }
                reject();
            };
            xhr.onerror = reject;
            xhr.send();
        });
    {% endif %}
{% endif %}

var {{ view_model_class }} = function(data) {
    // console.log('{{ view_model_class }}');
    var self = this;

    if (typeof {{ model_fields_var }} === 'undefined') {
        throw new Error(
            "{{ model_fields_var }} is undefined, " +
            "please setup Django Rest Framework or define it " +
            "yourself after the knockout templatetag."
        );
    }

    var fields = [
        {% for field_name in knockout_options.knockout_fields %}
            '{{ field_name }}',
        {% endfor %}
    ];
    var ignore = [
        {% for field_name in knockout_options.knockout_exclude %}
            '{{ field_name }}',
        {% endfor %}
    ];
    if (ignore.length && fields.length) {
        throw new Error(
            'Define knockout_exclude or knockout_fields, not both. ' +
            'ignore: ' + ignore + ' ' +
            'fields: ' + fields
        );
    }
    for (var key in {{ model_fields_var }}) {
        var not_in_fields = fields.indexOf(key) === -1;
        if (not_in_fields) {
            ignore.push(key);
        }
    }
    var mapping = {'ignore': ignore};

    var no_data = (
        typeof data === 'undefined' ||
        data instanceof {{ list_view_model_class }}
    );
    if (no_data) {
        ko.mapping.fromJS({{ model_fields_var }}, mapping, self);
    }
    else {
        ko.mapping.fromJS(data, mapping, self);
    }

    self.form_prefix = ko.observable();
    self.DELETE = ko.observable();
} // {{ view_model_class }}
