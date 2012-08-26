var datamap={};

var test="";

var colorscale=["#00FF00","#FFFF00","#FF0000"]

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
        datamap={};
        for (c in data) {
            if (data[c].cc !="BB") {
                datamap[data[c].cc]=data[c].percent+1; 
                }
            }
        $('#world-map').html("")            
        $('#world-map').vectorMap({
            map: 'world_mill_en',
            series: {
                regions: [{
                    values: datamap,
                    scale: colorscale,
                    attribute: 'fill',
                    min: 1,
                    max: 101
                }]
                },
            onRegionClick: function (e,str) { loadcountryinfo(str); }    
            })
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
        var html=["<h1>"+cc+"</h1>","<table>",
        "<tr><th>Provider</th><th>Total tests</th><th>Shaped tests</th><th>Percent tests shaped</th></tr>"]
        for (i in data) {
            html.push("<tr><td>",data[i].provider,"</td><td>",data[i].total,
            "</td><td>",data[i].shaped,"</td><td>",data[i].percent,"%</td></tr>")
        }
        html.push("</table>")
        $("#countryinfo").html(html.join(""));
        
        })
    }

$(document).ready(function () { testlist(); period(); loaddata() })
