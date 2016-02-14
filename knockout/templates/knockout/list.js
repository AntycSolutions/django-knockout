
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
        // console.log('add {{ model_name }}');
        self.{{ model_args }}.push(new {{ model_name }}());
    };

    self.create{{ model_name }} = function() {
        return new {{ model_name }}();
    };

    self.remove{{ model_name }} = function(data) {
        self.{{ model_args }}.remove(data);
    };

    self.destroy{{ model_name }} = function(data) {
        self.{{ model_args }}.destroy(data);
    };

    var sorted = false;

    self.sort{{ model_name }}sAsc = function() {
        self.{{ model_args }}.sort(function(a, b) {
            var a_comparator = a.{{ comparator }}();
            var b_comparator = b.{{ comparator }}();
            if (!a_comparator) { a_comparator = undefined; }
            if (!b_comparator) { b_comparator = undefined; }
            var result = a_comparator>b_comparator?-1:a_comparator<b_comparator?1:0;

            sorted = true;

            return result;
        });
    };

    self.sort{{ model_name }}sDesc = function() {
        self.{{ model_args }}.sort(function(a, b) {
            var a_comparator = a.{{ comparator }}();
            var b_comparator = b.{{ comparator }}();
            if (!a_comparator) { a_comparator = undefined; }
            if (!b_comparator) { b_comparator = undefined; }
            var result = a_comparator<b_comparator?-1:a_comparator>b_comparator?1:0;

            sorted = true;

            return result;
        });
    };

    self.afterAdd{{ model_name }} = function(elems) {
        for (var i = 0; i < elems.length; ++i) {
            if (elems[i].status == 'added') {
                var template = document.getElementById(empty_form_prefix);
                template.style.display = 'none';
                template.removeAttribute('id');

                var prefix = elems[i].value.form_prefix();
                if (!prefix) {
                    if (typeof empty_prefix === 'undefined') {
                        empty_prefix = '__prefix__';
                    }
                    var re = new RegExp(empty_prefix, "g");
                    prefix = empty_form_prefix.replace(
                        re, total_form_count.value
                    );
                }

                var children = template.children;
                self._update_prefix(children, prefix);

                if (!sorted) {
                    total_form_count.value = parseInt(total_form_count.value) + 1;
                }

                if (typeof self.afterAdd{{ model_name }}Callback === 'function') {
                    self.afterAdd{{ model_name }}Callback(
                        template, elems[i].value
                    );
                }
                else {
                    template.style.display = 'block';
                }
            }
            else {
                // console.log(elems[i].status);
            }
        }

        sorted = false;
    };

    self.afterAdd{{ model_name }}Test = function(element, index, data) {
        if (element.nodeType !== 1) { return; }
        // console.log('afterAdd {{ model_name }} Test');

        element.style.display = 'none';

        var prefix = data.form_prefix();
        if (!prefix) {
            if (typeof empty_prefix === 'undefined') {
                empty_prefix = '__prefix__';
            }
            var re = new RegExp(empty_prefix, "g");
            prefix = empty_form_prefix.replace(
                re, total_form_count.value
            );
            data.form_prefix(prefix);
        }

        var children = element.children;
        self._update_prefix(children, prefix);

        if (!sorted) {
            total_form_count.value = parseInt(total_form_count.value) + 1;
        }

        if (typeof self.afterAdd{{ model_name }}Callback === 'function') {
            self.afterAdd{{ model_name }}Callback(
                element, data
            );
        }
        else {
            element.style.display = 'block';
        }
    };

    self._update_prefix = function(children, prefix) {
        for (var i = 0; i < children.length; ++i) {
            var child = children[i];
            var attributes = child.attributes;
            for (var k = 0; k < attributes.length; ++k) {
                var attribute = attributes[k];
                var re = new RegExp(empty_form_prefix);
                var value = attribute.value.replace(re, prefix);
                attribute.value = value;
            }

            self._update_prefix(child.children, prefix);
        }
    }

    self.clickChecked = function(data, event) {
        if (event.currentTarget.checked) {
            event.currentTarget.parentElement.style.opacity = 0.5;
        }
        else {
            event.currentTarget.parentElement.style.opacity = "";
        }

        return true;
    };
