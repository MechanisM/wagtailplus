function(modal) {
    modal.respond('eventChosen', {{ instance_json|safe }});
    modal.close();
}