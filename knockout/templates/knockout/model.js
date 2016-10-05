{% load knockout_tags %}

var {{ model_name }} = function(data) {
    // console.log('{{ model_name }}');
    var self = this;

    var data_type = typeof data;
    var no_data = (
        data_type === 'undefined' ||
        typeof {{ model_name }}ViewModel === data_type
    );
    if (no_data) {
        ko.mapping.fromJS({{ model_name|lower }}_fields, {}, self);
    }
    else {
        ko.mapping.fromJS(data, {}, self);
    }

    self.form_prefix = ko.observable();
    self.DELETE = ko.observable();
} // {{ model_name }}
