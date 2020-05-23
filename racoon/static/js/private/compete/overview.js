// Markdown to HTML
$(function () {
    let obj_overview = $('#markdown_description_overview');
    obj_overview.html(DOMPurify.sanitize(marked(obj_overview.text())));
    let obj_eval = $('#markdown_description_eval');
    obj_eval.html(DOMPurify.sanitize(marked(obj_eval.text())));
})