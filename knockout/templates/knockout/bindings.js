
var data = (!{{ ignore_data|yesno:"true,false" }} && typeof {{ model_data_string }} !== 'undefined') ? {{ model_data_string }} : null;
ko.applyBindings(new {{ view_model_string }}(data),
                 document.getElementById("{% if element_id %}{{ element_id }}{% else %}{{ view_model_string|lower }}{% endif %}"));
