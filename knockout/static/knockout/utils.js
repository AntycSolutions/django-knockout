
function update_prefix(element, empty_prefix, prefix) {
    var attributes = element.attributes;
    for (var i = 0; i < attributes.length; ++i) {
        var attribute = attributes[i];
        var value = attribute.value.replace(empty_prefix, prefix);
        attribute.value = value;
    }

    var children = element.children;
    for (var i = 0; i < children.length; ++i) {
        var child = children[i];
        update_prefix(child, empty_prefix, prefix);
    }
}

function clickChecked(data, event) {
    if (event.currentTarget.checked) {
        event.currentTarget.parentElement.style.opacity = 0.5;
    }
    else {
        event.currentTarget.parentElement.style.opacity = "";
    }

    return true;
};


ko.observableArray.fn.swap = function(index1, index2) {
        this.valueWillMutate();

        var temp = this()[index1];
        this()[index1] = this()[index2];
        this()[index2] = temp;

        this.valueHasMutated();
    }

ko.bindingHandlers.fadeVisible = {
    init: function(element, valueAccessor) {
        // Initially set the element to be instantly visible/hidden
        //  depending on the value
        var value = valueAccessor();
        // console.log('fadeVisible', element, ko.unwrap(value));
        // Use "unwrapObservable" so we can handle values that may
        //  or may not be observable
        $(element).toggle(ko.unwrap(value));
    },
    update: function(element, valueAccessor) {
        // Whenever the value subsequently changes, slowly fade the
        //  element in or out
        var value = valueAccessor();
        ko.unwrap(value) ? $(element).fadeIn() : $(element).fadeOut();
    }
};
