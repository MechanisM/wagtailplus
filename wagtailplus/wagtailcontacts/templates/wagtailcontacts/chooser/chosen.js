function(modal) {
    modal.respond('contactChosen', {{ instance_json|safe }});
    modal.close();
}