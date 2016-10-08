
var {{ list_view_model_object }} = new {{ list_view_model_class }}();

{% if ajax_data %}
    {% if jquery %}
        $.getJSON(
            "{{ url }}",
            function(data) {
                var {{ model_list }}_observable_array = ko.mapping.fromJS(
                    data
                );
                {{ list_view_model_object }}.{{ model_list }}(
                    {{ model_list }}_observable_array()
                );
            }
        );
    {% else %}
        var xhr = new XMLHttpRequest();
        xhr.open('GET', "{{ url }}");
        xhr.setRequestHeader("Accept", "application/json");
        xhr.onload = function() {
            if (this.status == 200) {
                var data = JSON.parse(this.responseText);
                var {{ model_list }}_observable_array = ko.mapping.fromJS(
                    data
                );
                {{ list_view_model_object }}.{{ model_list }}(
                    {{ model_list }}_observable_array()
                );
            }
        };
        xhr.send();
    {% endif %}
{% endif %}

function ko_bind() {
    ko.applyBindings(
        {# Fix race condition when calling bindings multiple times #}
        {{ list_view_model_object }},
        document.getElementById(
            {% if element_id %}
                "{{ element_id }}"
            {% else %}
                "{{ list_view_model_object }}"
            {% endif %}
        )
    );
}

{% if ajax_options %}
    {{ model_options_var }}.then(ko_bind);
{% else %}
    ko_bind();
{% endif %}
