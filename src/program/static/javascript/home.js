$(document).ready(function(){
	
	$(".tablinks").on("click", function(){
		var plot_type_choice = $("[name ='plot']:checked").val()
		var actionName = $(this).attr("name");

		$(".tabcontent").css("display", "none")
		$(".tablinks").removeClass("active");

		if(actionName == "editPlot"){
			if(plot_type_choice == "scatterplot"){
				$("#editScatter").css("display", "block")
				$('#scatterCountry').chosen({});
				$('#scatterIndicator').chosen({max_selected_options: 2});
			}
			else{
				$("#editNonScatter").css("display", "block")
			}
		}
		else{
			$("#"+actionName).css("display", "block")
		}
		$(this).addClass("active")
	});

	// Add Country Selection
	$("#countrySelect").on("change", function(){     
		var selectedCountry = $("#countrySelect :selected").val();
		var countryDiv = $(".is" + selectedCountry);
		countryDiv.slideDown().removeClass("hidden");
		$("#countrySelect :selected").prop("disabled",true);
		$('#countrySelect').val("Add Country");
		$("#is" + selectedCountry).chosen({});
	});

	// Remove Selected Country
	$(".remove-btn").on("click", function(){ 
		var removedCountry = $(this).parent().attr("value");
		var countryDiv = $(".is" + removedCountry);
		$("#countrySelect option[value=" + removedCountry + "]").prop("disabled",false);
		$(this).parent().slideUp(function(){
			$(this).addClass("hidden");
		});
	});

	// Slider and Year Range Indicator
	$("#slider").slider({
		range: true,
		min: 1960,
		max: 2018,
		values: [1979, 1999],
		slide: function(event, ui) {
			$("#yearRange").val(ui.values[0] + " - " + ui.values[1]);
		}
	});
	// Year Range Initialization
	$("#yearRange").val( $("#slider").slider("values",0) + " - " + $("#slider").slider("values", 1) );

	// Grouping Checkbox
	$("#groupingBox").on("change",function(){
		var groupPropDiv = $("#doGroup")

		if ($(this).is(":checked")) {
			groupPropDiv.slideDown().removeClass("hidden");
		}
		else{
			groupPropDiv.slideUp().addClass("hidden");
		}
	});
	$("#groupingBox").prop("checked",false)

	//Submit Button
	$("#submitButton").on("click", function(){
		var plot_type_choice = $("[name ='plot']:checked").val()
		var year_range_choice = $("#slider").slider("values")
		var country_indicator_choice = {}
		var indicators_choice = []
		var do_group_choice = $("#groupingBox").is(":checked")
		var group_period_choice = $("[name = 'yearPeriod']:checked").val()
		var group_aggregation_choice = $("[name = 'aggrType']:checked").val()
		var grouping_prop_choice = {
			group_period: group_period_choice,
			group_aggregation: group_aggregation_choice
		}

		indicators_choice = $("#scatterIndicator").val()
		if (plot_type_choice == "scatterplot" && indicators_choice.length == 2){
			var countries_choice = $("#scatterCountry").val()
			for (var country of countries_choice){
				country_indicator_choice[country] = indicators_choice
			}
		}
		else{
			$(".country-div:not(.hidden)").each(function() {
				indicators_choice = $(this).children(".chosen-select").val();
				if(indicators_choice.length != 0){
					country_indicator_choice[$(this).attr("value")] = indicators_choice
				}
			});
		}
		if (!isEmpty(country_indicator_choice)){
			var data = {
				plot_type: plot_type_choice,
				country_indicator: country_indicator_choice,
				year_range: year_range_choice,
				do_group: do_group_choice,
				grouping_prop: grouping_prop_choice
			};
			$.ajax({
				url: "/getPlotData",
				contentType: "application/json",
				type: "POST",
				dataType : "json",
				data: JSON.stringify(data),
				success: function(response) {
					window.location.href = response["plot_link"];
				},
				error: function(error) {
					console.log(data)
				}
			});
		}
		else{
			plot_type_choice = plot_type_choice.charAt(0).toUpperCase() + plot_type_choice.slice(1)
			if(plot_type_choice == "Scatterplot"){
				alert("Wrong input on " + plot_type_choice + " creation!\n" + 
					  "Make sure you have:\n" + 
					  "  1. Choose at least one country.\n" + 
					  "  2. Choose exactly two indicators.")
			}
			else{
				alert("Wrong input on " + plot_type_choice + " creation!\n" + 
					  "Make sure you have:\n" + 
					  "  1. Choose at least one country.\n" + 
					  "  2. Choose at least one indicator, for a choosen country.")
			}
		}
	});
});

function isEmpty(obj) {
	return Object.keys(obj).length === 0;
}