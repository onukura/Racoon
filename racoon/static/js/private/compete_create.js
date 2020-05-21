// Extend marked.js
function marked_js_render(){
    // marked.js + highlight.js
    var renderer = new marked.Renderer()
    // code syntax highlight
    renderer.code = function (code, language) {
        return '<pre' + '><code class="hljs">' + hljs.highlightAuto(code).value + '</code></pre>';
    };
    // table tag
    renderer.table = function(header, body) {
        if (body) body = '<tbody>' + body + '</tbody>';

        return '<table class="table table-hover">'
            + '<thead>'
            + header
            + '</thead>'
            + body
            + '</table>';
    };
    marked.setOptions({
        renderer: renderer,
    });
}
$(function () {
    marked_js_render();
});

// Markdown to HTML
$("#description_md").keyup(function() {
    let markdown = $(this).val();
    $('#marked-preview').html(DOMPurify.sanitize(marked(markdown)));
});

var type_list = [
    {type: "regression", val:"mae", txt:"Mean Absolute Error"},
    {type: "regression", val:"mse", txt:"Mean Squared Error"},
    {type: "regression", val:"msle", txt:"Mean Squared Logarithmic Error"},
    {type: "regression", val:"rmse", txt:"Root Mean Squared Error"},
    {type: "classification", val:"accuracy", txt:"Accuracy"},
    {type: "classification", val:"auc", txt:"Area Under Curve(AUC)"},
    {type: "classification", val:"f1", txt:"F1 Score"},
    {type: "classification", val:"logloss", txt:"Log Loss"},
];

function createSelectBox() {
    var compete_type = $('input:radio[name="eval_type"]:checked').val();
    $("#metric").children().remove();
    for(var i=0;i<type_list.length;i++){
        if (compete_type === type_list[i].type) {
            $('#metric').append($('<option>').attr({ value: type_list[i].val, name: "metric" }).text(type_list[i].txt));
        }
    }
}
$(function () {
    createSelectBox();
    $("#expired_date").datepicker({
        dateFormat: "yy-mm-dd",
        minDate: 0,
    });
})
$('input:radio[name="eval_type"]').change(function () {
    createSelectBox()
})
