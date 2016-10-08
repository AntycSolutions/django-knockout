
{% if ajax_options %}
    var {{ model_fields_var }};

    {% if jquery %}
        var {{ model_options_var }} = $.ajax({
            url: "{{ url }}",
            type: 'OPTIONS',
            success: function(data) {
                {{ model_fields_var }} = ko.mapping.fromJS(data.POST);
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
            };
            xhr.send();
        });
    {% endif %}
{% endif %}

var {{ view_model_class }} = function(data) {
    // console.log('{{ view_model_class }}');
    var self = this;

    var no_data = (
        typeof data === 'undefined' ||
        data instanceof {{ list_view_model_class }}
    );
    if (no_data) {
        if (typeof {{ model_fields_var }} === 'undefined') {
            throw (
                "{{ model_fields_var }} is undefined, " +
                "please setup Django Rest Framework or define it " +
                "yourself after the knockout templatetag."
            );
        }

        ko.mapping.fromJS({{ model_fields_var }}, {}, self);
    }
    else {
        ko.mapping.fromJS(data, {}, self);
    }

    self.form_prefix = ko.observable();
    self.DELETE = ko.observable();
} // {{ view_model_class }}
