var datamap={}

function loadalltests () {
    $.get("json/countries.json",function(data) {
        for (c in data) {
            if (data[c].cc !="BB") {
                datamap[data[c].cc]=data[c].percent+1; 
                }
            }
            
        $('#world-map').vectorMap({
            map: 'world_mill_en',
            series: {
                regions: [{
                    values: datamap,
                    scale: ['#00FF00', '#FFFF00','#FF0000'],
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
    $.get("json/country-"+cc+".json", function(data ) {
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

$(document).ready(function () { loadalltests() })
