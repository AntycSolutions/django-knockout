
{{ view_model_string }}

var {{ list_view_model_class }} = function(data) {
    var self = this;

    self.{{ model_list }} = ko.observableArray(data);

	{{ list_utils_string }}
} // {{ list_view_model_class }}
