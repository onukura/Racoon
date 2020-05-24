// Markdown to HTML
$("#description_overview").keyup(function() {
    $('#marked-preview-overview').html(DOMPurify.sanitize(marked($(this).val())));
});
$("#description_eval").keyup(function() {
    $('#marked-preview-eval').html(DOMPurify.sanitize(marked($(this).val())));
});
$("#description_data").keyup(function() {
    $('#marked-preview-data').html(DOMPurify.sanitize(marked($(this).val())));
});

// This "type" and "val" must match with python functions in "racoon/lib/evals/__init__.py"
var type_list = [
    {type: "regression", val:"score_mae", txt:"Mean Absolute Error"},
    {type: "regression", val:"score_mse", txt:"Mean Squared Error"},
    {type: "regression", val:"score_msle", txt:"Mean Squared Logarithmic Error"},
    {type: "regression", val:"score_rmse", txt:"Root Mean Squared Error"},
    {type: "classification", val:"score_accuracy", txt:"Accuracy"},
    {type: "classification", val:"score_auc", txt:"Area Under Curve(AUC)"},
    {type: "classification", val:"score_f1", txt:"F1 Score"},
];

function createSelectBox() {
    var compete_type = $('input:radio[name="metric_type"]:checked').val();
    $("#metric_name").children().remove();
    for(var i=0;i<type_list.length;i++){
        if (compete_type === type_list[i].type) {
            $('#metric_name').append($('<option>').attr({ value: type_list[i].val, name: "metric_name" }).text(type_list[i].txt));
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
