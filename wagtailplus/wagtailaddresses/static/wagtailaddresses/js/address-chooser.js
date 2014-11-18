function createAddressChooser(id) {
    var chooserElement  = $('#' + id + '-chooser');
    var objTitle        = chooserElement.find('.title');
    var input           = $('#' + id);

    $('.action-choose', chooserElement).click(function() {
        ModalWorkflow({
            'url': window.chooserUrls.addressChooser,
            'responses': {
                'addressChosen': function(objData) {
                    input.val(objData.id);
                    objTitle.text(objData.title);
                    chooserElement.removeClass('blank');
                }
            }
        });
    });

    $('.action-clear', chooserElement).click(function() {
        input.val('');
        chooserElement.addClass('blank');
    });
}