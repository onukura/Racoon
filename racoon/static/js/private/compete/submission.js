// Markdown to HTML
$("#description").keyup(function() {
    $('#marked-preview').html(DOMPurify.sanitize(marked($(this).val())));
});