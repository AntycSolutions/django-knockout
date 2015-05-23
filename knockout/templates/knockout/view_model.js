
var {{ model_name }} = function(data) {
	var self = this;
	{% for field in fields %}
	self.{{ field }} = ko.observable(data.{{ field }});{% endfor %}
}

var {{ view_model_string }} = function({{ model_args }}) {
    var self = this;

    self.{{ model_args }} = ko.observableArray(ko.utils.arrayMap(
		{{ model_args }},
		function({{ model_arg }}) {
			return new {{ model_name }}({{ model_arg }});
		}
	));

	self.add{{ model_name }} = function({{ model_arg }}) {
		self.{{ model_args }}.push(new {{ model_name }}({{ model_arg }}));
	};

	self.remove{{ model_name }} = function({{ model_arg }}) {
		self.{{ model_args }}.remove({{ model_arg }})
	};

	self.sort{{ model_name }}sAsc = function() {
		self.{{ model_args }}(self.{{ model_args }}().sort(function(a, b) {
			return a.{{ comparator }}()>b.{{ comparator }}()?-1:a.{{ comparator }}()<b.{{ comparator }}()?1:0;
		 }));
	};

	self.sort{{ model_name }}sDesc = function() {
		self.{{ model_args }}(self.{{ model_args }}().sort(function(a, b) {
			return a.{{ comparator }}()<b.{{ comparator }}()?-1:a.{{ comparator }}()>b.{{ comparator }}()?1:0;
		}));
	};
}
