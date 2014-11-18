function(modal) {
    modal.respond('componentChosen', {{ instance_json|safe }});
    modal.close();
}