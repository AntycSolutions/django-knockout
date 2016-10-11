
var {{ model_object }};

{% if ajax_data %}
    {% if jquery %}
        var {{ model_data_var }} = $.getJSON(
            "{{ url }}",
            function(data) {
                if ($.isArray(data)) {
                    {{ model_object }} = (
                        new {{ list_view_model_class }}()
                    );

                    var {{ model_list }}_observable_array = ko.mapping.fromJS(
                        data
                    );
                    {{ model_object }}.{{ model_list }}(
                        {{ model_list }}_observable_array()
                    );
                }
                else {
                    {{ model_object }} = new {{ view_model_class }}(data);
                }
            }
        );
    {% else %}
        var {{ model_data_var }} = new Promise(function(resolve, reject) {
            var xhr = new XMLHttpRequest();
            xhr.open('GET', "{{ url }}");
            xhr.setRequestHeader("Accept", "application/json");
            xhr.onload = function() {
                if (this.status == 200) {
                    var data = JSON.parse(this.responseText);
                    if (Array.isArray(data)) {
                        {{ model_object }} = (
                            new {{ list_view_model_class }}()
                        );

                        var {{ model_list }}_observable_array = ko.mapping.fromJS(
                            data
                        );
                        {{ model_object }}.{{ model_list }}(
                            {{ model_list }}_observable_array()
                        );
                    }
                    else {
                        {{ model_object }} = new {{ view_model_class }}(data);
                    }
                    resolve();
                }
                reject();
            };
            xhr.onerror = reject;
            xhr.send();
        });
    {% endif %}
{% endif %}

function ko_bind_{{ model_object }}() {
    // console.log('ko_bind {{ model_object }} {{ element_id }}');
    var element = document.getElementById("{{ element_id }}");
    var is_bound = !!ko.dataFor(element);
    if (is_bound) {
        throw "Element '{{ element_id }}' is already bound!";
    }

    {% if ajax_data %}
        {{ model_data_var }}.then(function() {
            ko.applyBindings({{ model_object }}, element);
        });
    {% else %}
        {{ model_object }} = new {{ model_type }}();

        ko.applyBindings({{ model_object }}, element);
    {% endif %}
}

{% if ajax_options %}
    {{ model_options_var }}.then(ko_bind_{{ model_object }});
{% else %}
    ko_bind_{{ model_object }}();
{% endif %}
