
ko.applyBindings(new {{ view_model_string }}({{ model_data_string }}),
                 document.getElementById("{% if element_id %}{{ element_id }}{% else %}{{ view_model_string|lower }}{% endif %}"));
