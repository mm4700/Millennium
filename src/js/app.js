






//draw the d3 chart for each ticker.
$("#company_overview").change(function() {
    //hide social worker and sponsor stuff
    value  = $(this).val();

    console.log(value)

    // Set the dimensions of the canvas / graph
    var margin = {top: 30, right: 20, bottom: 30, left: 50},
        width = 600 - margin.left - margin.right,
        height = 270 - margin.top - margin.bottom;

    // Set the ranges
    var x = d3.time.scale().range([0, width]);
    var y = d3.scale.linear().range([height, 0]);

    // Define the axes
    var xAxis = d3.svg.axis().scale(x)
        .orient("bottom").ticks(10);

    var yAxis = d3.svg.axis().scale(y)
        .orient("left").ticks(10);

    // // Define the line
    var valueline = d3.svg.line()
        .x(function (d) {
            return x(d.Date);
        })
        .y(function (d) {
            return y(d.PX_LAST);
        });


   //get ticker data from database for the company overview
    $.ajax({
        url: "http://localhost:5000/timeseries/" + value,
        type: 'GET',
        success: function(response) {
            $("#company_overview_chart").html("");
            $.ajax({
                url: "http://localhost:5000/firm_overview/" + value,
                type: 'GET',
                success: function(r1) {
                    res = JSON.parse(r1.overview);
                    res = res[0];

                    $("#ticker_name").text(res["Name"]);
                    $("#description").text(res["Description"]);
                    $("#GICS_Sector").text(res["GICS Sector"]);
                    $("#GICS_industry").text(res["GICS industry"]);
                    $("#GICS_industry_group").text(res["GICS Industry group"]);
                    $("#GICS_industry_subgroup").text(res["GICS Sub Industry Group"]);
                }
            });

            var data = JSON.parse(response.ts);
            var svg = d3.select("#company_overview_chart")
                .append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
                .append("g")
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


            x.domain(d3.extent(data, function (d) {
                return d.Date;
            }));
            y.domain([0, d3.max(data, function (d) {
                return d.PX_LAST;
            })]);


            // Add the valueline path.
            svg.append("path")
                .attr("class", "line")
                .attr("d", valueline(data));

            // Add the X Axis
            svg.append("g")
                .attr("class", "x axis")
                .attr("transform", "translate(0," + height + ")")
                .call(xAxis);

            // Add the Y Axis
            svg.append("g")
                .attr("class", "y axis")
                .call(yAxis);

        }
    });


});

// get firms into a dropdown list from database
$(function() {
    $.ajax({
        url: "http://localhost:5000/getFirms",
        type: 'GET',
        async:true,
        success: function(response) {
            $('#build_portfolio').html("");
            $('#ticker1').html("");
            $('#ticker2').html("");

            firms = response.firms;

            var list = [];
            firms.forEach(function( val) {
                $('#build_portfolio')
                    .append($("<option></option>")
                        .attr("value",val)
                        .text(val));

                $('#ticker1')
                    .append($("<option></option>")
                        .attr("value",val)
                        .text(val));

                $('#ticker2')
                    .append($("<option></option>")
                        .attr("value",val)
                        .text(val));

                $('#company_overview')
                    .append($("<option></option>")
                        .attr("value",val)
                        .text(val));

            });
        }
    });



//live data from alphavantage
    function f(stock) {
        d3.json("https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=" + stock + "&interval=1min&apikey=0ATTX6FGPXFFKBB9", function (data) {

            $("#live_data").html("");

            data = data["Time Series (1min)"]

            var margin = {top: 30, right: 20, bottom: 30, left: 50},
                width = 600 - margin.left - margin.right,
                height = 270 - margin.top - margin.bottom;

            // Set the ranges
            var x = d3.time.scale().range([0, width]);
            var y = d3.scale.linear().range([height, 0]);

            // Define the axes
            var xAxis = d3.svg.axis().scale(x)
                .orient("bottom").ticks(10);

            var yAxis = d3.svg.axis().scale(y)
                .orient("left").ticks(10);


            var svg = d3.select("#live_data")
                .append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
                .append("g")
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


            var dates= [];
            var str_dates =[];

            for(var k in data) {
                dates.push(Date.parse(k));
                str_dates.push(k);
            }

            var res = [];
            for(var i =0; i < str_dates.length; i ++) {
                res.push({
                    date: Date.parse(str_dates[i]),
                    close: parseFloat(data[str_dates[i]]["4. close"])
                })
            }

            x.domain(d3.extent(res, function (d) {
                return d.date;
            }));
            y.domain([d3.min(res, function (d) {
                return d.close;
            }), d3.max(res, function (d) {
                return d.close;
            })]);




            var	valueline = d3.svg.line()
                .x(function(d) { return x(d.date); })
                .y(function(d) { return y(d.close); });

            // Add the valueline path.
            svg.append("path")
                .attr("class", "line")
                .attr("d", valueline(res));

            // Add the X Axis
            svg.append("g")
                .attr("class", "x axis")
                .attr("transform", "translate(0," + height + ")")
                .call(xAxis);

            // Add the Y Axis
            svg.append("g")
                .attr("class", "y axis")
                .call(yAxis);

        });
        return true;
    }



    $("#stock_input").click(function (event) {
        event.preventDefault();
        event.stopPropagation();


        if(self.niubi) {
            window.clearInterval(self.niubi)
        }

        f($("#uname").val());

        self.niubi = setInterval( function() { f($("#uname").val()); }, 5000 );
    });

});


// upload/reset csv data
$("#upload_all_data" ).click(function( event ) {
    $.ajax({
        url: "http://localhost:5000/uploadAll",
        type: 'PUT',
        success: function(response) {
            //...
        }
    });

    event.preventDefault();
});

$( "#reset_all_data" ).click(function( event ) {

    $.ajax({
        url: "http://localhost:5000/resetAll",
        type: 'PUT',
        success: function(response) {
            //...
        }
    });
    event.preventDefault();
});

//stock comparison
$( "#stock_comparison" ).click(function( event ) {
    event.stopPropagation();
    event.preventDefault();

    var t1 = $("#ticker1").val();
    var t2 = $("#ticker2").val();

    $.post( "http://localhost:5000/stats", { ticker1: t1, ticker2: t2 })
        .done(function( data ) {
            console.log(data);

            $("#beta").text(data.beta);
            $("#corr").text(data.corr);
        });

    // event.preventDefault();
});

$("#build_portfolio").change(function(){
    $("#stock_weight").append("<label>" +  $(this).val() + "</label>\n" +
        "                    <input type=\"number\" id="+ $(this).val() +" />")
});


//build portfoio
$("#liguifan").click(function () {
    ids = []
    weights = []

    value = 0;
    var divs = $("#stock_weight :input");
    for(var i = 0; i < divs.length; i++){
        ids.push(divs[i].id);
        weights.push(divs[i].value);
        value = value + parseInt(divs[i].value);
    }

    if(value !=100 ) {
        alert("Error must add up to 100");

    } else {
        jf = JSON.stringify({
            ids: ids,
            weights: weights
        });

        $.post( "http://localhost:5000/add_portfolio", {'jf':jf}).done(function( data ) {
            console.log(data)
        });

        alert("Send portfolio successful !")
    }




});