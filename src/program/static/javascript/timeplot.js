function main(data, country_map, indicator_map){

	// set the dimensions and margins of the graph
	var margin = {top: 50, right: 50, bottom: 50, left: 50},
		legend_width = 370,
		width = 900 - margin.left - margin.right,
		height = 700 - margin.top - margin.bottom;

	// Append the svg object to the body of the page
	var svg = d3.select("#plot")
		.append("svg")
		.attr("width", width + margin.left + margin.right + legend_width)
		.attr("height", height + margin.top + margin.bottom)
		.append("g")
			.attr("transform", "translate(" + margin.left + "," + margin.top + ")");
	var tooltip = d3.select('#tooltip');
	var tooltipLine = svg.append('line');

	var lines = d3.nest()
		.key(function(d) { return d.Code;})
		.entries(data);
	var codes = lines.map(function(d){return d.key;})
	var max_measurement = d3.max(data, function(d){return +d.Measurement});

	var groups = d3.map(data, function(d){return(d.Year)}).keys()

	// Add X axis
	var x = d3.scalePoint()
		.domain(groups)
		.range([0, width]);
	svg.append("g")
		.attr("transform", "translate(0," + height + ")")
		.call(d3.axisBottom(x).tickValues(x.domain().filter((d, i) => i % ((groups.length>20) ? 2 : 1) === 0)));
	svg.append("text")
		.attr("transform", "translate(" + (width/2) + " ," + (height + 40) + ")")
		.style("text-anchor", "middle")
		.text("Year");

	// Add Y axis
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

	// Color palette. One color per line.
	var color = d3.scaleOrdinal()
		.domain(codes)
		.range(['#009900', '#ff0000', '#ff8000', '#00ff80', '#ffff33', '#0080ff', '#00ff00', '#cc0066', '#00994c'])

	// Draw the line
	svg.selectAll(".line")
		.data(lines)
		.enter()
		.append("path")
			.attr("fill", "none")
			.attr("stroke", function(d){ return color(d.key) })
			.attr("stroke-width", 2.5)
			.attr("d", function(d){
				return d3.line()
				.x(function(d) { return x(d.Year); })
				.y(function(d) { return y(+d.Measurement); })
				(d.values)
		})
	
	//Display Lagend
	var size = 20;
	var legend = svg.append("g")
		.attr("class", "legend")
		.attr("transform", "translate(" + width + "," + 20 + ")")
		.selectAll("g")
		.data(codes)
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

	// Display the Tooltip
	var tipBox = svg.append('rect')
		.attr('width', width)
		.attr('height', height)
		.attr('opacity', 0)
		.on('mousemove', function() {
			var domain = x.domain();
    		var range = x.range();
			var xPos = d3.mouse(tipBox.node())[0] - (x.step()/2);
			var year = domain[d3.bisect(d3.range(range[0], range[1], x.step()), xPos)];
			
			lines.sort((a, b) => {
				return b.values.find(h => h.Year == year).Measurement - a.values.find(h => h.Year == year).Measurement;
			})
			
			tooltipLine.attr('stroke', 'black')
				.attr("stroke-width", 1.5)
				.attr('x1', x(year))
				.attr('x2', x(year))
				.attr('y1', 0)
				.attr('y2', height);

			tooltip.html(year+"'s measurements:")
				.style('display', 'block')
				.style('font-weight', 'bold')
				.style('background-color','#404040')
				.style('left', d3.event.pageX + 60 + "px")
				.style('top', d3.event.pageY - 20 + "px")
				.selectAll()
				.data(lines).enter()
					.append('div')
					.style('color', d => color(d.key))
					.html(d => (Math.round(d.values.find(h => h.Year == year).Measurement * 100) / 100) + "%");
		})
		.on('mouseout', function(){
			if (tooltip) tooltip.style('display', 'none');
			if (tooltipLine) tooltipLine.attr('stroke', 'none');
		});
}