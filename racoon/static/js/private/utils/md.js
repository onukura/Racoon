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
