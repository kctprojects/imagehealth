function hex (c) {
    var s = "0123456789abcdef";
    var i = parseInt (c);
    if (i == 0 || isNaN (c))
      return "00";
    i = Math.round (Math.min (Math.max (0, i), 255));
    return s.charAt ((i - i % 16) / 16) + s.charAt (i % 16);
}
  
  /* Convert an RGB triplet to a hex string */
  function convertToHex (rgb) {
    return hex(rgb[0]) + hex(rgb[1]) + hex(rgb[2]);
}
  
/* Remove '#' in color hex string */
function trim (s) { return (s.charAt(0) == '#') ? s.substring(1, 7) : s }
  
/* Convert a hex string to an RGB triplet */
function convertToRGB (hex) {
    var color = [];
    color[0] = parseInt ((trim(hex)).substring (0, 2), 16);
    color[1] = parseInt ((trim(hex)).substring (2, 4), 16);
    color[2] = parseInt ((trim(hex)).substring (4, 6), 16);
    return color;
}
  
function generateColor(colorStart,colorEnd,colorCount){
  
    // The beginning of your gradient
    var start = convertToRGB (colorStart);    
  
    // The end of your gradient
    var end   = convertToRGB (colorEnd);    

    // The number of colors to compute
    var len = colorCount;
  
    //Alpha blending amount
    var alpha = 0.0;
  
    var saida = [];
      
    for (i = 0; i < len; i++) {
        var c = [];
          
        c[0] = start[0] * (1 - alpha) + alpha * end[0];
        c[1] = start[1] * (1 - alpha) + alpha * end[1];
        c[2] = start[2] * (1 - alpha) + alpha * end[2];
        alpha += (1.0/(len-1));
  
        saida.push("#" + convertToHex (c));
          
    }
    return saida;
}
/*
var tmp = generateColor('#000000','#ff0ff0',10);
  
for (cor in tmp) {
    $('#result_show').append("<div style='padding:8px;color:#FFF;background-color:#"+tmp[cor]+"'>COLOR "+cor+"° - #"+tmp[cor]+"</div>")
   
}
*/
//-------------------------
function hslToRgb(h, s, l) {
    var r, g, b;
  
    if (s == 0) {
      r = g = b = l; // achromatic
    } else {
      function hue2rgb(p, q, t) {
        if (t < 0) t += 1;
        if (t > 1) t -= 1;
        if (t < 1/6) return p + (q - p) * 6 * t;
        if (t < 1/2) return q;
        if (t < 2/3) return p + (q - p) * (2/3 - t) * 6;
        return p;
      }
  
      var q = l < 0.5 ? l * (1 + s) : l + s - l * s;
      var p = 2 * l - q;
  
      r = hue2rgb(p, q, h + 1/3);
      g = hue2rgb(p, q, h);
      b = hue2rgb(p, q, h - 1/3);
    }
  
    c = [ r * 255, g * 255, b * 255 ];
    return "#" + convertToHex (c)
  }
//--------------------------
function nmax(numbers, limit) {
    var ret = limit;
    for (var i = 0; i < numbers.length; i++) {
        if (!isNaN(numbers[i])) {
            if (numbers[i] > ret) {
                ret = numbers[i];
            }
        }
    }
    return ret;
}
function nmin(numbers, limit) {
    var ret = limit;
    for (var i = 0; i < numbers.length; i++) {
        if (!isNaN(numbers[i])) {
            if (numbers[i] < ret) {
                ret = numbers[i];
            }
        }
    }
    return ret;
}
function normalize(numbers) {

    //var max = Math.max.apply(Math, numbers);
    //var min = Math.min.apply(Math, numbers);
    var max = nmax(numbers, -1);
    var min = nmin(numbers, 101);
    var range = max - min;
    //console.log(max, min, numbers);

    for (var i = 0; i < numbers.length; i++) {
        numbers[i] = (numbers[i] - min) / range * 100.0;
    }
    return numbers;
}
function normalize2(numbers, globalmin, globalmax) {

    //var max = Math.max.apply(Math, numbers);
    //var min = Math.min.apply(Math, numbers);
    var max = globalmax;
    var min = globalmin;
    var range = max - min;
    //console.log(max, min, numbers);

    for (var i = 0; i < numbers.length; i++) {
        numbers[i] = (numbers[i] - min) / range * 100.0;
    }
    return numbers;
}

//--------------------------
function responsivefy(svg) {
    // get container + svg aspect ratio
    var container = d3.select(svg.node().parentNode),
        width = parseInt(svg.style("width")),
        height = parseInt(svg.style("height")),
        aspect = width / height;

    // add viewBox and preserveAspectRatio properties,
    // and call resize so that svg resizes on inital page load
    svg.attr("viewBox", "0 0 " + width + " " + height)
        .attr("perserveAspectRatio", "xMinYMid")
        .call(resize);

    // to register multiple listeners for same event type, 
    // you need to add namespace, i.e., 'click.foo'
    // necessary if you call invoke this function for multiple svgs
    // api docs: https://github.com/mbostock/d3/wiki/Selections#on
    d3.select(window).on("resize." + container.attr("id"), resize);

    // get width of container and resize svg to fit it
    function resize() {
        var targetWidth = parseInt(container.style("width"));
        svg.attr("width", targetWidth);
        svg.attr("height", Math.round(targetWidth / aspect));
    }
}

var colormap = generateColor('#ff0000','#00ff00',101);
console.log(colormap);
function refresh() {
    var iage = document.getElementById("iage").value;
    var iecon = document.getElementById("iecon").value;
    var irent = document.getElementById("irent").value;
    var iedu = document.getElementById("iedu").value;
    var irace = document.getElementById("irace").value;
    var bnormalize = document.getElementById('normalize').checked;

    //health = Array.from({length: 144}, () => colormap[Math.floor(Math.random() * 40)]);
    //health = healhArray[0][iage]
    /*
    healthData = [[129, 64.8], [128, 63.6], [20, 64.6], [95, 62.2], [42, 65.2], [34, 63.2], [76, 60.0], [52, 63.6], [49, 65.2], [39, 67.4], [112, 54.2], [127, 61.6], [122, 62.6], [24, 54.6], [69, 62.8], [108, 61.4], [41, 69.6], [57, 59.6], [30, 55.8], [71, 60.8], [109, 59.8], [96, 63.8], [133, 68.2], [75, 60.2], [120, 62.6], [33,
        64.4], [123, 62.8], [92, 61.4], [66, 64.6], [59, 65.4], [47, 63.8], [126, 61.0], [93, 61.0], [26, 59.6], [83, 60.4], [62, 63.2], [9, 63.6], [138, 59.0], [5, 57.0], [32, 61.8], [11, 65.0], [13, 60.4], [44, 58.4], [102, 63.2],
        [101, 64.8], [25, 57.0], [65, 63.4], [140, 65.0], [53, 61.4], [88, 62.8], [87, 65.0], [134, 65.0], [48, 66.6], [8, 60.8], [21, 59.6], [22, 57.8], [106, 62.6], [125, 60.6], [14, 63.0], [90, 63.8], [110, 57.2], [124, 59.4], [78, 59.6], [6, 58.2], [15, 69.6], [114, 65.0],
        [117, 62.2], [38, 64.8], [105, 70.0], [103, 68.6], [56, 68.4], [84, 61.2], [19, 60.0], [132, 60.0], [29, 62.4], [12, 65.0], [130, 64.6], [17, 60.6], [135, 59.6], [73, 59.0], [115,
        54.4], [2, 56.4], [99, 66.6], [104, 61.4], [18, 58.2], [50, 63.2], [36, 61.6], [82, 64.0], [68, 66.4], [74, 57.8], [121, 55.8], [107, 60.0], [54, 59.4], [58, 64.2], [80, 62.8], [45, 61.6], [23, 61.6], [67, 63.4], [46, 65.6],
        [10, 68.2], [72, 58.2], [4, 59.6], [111, 57.2], [86, 61.4], [98, 65.8], [131, 63.8], [89,
        68.4], [28, 55.0], [139, 56.6], [85, 55.4], [70, 65.0], [40, 66.4], [116, 66.0], [16, 64.8], [118, 63.0], [61, 58.0], [63, 65.6], [3, 60.2], [55, 57.8], [81, 63.6], [79, 61.0], [43, 58.8], [77, 63.8], [136, 58.4], [1, 60.6],
        [35, 60.2], [113, 53.2], [91, 59.2], [119, 61.6], [51, 63.2], [37, 62.6], [7, 61.8], [137, 60.2], [64, 64.0], [60, 62.8], [94, 62.0], [100, 65.2], [97, 63.8], [27, 58.6], [31, 61.4]];
    health = [];
    healthData.forEach(function(entry) {
        //health[entry[0]] =  (entry[1] - 50) * 4;
        health[entry[0]] =  entry[1]
    });
    */
    health = [];
    var ageData = healthArray.age[iage];
    var incomeData = healthArray.income[iecon];
    var houseData = healthArray.housing[irent];
    var educationData = healthArray.education[iedu];
    var raceData = healthArray.race[irace];
    var codes = healthArray.codes;
    console.log(codes);
    for (var i = 0; i < ageData.length; i++) {
        health[codes[i]] = (ageData[i] + incomeData[i] + houseData[i] + educationData[i] + raceData[i]) / 5;
    }
    if (bnormalize) {
        //health = normalize(health);
        health = normalize2(health, healthArray.globalMin, healthArray.globalMax);
    }
    //console.log(iage, iecon, irent, iedu);
    redrawMap(health);
}

function redrawMap(health) {
    //d3.select("#n097").attr("fill", "rgb(100, 149, 237)");
    //d3.select("#n027").attr("fill", "rgb(255, 0, 0)");
    d3.selectAll("path")  //here's how you get all the nodes
        .each(function(d) {
            //console.log(d.properties.AREA_S_CD, health[parseInt(d.properties.AREA_S_CD)]);
            //d3.select(this).attr("fill", colormap[Math.round(health[parseInt(d.properties.AREA_S_CD)])]);
            d3.select(this).attr("fill", hslToRgb(health[parseInt(d.properties.AREA_S_CD)] / 100 * 0.33, 1, 0.5));
            d3.select(this).attr("data-health", health[parseInt(d.properties.AREA_S_CD)]);
        });
    //console.log("redrawMap done");
}

//---------------
function init() {
    console.log("start");

    d3.json(
        "NEIGHBORHOODS_WGS84.geojson").then(
        function (json) {
            console.log("fn");
            //dimensions
            var w = 1024;
            var h = 380;

            var svg = d3.select("#chart").append("svg")
            .attr("width", w)
            .attr("height", h).call(responsivefy);;

            console.log("append");
            //create geo.path object, set the projection to merator bring it to the svg-viewport
            //var projection = d3.geoMercator().translate([w/2, h/2]).scale(2200).center([0,40]);
            //var path = d3.geoPath().projection(projection);
            var projection = d3.geoMercator()
                //.translate([111200, 68300])
                //.scale(80000);
                .scale(50000)
                .translate([111200-55500+13000+1000, 68300-34000+8000+380]);

            var path = d3.geoPath()
                .projection(projection);
                /*
            console.log(json.features);
            var b = path.bounds(json.features),
            s = .95 / Math.max((b[1][0] - b[0][0]) / w, (b[1][1] - b[0][1]) / h),
            t = [(w - s * (b[1][0] + b[0][0])) / 2, (h - s * (b[1][1] + b[0][1])) / 2];
            console.log(b);
            projection
            .scale(s)
            .translate(t);*/
            console.log("path");
            //return;
            //draw svg lines of the boundries
            svg.append("g")
                .attr("class", "black")
                .selectAll("path")
                .data(json.features)
                .enter()
                .append("path")
                .attr("id", function(d) {return "n"+d.properties.AREA_S_CD})
                .attr("fill", "grey")
                .attr("stroke", "black")
                .attr("data-name", function(d) {return d.properties.AREA_NAME})
                .attr("d", path)
                .append("title")
                .text(function(d) {return d.properties.AREA_NAME});
            refresh();
            console.log("fn done");
        });
    console.log("done");
}