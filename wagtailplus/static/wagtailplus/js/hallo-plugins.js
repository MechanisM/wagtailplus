
(function() {
    (function($) {
        return $.widget('IKS.togglesource', {
            options: {
                uuid: '',
                editable: null
            },

            populateToolbar: function(toolbar) {
                var button, widget;
     
                widget  = this;
                button  = $('<span></span>');
    
                button.hallobutton({
                    uuid:       this.options.uuid,
                    editable:   this.options.editable,
                    label:      'Toggle Source',
                    icon:       'icon-code',
                    command:    null
                });
    
                toolbar.append(button);
    
                return button.on('click', function(event) {
                    // URL is assigned in wagtail_hooks.py.
                    var workflow = ModalWorkflow({'url': window.toggleHalloSourceURL});

                    // Assign the hallo instance to the workflow.
                    workflow.hallo = widget.options.editable;
                });
            }
        });
    })(jQuery);
}).call(this);