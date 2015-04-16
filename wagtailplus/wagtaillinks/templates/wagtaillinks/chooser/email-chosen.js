function(modal) {
    modal.respond('pageChosen', {{ instance_json|safe }});
    modal.close();
}