// Markdown to HTML
$(function () {
    let obj_data = $('#markdown_description_data');
    obj_data.html(DOMPurify.sanitize(marked(obj_data.text())));
})
