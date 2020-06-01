function main(data, header, max_measurement, country_map, indicator_map){

	// Set the dimensions and margins of the graph.
	var margin = {top: 50, right: 50, bottom: 50, left: 50},
		legend_width = 370,
		width = 900 - margin.left - margin.right,
		height = 700 - margin.top - margin.bottom;

	// Append the svg object to the body of the page.
	var svg = d3.select("#plot")
		.append("svg")
		.attr("width", width + margin.left + margin.right + legend_width)
		.attr("height", height + margin.top + margin.bottom)
		.append("g")
			.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

	// List of groups. Each group is a year with its measurements.
	var groups = d3.map(data, function(d){return(d.Year)}).keys()
	
	// List of subgroups. Each subgroup is CountryCode#IndicatorCode pair.
	var subgroups = header.filter(item => item !== "Year");

	// Add X axis.
	var x = d3.scaleBand()
		.domain(groups)
		.range([0, width])
		.padding([0.2]);
	svg.append("g")
		.attr("transform", "translate(0," + height + ")")
		.call(d3.axisBottom(x).tickValues(x.domain().filter((d, i) => i % ((groups.length>20) ? 2 : 1) === 0)));
	svg.append("text")
		.attr("transform", "translate(" + (width/2) + " ," + (height + 40) + ")")
		.style("text-anchor", "middle")
		.text("Year");

	// Add Y axis.
	var y = d3.scaleLinear()
		.domain([0, Math.round(max_measurement + (2-max_measurement%2))])
		.range([ height, 0 ]);
	svg.append("g")
		.call(d3.axisLeft(y));
	svg.append("text")
		.attr("transform", "rotate(-90)")
		.attr("y", 0 - margin.left)
		.attr("x", 0 - (height / 2))
		.attr("dy", "1em")
		.style("text-anchor", "middle")
		.text("Percentage (%)");

	// Scale for subgroups.
	var xSubgroup = d3.scaleBand()
		.domain(subgroups)
		.range([0, x.bandwidth()])
		.padding([0.05])

	// Color palette. One color per subgroup.
	var color = d3.scaleOrdinal()
	    .domain(subgroups)
	    .range(['#009900', '#ff0000', '#ff8000', '#00ff80', '#ffff00', '#0000ff', '#00ff00', '#cc0066', '#00994c'])

	// Create a tooltip
	var tool_tip = d3.tip()
		.attr("class", "d3-tip")
		.offset([-8, 0])
		.html(function(d) { return "Value: " + (Math.round(d.value * 100) / 100) + "%";});
	svg.call(tool_tip);

	// Show the bars.
	svg.append("g")
		.selectAll("g")
		// Enter in data = loop group per group
		.data(data)
		.enter()
		.append("g")
		.attr("transform", function(d) { return "translate(" + x(d.Year) + ",0)"; })
		.selectAll("rect")
		// Enter in group = loop subgroup per subgroup
		.data(function(d) { return subgroups.map(function(key) { return {key: key, value: d[key]}; }); })
		.enter()
		.append("rect")
			.attr("x", function(d) { return xSubgroup(d.key); })
			.attr("y", function(d) { return y(d.value); })
			.attr("width", xSubgroup.bandwidth())
			.attr("height", function(d) { return height - y(d.value); })
			.attr("fill", function(d) { return color(d.key); })
			.on('mouseover', tool_tip.show)
			.on('mouseout', tool_tip.hide);

	//Display Lagend
	var size = 20;
	var legend = svg.append("g")
		.attr("class", "legend")
		.attr("transform", "translate(" + width + "," + 20 + ")")
		.selectAll("g")
		.data(subgroups)
		.enter().append("g");

	legend.append("rect")
		.attr("x", 40)
		.attr("y", function(d,i){ return 10 + i*(size+35)}) 
		.attr("width", size)
		.attr("height", size)
		.style("fill", function(d){ return color(d)})
	legend.append("text")
		.attr("x", 40 + size*1.2)
		.attr("y", function(d,i){ return 10 + i*(size+35) + size/2}) 
		.text(function(d){ return country_map[d.split("#")[0]]})
		.attr("text-anchor", "left")
		.style('font-weight', 'bold')
		.style("font-size", "15px")
		.style("alignment-baseline", "middle")
	legend.append("text")
		.attr("x", 40 + size*1.2)
		.attr("y", function(d,i){ return 25 + i*(size+35) + size/2}) 
		.text(function(d){ return indicator_map[d.split("#")[1]].split("(")[0]})
		.attr("text-anchor", "left")
		.style("font-size", "15px")
		.style("alignment-baseline", "middle")
	legend.append("text")
		.attr("x", 40 + size*1.2)
		.attr("y", function(d,i){ return 40 + i*(size+35) + size/2}) 
		.text(function(d){ return "(" + indicator_map[d.split("#")[1]].split("(")[1]})
		.attr("text-anchor", "left")
		.style("font-size", "15px")
		.style("alignment-baseline", "middle")
}
