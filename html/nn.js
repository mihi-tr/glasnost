var datamap={};

var test="";

var colorscales=[["#00FF00","#FFFF00","#FF0000"],["#e4f264","#8fd772","#48b581","#149084","#1d6a76","#2c4559"]];
var cindex=1;
var colorscale=colorscales[1];

function hex_to_rgb(hx) {
    var c=parseInt(hx.replace("#",""),16);
    var red=c>>16 &0xFF;
    var green=c>>8 &0xFF;
    var blue=c & 0xFF;
    return ([red,green,blue]);
    }

function switch_colorscales() {
    if (cindex<colorscales.length-1) {
        cindex++;
        }
    else {
        cindex=0;
        }
    colorscale=colorscales[cindex];  
    var mapobject=$("#world-map").vectorMap("get","mapObject");
    mapobject.series.regions[0].scale.scale=colorscale.map(hex_to_rgb);
    loaddata();
    scalebar();

    }
function number_length(n,l) {
    while (n.length<l) {
        n="0"+n
        }
    return n    
    }
function rgb_to_hex(rgb) {
    var c=rgb[0]<<16 | rgb[1] <<8 | rgb[2];
    return ("#"+number_length(c.toString(16),6));
    }

function rgb_diff(a,b) {
    return ([a[0]-b[0],a[1]-b[1],a[2]-b[2]])
    }

function rgb_mult(a,d) {
    return ([a[0]*d,a[1]*d,a[2]*d])
    }

function rgb_add(a,b) {
    return([a[0]+b[0],a[1]+b[1],a[2]+b[2]])
    }

function map_value_to_color(value,min,max,mincolor,maxcolor) {
    var minc=hex_to_rgb(mincolor);
    var maxc=hex_to_rgb(maxcolor);
    var cv=rgb_diff(maxc,minc);
    var vd=(value-min)/(max-min);
    var rc=rgb_add(minc,rgb_mult(cv,vd))
    return rgb_to_hex(rc)
    }

function dorange(min,max,step) {
    var r=[];
    for (var i=min; i<=max; i=i+step) {
        r.push(i)
        }
    return (r);    
    }

function map_value_to_range(value,min,max,range) {
    var vstep=(max-min)/(range.length-1);
    var vr=dorange(min,max,vstep);
    var r;
    for (var i=0; i<range.length; i++) {
        if ((vr[i]<=value) && (vr[i+1]>=value)) {
            r=map_value_to_color(value,vr[i],vr[i+1],range[i],range[i+1]);
            }
        }
    return (r);    
    }

function scalebar() {
    var html=[]
    for (var i=0;i<=100;i=i+10) {
        html.push("<span style='background: "
        +map_value_to_range(i,0,100,colorscale)+"'>"+i+"%</span>")
        }
    $("#scalebar").html(html)    
        }

function testlist() {
    $.get("json/tests.json", function(data) {
        for (i in data) {
            $("#testselector").append("<option value="
                +data[i]+">"+data[i]+"</option>");
                }
        })
    }

function period() {
    $.get("json/period.json",function (data) {
        $("#period-begin").html(data["begin"]);
        $("#period-end").html(data["end"]);
        }
        )
    }
function selecttest() {
    test=$("#testselector").val();
    loaddata();
};


function loaddata () {
    var url;
    if (test) {
        url="json/countries-"+test+".json";
        }
    else {
        url="json/countries.json";
        }
        
    $.get(url,function(data) {
        var mapobject=$("#world-map").vectorMap("get","mapObject");
        for (var i in mapobject.series.regions[0].values) {
            var a={}
            a[i]=0;
            try {
            mapobject.series.regions[0].setValues(a);
            }
            catch (err) {
                console.log(a);
                console.log("Error on resetting country "+i)
                }
            }
        datamap={};
        for (c in data) {
            if (! (data[c].cc in ["BB","A1","A2"])) {
                datamap[data[c].cc]=data[c].percent+1; 
                }
            }
        mapobject.series.regions[0].setValues(datamap);
        /*$('#world-map').vectorMap("set","series",
            ) */
            }) 
            }

function loadcountryinfo(cc) {
    var url;
    if (test) {
        url="json/country-"+cc+"-"+test+".json";
        }
    else {
        url="json/country-"+cc+".json";
        };
    $.get(url, function(data ) {
        $("#countrycode").html(cc);

        var html=[
        "<thead><tr><th>Provider</th><th>Total tests</th><th>Shaped ",
        "tests</th><th>Percent tests shaped</th></tr></thead>",
         "<tbody>"]
        for (i in data) {
            var c=map_value_to_range(data[i].percent,0,100,colorscale);
            html.push("<tr><td>",data[i].provider,"</td><td>",data[i].total,
            "</td><td>",data[i].shaped,"</td><td style='background: "
            +c+"'>",Math.round(data[i].percent*10)/10,"%</td></tr>")
        }
        html.push("</tbody>")
        $("#providertable").html(html.join(""));
        $("#providertable").tablesorter([[4,0],[0,0]]);
        $(".aboutTab").hide();
        $("#countryinfo-wrapper").show();
        })
    }

$(document).ready(function () { testlist(); scalebar(); period();
        $('#world-map').vectorMap({
            map: 'world_mill_en',
            series: {regions: [{
                    values: datamap,
                    scale: colorscale,
                    attribute: 'fill',
                    min: 1,
                    max: 101
                }]
                },
            onRegionClick: function (e,str) { loadcountryinfo(str); }    
            })
         loaddata();   
            })
