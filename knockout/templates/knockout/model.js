{% load knockout %}
var {{ model_name }} = function(data) {
    var self = this;
    {% for field in fields %}
    self._{{ field }} = ko.observable(data.{{ field }});
    {% endfor %}
    {% for field_dict in fk_fields %}
    {{ field_dict.model_string }}
    var data_{{ field_dict.field_name }} = (data.{{ field_dict.field_name }}) ? data.{{ field_dict.field_name }} : data;
    self._{{ field_dict.field_name }} = new {{ field_dict.model_name }}(data_{{ field_dict.field_name }});
    {% endfor %}
    {% for field_dict in m2m_fields %}
    {{ field_dict.model_string }}
    {{ field_dict.model_list }}
    {% endfor %}
}
