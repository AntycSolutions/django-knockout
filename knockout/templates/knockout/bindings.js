
{% if ajax_data %}
    {% if jquery %}
        var {{ model_data_var }} = $.getJSON("{{ url }}").then(function(data) {
            if ($.isArray(data)) {
                var mapping = {
                    create: function(options) {
                        return new {{ view_model_class }}(options.data);
                    }
                }
                {# map data and get the underlying array #}
                var ko_data = ko.mapping.fromJS(data, mapping)();

                return new {{ list_view_model_class }}(ko_data);
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
                if (this.status !== 200) {
                    reject();
                }

                var data = JSON.parse(this.responseText);
                if (Array.isArray(data)) {
                    var mapping = {
                        create: function(options) {
                            return new {{ view_model_class }}(options.data);
                        }
                    }
                    {# map data and get the underlying array #}
                    var ko_data = ko.mapping.fromJS(data, mapping)();

                    resolve(new {{ list_view_model_class }}(ko_data));
                }
                else {
                    resolve(new {{ view_model_class }}(data));
                }
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
            "Element {% if element_id %}with id {% endif %}'" +
            element_id + "' is already bound! " +
            "If you are binding multiple elements element_id is required " +
            "on all knockout/knockout_bindings tags"
        );
    }

    {% if ajax_data %}
        {{ model_data_var }}.then(function(view_model) {
            ko.applyBindings(view_model, element);
        }).{% if jquery %}fail{% else %}catch{% endif %}(function(error) {
            throw error;
        });
    {% else %}
        ko.applyBindings(new {{ model_type }}(), element);
    {% endif %}
}

{% if ajax_options %}
    {{ model_options_var }}.then(
        {{ bind_function }}
    ).{% if jquery %}fail{% else %}catch{% endif %}(function(error) {
        throw error;
    });
{% else %}
    {{ bind_function }}();
{% endif %}
