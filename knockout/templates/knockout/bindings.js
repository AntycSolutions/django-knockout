
ko.applyBindings(
    new {{ view_model_string }}(),
    document.getElementById(
        {% if element_id %}
            "{{ element_id }}"
        {% else %}
            "{{ view_model_string|lower }}"
        {% endif %}
    )
);
