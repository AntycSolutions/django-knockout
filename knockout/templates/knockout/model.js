{% load knockout %}
var {{ model_name }} = function(data) {
    var self = this;

    if (data) {
        {% for field in fields %}
        self.{{ field }} = ko.observable(data.{{ field }});
        {% endfor %}
        {% for knockout_model in fk_knockout_models %}
        var data_{{ knockout_model.field_name }} = (data.{{ knockout_model.field_name }}) ? data.{{ knockout_model.field_name }} : data;
        self.{{ knockout_model.field_name }} = new {{ knockout_model.model_name }}(data_{{ knockout_model.field_name }});
        {% endfor %}
    }
    else {
        {% for field in fields %}
        self.{{ field }} = ko.observable();
        {% endfor %}
        {% for knockout_model in fk_knockout_models %}
        self.{{ knockout_model.field_name }} = new {{ knockout_model.model_name }}();
        {% endfor %}
    }
    {% for m2m_knockout_model in m2m_knockout_models %}
    {{ m2m_knockout_model.model_list }}
    {% endfor %}
} // {{ model_name }}
{% for knockout_model in fk_knockout_models %}
{{ knockout_model.model_string }}
{% endfor %}
{% for m2m_knockout_model in m2m_knockout_models %}
{{ m2m_knockout_model.model_string }}
{% endfor %}
