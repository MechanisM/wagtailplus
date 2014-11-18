function(modal) {
    function ajaxifyLinks (context) {
        $('a.address-choice', context).click(function() {
            modal.loadUrl(this.href);
            return false;
        });

        $('.pagination a', context).click(function() {
            var page = this.getAttribute("data-page");
            setPage(page);
            return false;
        });
    };

    var searchUrl = $('form.address-search', modal.body).attr('action')

    function search() {
        $.ajax({
            url: searchUrl,
            data: {q: $('#id_q').val()},
            success: function(data, status) {
                $('#search-results').html(data);
                ajaxifyLinks($('#search-results'));
            }
        });
        return false;
    };

    function setPage(page) {
        if($('#id_q').val().length){
            dataObj = {q: $('#id_q').val(), p: page};
        }
        else {
            dataObj = {p: page};
        }

        $.ajax({
            url: searchUrl,
            data: dataObj,
            success: function(data, status) {
                $('#search-results').html(data);
                ajaxifyLinks($('#search-results'));
            }
        });

        return false;
    }

    ajaxifyLinks(modal.body);

    function submitForm() {
        var formdata = new FormData(this);

        $.ajax({
            url: this.action,
            data: formdata,
            processData: false,
            contentType: false,
            type: 'POST',
            dataType: 'text',
            success: function(response){
                modal.loadResponseText(response);
            }
        });

        return false;
    }

    $('form.address-create', modal.body).submit(submitForm);
    $('form.address-edit', modal.body).submit(submitForm);
    $('form.address-search', modal.body).submit(search);

    $('#id_q').on('input', function() {
        clearTimeout($.data(this, 'timer'));
        var wait = setTimeout(search, 50);
        $(this).data('timer', wait);
    });

    {% url 'wagtailadmin_tag_autocomplete' as autocomplete_url %}
    $('#id_tags', modal.body).tagit({
        autocomplete: {source: "{{ autocomplete_url|addslashes }}"}
    });
    
    function detectErrors() {
        var errorSections = {};

        // First count up all the errors
        $('form.address-create .error-message').each(function(){
            var parentSection = $(this).closest('section');
    
            if(!errorSections[parentSection.attr('id')]){
                errorSections[parentSection.attr('id')] = 0;
            }
    
            errorSections[parentSection.attr('id')] = errorSections[parentSection.attr('id')]+1;
        });
    
        // Now identify them on each tab
        for(var index in errorSections) {
            $('.tab-nav a[href=#'+ index +']').addClass('errors').attr('data-count', errorSections[index]);
        }   
    }
    
    detectErrors();
}