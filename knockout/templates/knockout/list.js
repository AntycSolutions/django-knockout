
    self.{{ model_list }} = ko.observableArray(data);

    self.add{{ view_model_class }} = function(data) {
        // console.log('add{{ view_model_class }}');
        self.{{ model_list }}.push(new {{ view_model_class }}(data));
    };

    self.create{{ view_model_class }} = function(data) {
        // console.log('create{{ view_model_class }}');
        return new {{ view_model_class }}(data);
    };

    self.remove{{ view_model_class }} = function(data) {
        // console.log('remove{{ view_model_class }}');
        self.{{ model_list }}.remove(data);
    };

    self.destroy{{ view_model_class }} = function(data) {
        // console.log('destroy{{ view_model_class }}');
        self.{{ model_list }}.destroy(data);
    };

    self.delete{{ view_model_class }} = function(data) {
        // console.log('delete{{ view_model_class }}');
        var index = self.{{ model_list }}.indexOf(data);
        self.{{ model_list }}()[index].DELETE(true);
    }

    self.sort{{ view_model_class }}sAsc = function() {
        // console.log('sort{{ view_model_class }}sAsc');
        self.{{ model_list }}.sort(function(a, b) {
            var a_comparator = a.{{ comparator }}();
            var b_comparator = b.{{ comparator }}();
            if (!a_comparator) { a_comparator = undefined; }
            if (!b_comparator) { b_comparator = undefined; }
            var result = a_comparator>b_comparator?-1:a_comparator<b_comparator?1:0;

            return result;
        });
    };

    self.sort{{ view_model_class }}sDesc = function() {
        // console.log('sort{{ view_model_class }}sDesc');
        self.{{ model_list }}.sort(function(a, b) {
            var a_comparator = a.{{ comparator }}();
            var b_comparator = b.{{ comparator }}();
            if (!a_comparator) { a_comparator = undefined; }
            if (!b_comparator) { b_comparator = undefined; }
            var result = a_comparator<b_comparator?-1:a_comparator>b_comparator?1:0;

            return result;
        });
    };

    self.afterAdd{{ view_model_class }} = function(element, index, data) {
        if (element.nodeType !== 1) { return; }
        // console.log('afterAdd{{ view_model_class }}');

        element.style.display = 'none';

        var {{ model_list }}_index = self.{{ model_list }}().length - 1;
        var prefix = empty_prefix.replace(
            '__prefix__', {{ model_list }}_index
        );
        update_prefix(element, empty_prefix, prefix);
        total_form_count.value = parseInt(total_form_count.value) + 1;
        data.form_prefix(prefix);

        function_exists = (
            typeof self.afterAdd{{ view_model_class }}Callback === 'function'
        );
        if (function_exists) {
            self.afterAdd{{ view_model_class }}Callback(element, index, data);
        }
        else {
            element.style.display = 'block';
        }
    };
