{% load knockout %}

var {{ view_model_string }} = function(data) {
    var self = this;

    {{ model_string}}

	{{ model_list_string }}
}
