
    self.{{ model_args }} = ko.observableArray();

    self.add{{ model_name }} = function(data) {
        // console.log('add{{ model_name }}');
        self.{{ model_args }}.push(new {{ model_name }}(data));
    };

    self.create{{ model_name }} = function(data) {
        // console.log('create{{ model_name }}');
        return new {{ model_name }}(data);
    };

    self.remove{{ model_name }} = function(data) {
        // console.log('remove{{ model_name }}');
        self.{{ model_args }}.remove(data);
    };

    self.destroy{{ model_name }} = function(data) {
        // console.log('destroy{{ model_name }}');
        self.{{ model_args }}.destroy(data);
    };

    self.delete{{ model_name }} = function(data) {
        // console.log('delete{{ model_name }}');
        var index = self.{{ model_args }}.indexOf(data);
        self.{{ model_args }}()[index].DELETE(true);
    }

    self.sort{{ model_name }}sAsc = function() {
        // console.log('sort{{ model_name }}sAsc');
        self.{{ model_args }}.sort(function(a, b) {
            var a_comparator = a.{{ comparator }}();
            var b_comparator = b.{{ comparator }}();
            if (!a_comparator) { a_comparator = undefined; }
            if (!b_comparator) { b_comparator = undefined; }
            var result = a_comparator>b_comparator?-1:a_comparator<b_comparator?1:0;

            return result;
        });
    };

    self.sort{{ model_name }}sDesc = function() {
        // console.log('sort{{ model_name }}sDesc');
        self.{{ model_args }}.sort(function(a, b) {
            var a_comparator = a.{{ comparator }}();
            var b_comparator = b.{{ comparator }}();
            if (!a_comparator) { a_comparator = undefined; }
            if (!b_comparator) { b_comparator = undefined; }
            var result = a_comparator<b_comparator?-1:a_comparator>b_comparator?1:0;

            return result;
        });
    };

    self.afterAdd{{ model_name }} = function(element, index, data) {
        if (element.nodeType !== 1) { return; }
        // console.log('afterAdd{{ model_name }}');

        element.style.display = 'none';

        var {{ model_args }}_index = self.{{ model_args }}().length - 1;
        var prefix = empty_prefix.replace(
            '__prefix__', {{ model_args }}_index
        );
        update_prefix(element, empty_prefix, prefix);
        total_form_count.value = parseInt(total_form_count.value) + 1;
        data.form_prefix(prefix);

        if (typeof self.afterAdd{{ model_name }}Callback === 'function') {
            self.afterAdd{{ model_name }}Callback(element, index, data);
        }
        else {
            element.style.display = 'block';
        }
    };
