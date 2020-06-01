function main(data, header, country_map, indicator_map){

	// Set the dimensions and margins of the graph
	var margin = {top: 50, right: 50, bottom: 50, left: 50},
		legend_width = 350,
		width = 900 - margin.left - margin.right,
		height = 700 - margin.top - margin.bottom;

	// Append the svg object to the body of the page
	var svg = d3.select("#plot")
		.append("svg")
		.attr("width", width + margin.left + margin.right + legend_width)
		.attr("height", height + margin.top + margin.bottom)
		.append("g")
		.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

	// Extract the indicator codes from header
    var scatter_indicators = header.filter(item => !["Year", "CountryCode"].includes(item));
    var indicator0 = scatter_indicators[0];
    var indicator1 = scatter_indicators[1];
    var ind0_max_measurement = d3.max(data, function(d){return +d[indicator0]});
    var ind1_max_measurement = d3.max(data, function(d){return +d[indicator1]});
    var country_codes = d3.map(data, function(d){return(d.CountryCode)}).keys()

	// Add X axis
	var x = d3.scaleLinear()
		.domain([0, Math.round(ind0_max_measurement + (2-ind0_max_measurement%2))])
		.range([ 0, width ]);
	svg.append("g")
		.attr("transform", "translate(0," + height + ")")
		.call(d3.axisBottom(x));
	svg.append("text")
		.attr("transform", "translate(" + (width/2) + " ," + (height + 40) + ")")
		.style("text-anchor", "middle")
		.text(indicator_map[indicator0]);

	// Add Y axis
	var y = d3.scaleLinear()
		.domain([0, Math.round(ind1_max_measurement + (2-ind1_max_measurement%2))])
		.range([ height, 0]);
	svg.append("g")
		.call(d3.axisLeft(y));
	svg.append("text")
		.attr("transform", "rotate(-90)")
		.attr("y", 0 - margin.left)
		.attr("x", 0 - (height / 2))
		.attr("dy", "1em")
		.style("text-anchor", "middle")
		.text(indicator_map[indicator1]);

	// Color palette. One color per CountryCode
	var color = d3.scaleOrdinal()
		.domain(country_codes)
		.range(['#009900', '#ff0000', '#ff8000', '#00ff80', '#ffff33', '#0080ff', '#00ff00', '#cc0066', '#00994c'])

	// Highlight functions 
	var highlightColor = function(d){
		selected_Country = d.CountryCode
		d3.selectAll(".dot")
			.transition()
			.duration(200)
			.style("fill", "lightgrey")
			.attr("r", 3)
		d3.selectAll("." + selected_Country)
			.transition()
			.duration(200)
			.style("fill", color(selected_Country))
			.attr("r", 7)
	}

	var resetColor = function(){
		d3.selectAll('.dot')
			.each(function(d) {
				d3.select(this)
					.transition()
					.duration(200)
					.style('fill', function (d) { return color(d.CountryCode) })
					.attr("r", 5)
			}
		)
	}

	// Add dots
	svg.append('g')
		.selectAll("dot")
		.data(data).enter()
			.append("circle")
			.attr("class", function (d) { return "dot " + d.CountryCode } )
			.attr("cx", function (d) { return x(d[indicator0]); } )
			.attr("cy", function (d) { return y(d[indicator1]); } )
			.attr("r", 5)
			.style("fill", function (d) { return color(d.CountryCode) } )
			.on("mouseover", highlightColor)
    		.on("mouseout", resetColor);

    //Display Lagend
	var size = 20;
	var legend = svg.append("g")
		.attr("class", "legend")
		.attr("transform", "translate(" + width + "," + 20 + ")")
		.selectAll("g")
		.data(country_codes)
		.enter().append("g");

	legend.append("rect")
		.attr("x", 10)
		.attr("y", function(d,i){ return 10 + i*(size+20)}) 
		.attr("width", size)
		.attr("height", size)
		.style("fill", function(d){ return color(d)})
	legend.append("text")
		.attr("x", 10 + size*1.2)
		.attr("y", function(d,i){ return 10 + i*(size+20) + size/2}) 
		.text(function(d){ return country_map[d]})
		.attr("text-anchor", "left")
		.style('font-weight', 'bold')
		.style("font-size", "15px")
		.style("alignment-baseline", "middle")
}