
{% if ajax_data %}
    {% if jquery %}
        var {{ model_data_var }} = $.getJSON("{{ url }}").then(function(data) {
            if ($.isArray(data)) {
                return new {{ list_view_model_class }}(data);
            }
            else {
                return new {{ view_model_class }}(data);
            }
        });
    {% else %}
        var {{ model_data_var }} = new Promise(function(resolve, reject) {
            var xhr = new XMLHttpRequest();
            xhr.open('GET', "{{ url }}");
            xhr.setRequestHeader("Accept", "application/json");
            xhr.onload = function() {
                if (this.status == 200) {
                    var data = JSON.parse(this.responseText);
                    if (Array.isArray(data)) {
                        resolve(new {{ list_view_model_class }}(data));
                    }
                    else {
                        resolve(new {{ view_model_class }}(data));
                    }
                }
                reject();
            };
            xhr.onerror = reject;
            xhr.send();
        });
    {% endif %}
{% endif %}

function {{ bind_function }}() {
    {% if element_id %}
        var element_id = "{{ element_id }}";
        var element = document.getElementById(element_id);
    {% else %}
        var element_id = "body";
        var element = document.body;
    {% endif %}

    // console.log('{{ bind_function }}');

    var is_bound = !!ko.dataFor(element);
    if (is_bound) {
        throw new Error(
            "Element '" + element_id + "' is already bound! " +
            "If you are binding multiple elements element_id is required " +
            "on all knockout/knockout_bindings tags"
        );
    }

    {% if ajax_data %}
        {{ model_data_var }}.done(function(view_model) {
            ko.applyBindings(view_model, element);
        });
    {% else %}
        ko.applyBindings(new {{ model_type }}(), element);
    {% endif %}
}

{% if ajax_options %}
    {{ model_options_var }}.done({{ bind_function }});
{% else %}
    {{ bind_function }}();
{% endif %}
