
    if (data) {
        self.{{ model_args }} = ko.observableArray(ko.utils.arrayMap(
            data.{{ model_args }},
            function(data) {
                return new {{ model_name }}(data);
            }
        ));
    }
    else {
        self.{{ model_args }} = ko.observableArray();
    }

    self.add{{ model_name }} = function() {
        self.{{ model_args }}.push(new {{ model_name }}());
    };

    self.remove{{ model_name }} = function(data) {
        self.{{ model_args }}.remove(data);
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
