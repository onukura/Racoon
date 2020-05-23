// Markdown to HTML
$("#description_submission").keyup(function() {
    $('#marked-preview').html(DOMPurify.sanitize(marked($(this).val())));
});