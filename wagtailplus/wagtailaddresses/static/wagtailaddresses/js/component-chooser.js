function createComponentChooser(id, url) {
    var chooserElement  = $('#' + id + '-chooser');
    var objTitle        = chooserElement.find('.title');
    var input           = $('#' + id);

    $('.action-choose', chooserElement).click(function() {
        ModalWorkflow({
            'url': url,
            'responses': {
                'componentChosen': function(objData) {
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

    $('.action-edit', chooserElement).click(function() {
        ModalWorkflow({
            'url': '/admin/addresses/edit-component/' + input.val() + '/',
            'responses': {
                'componentChosen': function(objData) {
                    input.val(objData.id);
                    objTitle.text(objData.title);
                    chooserElement.removeClass('blank');
                }
            }
        });
    });
}