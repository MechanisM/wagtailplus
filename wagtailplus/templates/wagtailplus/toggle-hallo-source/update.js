function(modal) {
    // Grab the raw source code textarea element.
    var raw = $('textarea', modal.body);

    // Update with current hallo instance contents.
    raw.html(modal.hallo.getContents());

    // Update hallo instance with raw source code.
    $('input[type=button]', modal.body).click(function() {
        modal.hallo.setContents(raw.val());
        modal.hallo.element.trigger('change');
        modal.close();
    });
}