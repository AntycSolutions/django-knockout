{% load knockout_tags %}

var {{ model_name }} = function() {
    // console.log('{{ model_name }}');
    var self = this;

    ko.mapping.fromJS({{ model_name|lower }}_fields, {}, self);

    self.form_prefix = ko.observable();
    self.DELETE = ko.observable();
} // {{ model_name }}
