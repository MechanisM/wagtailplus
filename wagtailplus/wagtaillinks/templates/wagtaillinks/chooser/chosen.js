function(modal) {
    modal.respond('linkChosen', {{ instance_json|safe }});
    modal.close();
}