self._{{ model_args }} = ko.observableArray(ko.utils.arrayMap(
    data.{{ model_args }},
    function(data) {
        return new {{ model_name }}(data);
    }
));

self.add{{ model_name }} = function(data) {
    self._{{ model_args }}.push(new {{ model_name }}(data));
};

self.remove{{ model_name }} = function(data) {
    self._{{ model_args }}.remove(data);
};

self.sort{{ model_name }}sAsc = function() {
    self._{{ model_args }}(self._{{ model_args }}().sort(function(a, b) {
        return a._{{ comparator }}()>b._{{ comparator }}()?-1:a._{{ comparator }}()<b._{{ comparator }}()?1:0;
     }));
};

self.sort{{ model_name }}sDesc = function() {
    self._{{ model_args }}(self._{{ model_args }}().sort(function(a, b) {
        return a._{{ comparator }}()<b._{{ comparator }}()?-1:a._{{ comparator }}()>b._{{ comparator }}()?1:0;
    }));
};
