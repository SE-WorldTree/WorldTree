// Delay loading any function until the html dom has loaded. All functions are
// defined in this top level function to ensure private scope.
jQuery(document).ready(function () {

    // Installs error handling.
    jQuery.ajaxSetup({
        error: function(resp, e) {
            if (resp.status == 0){
                alert('You are offline!!\n Please Check Your Network.');
            } else if (resp.status == 404) {
                alert('Requested URL not found.');
            } else if (resp.status == 500) {
                alert('Internel Server Error:\n\t' + resp.responseText);
            } else if (e == 'parsererror') {
                alert('Error.\nParsing JSON Request failed.');
            } else if (e == 'timeout') {
                alert('Request timeout.');
            } else {
                alert('Unknown Error.\n' + resp.responseText);
            }
        }
    });  // error:function()

    var svg_div = jQuery('#graphviz_svg_div');

    function UpdateGraphviz() {
	    svg_div.html("");
        // Generate the Visualization of the Graph into "svg".
        var arrv = jQuery('#v_data').val().split('\n');
        var arre = jQuery('#e_data').val().split('\n');
        var sizv = arrv.length - 1;
        sizv = (sizv - sizv % 2) / 2;
        var size = arre.length - 1;
        size = (size - size % 3) / 3;

        var arrs = new Array(1+sizv+size+1);
        arrs[0] = "digraph G {";
        for (var i = 0 ; i < sizv ; i++)
            arrs[i+1] = arrv[i*2] + " [ label = \"" + arrv[i*2+1] + "\" ]; ";
        for (i = 0 ; i < size ; i++)
            arrs[i+1+sizv] = arre[i*3+1] + " -> " + arre[i*3+2] + "; ";
        arrs[1+sizv+size] = "}";

        var data = arrs.join('\n');
        //svg_div.html(data)
        var svg = Viz(data, "svg");
        //Sort
        var tmparr = svg.split("<g");
        tmparr[tmparr.length-1] = tmparr[tmparr.length-1].split("</g")[0]+"</g>";
        var head0 = tmparr[0] , head1 = tmparr[1];
        tmparr[0] = tmparr[1] = "";
        tmparr.sort();
        tmparr[0] = head0;
        tmparr[1] = head1;
        svg = tmparr.join("<g") + "</svg>";

        //Add url:
        svg = svg.replace("<g", "<qwertier"); // Protect

        for (i = 0 ; i < size ; i++) {
            svg = svg.replace("<g", "<a href = \"../edgeDetail?id=" + arre[i * 3] + "\"> <qwertier");
            svg = svg.replace("</g>", "</qwertier> </a>");
        }
        for (i = 0 ; i < sizv ; i++) {
            svg = svg.replace("<g", "<a href = \"../vertexDetail?id=" + arrv[i * 2] + "\"> <qwertier");
            svg = svg.replace("</g>", "</qwertier> </a>");
        }

	    svg = svg.replace(/qwertier/g, "g"); // Recovery

        svg = svg.replace(/<!--[^<>]*-->/g, ""); // Remove wrong labels

        svg_div.html(svg);
    }

    UpdateGraphviz();
});
