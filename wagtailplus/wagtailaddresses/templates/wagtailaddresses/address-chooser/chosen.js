function(modal) {
    modal.respond('addressChosen', {{ instance_json|safe }});
    modal.close();
}