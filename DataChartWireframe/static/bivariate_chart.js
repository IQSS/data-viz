$(document).ready(function(){



	$('#bivariate_warning').hide();
	$().alert();


	

	$('.switch_bivariate').on('click', function(){

		

			$('#bivariate_warning').fadeIn('fast');


			$('#dismiss_bivariate').click(function(){
				$('#bivariate_warning').hide();
			});


			$('#continue_to_bivariate').on('click', function(){


				$('#chart').html('<div id="container"></div>')
				$('#bivariate_warning').hide();
				$('#json_popup').hide();
				$('#sum_stats_preview').empty();
				$('.chart_button').hide();
				$('svg').empty();
				$('.switch').remove();
				$('.chart_options').prepend('<button type="button" class="btn btn-sm btn-default switch_charting" id="btnAddItem"  title="Bivariate Mode"><span class="glyphicon glyphicon-transfer" style="color:#818181;"></span> Return to Charting</button>');
				$('#variable-list').val('');
				$('.variable').css('background-color', 'rgb(240, 248, 270)');
				$('#right_panel_title').html('Drag and Drop Variables To Plot');
				$('#scatter_controls').fadeIn();
				$('#range_area_controls').fadeIn();
				$('#simple_heat_map_controls').fadeIn();
				$('#stacked_percent_controls').fadeIn();
				$('#stacked_count_controls').fadeIn();
				//turn previous events off when click variables
				$('.variable').off();

				$('.variable').css('cursor','-webkit-grab');
				$('.variable').draggable({helper:'clone'});

				$('#rightpanel').css('z-index', 0);

				$('input').droppable({
					drop: function(event, ui){
						var id = ui.draggable.attr('id');
						$(this).val(id);
					}			
				});

				$('#submit_scatter_inputs').click(function(){
					var x_value = $('#x_value_scatter').val();
					var y_value = $("#y_value_scatter").val();
					var z_value = $('#z_value_scatter').val();


					$.getJSON('http://127.0.0.1:5000/bivariate_scatter/',{'x_value':x_value, 'y_value':y_value, 'z_value': z_value}, function(data){

						if(data.x_or_y_missing === true){ //if user didn't specify both x and y
							$('#submit_scatter_inputs').attr('data-content', 'Chart not created. Please insert an appropriate variable name to both the "X" and "Y" fields.');
							$('#submit_scatter_inputs').focus();

						}

						else if(data.repeated_variables === true){
							$('#submit_scatter_inputs').attr('data-content', 'Chart not created. No variable can be used for more than one axis.');
							$('#submit_scatter_inputs').focus();
						}

						else if(data.inputs_valid === false){ // if user submits invalid variable name
							$("#submit_scatter_inputs").attr('data-content','Chart not created. All inputs must be valid variable names.');
							$('#submit_scatter_inputs').focus();
						}

						else if(data.all_data_numeric === false){ // user submits non-numeric va
							$("#submit_scatter_inputs").attr('data-content','Chart not created. All variables must be of numeric type, not character.');
							$('#submit_scatter_inputs').focus();
						}

						else if (data.z_empty === true){
							$('.popover').remove();
							$(function () {

							    $('#container').highcharts({

							        chart: {
							            type: 'bubble',
							            zoomType: 'xy'
							        },

							        title: {
							            text:'<b>' +x_value + '</b> v.s <b>' + y_value+'</b>'
							        },
							        plotOptions : {
							            bubble : {
							                tooltip : {
							                    headerFormat: '<b>{series.name}</b><br>',
							                    pointFormat : x_value+': '+ '{point.x} , '+ y_value+': '+'{point.y}, frequency: {point.z}'
							                    
							                }
							            }
							        },
							        yAxis:{
							            title:{
							                text: y_value}
							        },
							        xAxis:{
							            title:{
							                text: x_value}
							        },

							        series: [data.bivariate_data]
							    });
							});
						}

						else{
							$('.popover').remove();
							$(function () {


								    // Give the points a 3D feel by adding a radial gradient
								    Highcharts.getOptions().colors = $.map(Highcharts.getOptions().colors, function (color) {
								        return {
								            radialGradient: {
								                cx: 0.4,
								                cy: 0.3,
								                r: 0.5
								            },
								            stops: [
								                [0, color],
								                [1, Highcharts.Color(color).brighten(-0.2).get('rgb')]
								            ]
								        };
								    });

								    // Set up the chart
								    var chart = new Highcharts.Chart({
								        chart: {
								            renderTo: 'container',
								            margin: 100,
								            type: 'bubble',
								            options3d: {
								                enabled: true,
								                alpha: 10,
								                beta: 30,
								                depth: 250,
								                viewDistance: 5,

								                frame: {
								                    bottom: { size: 1, color: 'rgba(0,0,0,0.02)' },
								                    back: { size: 1, color: 'rgba(0,0,0,0.04)' },
								                    side: { size: 1, color: 'rgba(0,0,0,0.06)' }
								                }
								            }
								        },
								        title: {
								            text:'<b>' +x_value +'</b> vs <b>' + y_value + '</b> vs <b>' + z_value+'</b>'
								        },
								        subtitle: {
								            text: 'Click and drag the plot area to rotate in space'
								        },
								        plotOptions: {
								            bubble: {

								            	allowPointSelect:true,
								            	maxSize: '15%',
								                width: 10,
								                height: 10,
								                depth: 10
								            }
								        },
								        yAxis: {
								            min: data.min_y_3d,
								            max: data.max_y_3d,
								            title: {text: 'y-Axis: '+y_value}
								        },
								        xAxis: {
								            min: data.min_x_3d,
								            max: data.max_x_3d,
								            title: {text:'x-Axis: '+x_value},
								            gridLineWidth: 1
								        },
								        zAxis: {
								            min: data.min_z_3d,
								            max: data.max_z_3d,
								            title: {text: 'z-Axis: '+z_value},
								            showFirstLabel: false
								        },
								        legend: {
								            enabled: false
								        },

								        series: [data.trivariant_data]
								    });


								    // Add mouse events for rotation
								    $(chart.container).bind('mousedown.hc touchstart.hc', function (e) {
								        e = chart.pointer.normalize(e);

								        var posX = e.pageX,
								            posY = e.pageY,
								            alpha = chart.options.chart.options3d.alpha,
								            beta = chart.options.chart.options3d.beta,
								            newAlpha,
								            newBeta,
								            sensitivity = 5; // lower is more sensitive

								        $(document).bind({
								            'mousemove.hc touchdrag.hc': function (e) {
								                // Run beta
								                newBeta = beta + (posX - e.pageX) / sensitivity;
								                chart.options.chart.options3d.beta = newBeta;

								                // Run alpha
								                newAlpha = alpha + (e.pageY - posY) / sensitivity;
								                chart.options.chart.options3d.alpha = newAlpha;

								                chart.redraw(false);
								            },
								            'mouseup touchend': function () {
								                $(document).unbind('.hc');
								            }
								        });
								    });

								});

						}

					});
				});


				$('#submit_range_area').on('click',function(){
					var x_value = $('#x_value_range_area').val();
					var y_value = $("#y_value_range_area").val();

					$.getJSON('http://127.0.0.1:5000/bivariate_range_area/',{'x_value':x_value, 'y_value':y_value},function(data){

						if(data.x_or_y_missing == true){
							$('#submit_range_area').attr('data-content','Chart not created. Please insert a viariable name to both the "x-Axis" and "y-Axis" fields.');
							$('#submit_range_area').focus();
						}
						else if(data.repeated_variables== true){
							$('#submit_range_area').attr('data-content','Chart not created. No variable may be used for both the "X" and "Y" fields.');
							$('#submit_range_area').focus();

						}
						else if(data.inputs_valid == false){
							$('#submit_range_area').attr('data-content', 'Chart not created. All submitted variable names must be valid.');
							$('#submit_range_area').focus();

						}
						else if(data.y_axis_numeric == false){
							$('#submit_range_area').attr('data-content', 'Chart not created. The variable in the "Y-Axis" field must be numeric, not character');
							$('#submit_range_area').focus();

						}
						else{

							$(function () {
   									$('.popover').remove();
							        $('#container').highcharts({

							            chart: {
							                type: 'arearange',
							                zoomType: 'x'
							            },

							            title: {
							                text: 'Range of <b>'+ y_value+'</b> over <b>' + x_value+'</b>'
							            },

							            xAxis: {
							            	title: {text:x_value}

							            },

							            yAxis: {
							                title: {
							                    text: y_value
							                }
							            },

							            tooltip: {
							            	headerFormat: '<b>' +x_value+': {point.x}</b><br>',
							                crosshairs: true,
							                shared: true

							            },

							            legend: {
							                enabled: false
							            },

							            series: [{
							                name: y_value + ' range: ',
							                data: data.data_range_area
							            }]

							        });


							});
						}


					});


				});
				
				$('#submit_simple_heat_map').on('click',function(){

					var x_value = $('#x_value_simple_heat_map').val();
					var y_value = $('#y_value_simple_heat_map').val();

					$.getJSON('http://127.0.0.1:5000/bivariate_simple_heat_map/',{'x_value':x_value, 'y_value':y_value},function(data){

						if(data.x_or_y_missing == true){
							$('#submit_simple_heat_map').attr('data-content', 'Chart not created. Please specify a variable name for both the "X" and "Y" axises.');
							$('#submit_simple_heat_map').focus();

						}
						else if(data.repeated_variables== true){
							$('#submit_simple_heat_map').attr('data-content', 'Chart not created. No variable may be used for both the "X" and "Y" fields.');
							$('#submit_simple_heat_map').focus();
						}
						else if(data.inputs_valid == false){
							$('#submit_simple_heat_map').attr('data-content','Chart not created. All variable names must be valid variables. ');
							$('#submit_simple_heat_map').focus();
						}
						else if(data.x_too_large == true){
							$('#submit_simple_heat_map').attr('data-content', 'Chart not created. '+ x_value +' has too many unique values. Please choose another variable as your x_axis.');
							$('#submit_simple_heat_map').focus();
						}
						else if(data.y_too_large == true){
							$('#submit_simple_heat_map').attr('data-content','Chart not created. '+y_value +' has too many unique values. Please choose another variable as your y_axis.');	
							$('#submit_simple_heat_map').focus();
						}
						else{

							$(function () {
								$('.popover').remove();
							    $('#container').highcharts({

							        chart: {
							            type: 'heatmap',
							            marginTop: 40,
							            marginBottom: 80
							        },


							        title: {
							            text: 'Heat map: <b>'+y_value+'</b> on <b>'+x_value+'</b>'
							        },

							        xAxis: {
							            categories: data.x_categories,
							            title: {text:x_value}
							        },

							        yAxis: {
							            categories: data.y_categories,
							            title: {text:y_value}
							        },

							        colorAxis: {
							            min: 0,
							            minColor: '#FFFFFF',
							            maxColor: Highcharts.getOptions().colors[0]
							        },

							        legend: {
							            align: 'right',
							            layout: 'vertical',
							            margin: 0,
							            verticalAlign: 'top',
							            y: 25,
							            symbolHeight: 280
							        },

							        tooltip: {
							            formatter: function () {
							                return '<b>' +x_value +'</b> of <b>'+ this.series.xAxis.categories[this.point.x] + '</b> and <br><b>'+y_value + '</b> of ' +'<b>' +this.series.yAxis.categories[this.point.y] +'</b><br> intersect <b>'+ this.point.value+ '</b> times. </b></br>';
							            }
							        },

							        series: [{
							            name: 'Sales per employee',
							            borderWidth: 1,
							            data: data.data_simple_heat_map ,
							            dataLabels: {
							                enabled: true,
							                color: '#000000'
							            }
							        }]

							    });
							});
						}
					});
				})
				$('#submit_stacked_percent_bar').on('click',function(){

					var x_value = $('#x_value_percent_bar').val();
					var y_value = $('#y_value_percent_bar').val();

					$.getJSON('http://127.0.0.1:5000/bivariate_percent_bars',{'x_value':x_value, 'y_value':y_value},function(data){

						if(data.x_or_y_missing == true){
							alert('x or y missing');
						}
						else if(data.repeated_variables == true){
							alert('repeated_variables')
						}
						else if (data.x_too_large == true){
							alert('x too large');
						}
						else if (data.y_too_large == true){
							alert('y too large');
						}
						else{

							$(function () {
						    $('#container').highcharts({
						        chart: {
						            type: 'column'
						        },
						        title: {
						            text: 'Stacked Percentage Bar Chart'
						        },
						        xAxis: {
						            categories: data.x_categories,
						            title:{text:'<b>'+ x_value+'</b>'}
						        },
						        yAxis: {
						            min: 0,
						            title: {
						                text: 'Proportion of <b> '+y_value + '</b> by <b>' + x_value +'</b>'
						            }
						        },
						        tooltip: {
						        	headerFormat:'<b>'+ y_value +'</b> on <b>' +x_value + '</b> of <b>{point.x}</b><br>',
						            pointFormat: '<span style="color:{series.color}">{series.name}: <b>{point.y}</b> ({point.percentage:.0f}%)<br/></span>',
						            shared: true
						        },
						        plotOptions: {
						            column: {
						                stacking: 'percent'
						            }
						        },
						        series: data.series
						    });
							});

						}

					});

				});

				$('#submit_stacked_count_bar').on('click',function(){

					var x_value = $('#x_value_count_bar').val();
					var y_value = $('#y_value_count_bar').val();

					$.getJSON('http://127.0.0.1:5000/bivariate_percent_bars',{'x_value':x_value, 'y_value':y_value},function(data){

						if(data.x_or_y_missing == true){
							alert('x or y missing');
						}
						else if(data.repeated_variables == true){
							alert('repeated_variables')
						}
						else if (data.x_too_large == true){
							alert('x too large');
						}
						else if (data.y_too_large == true){
							alert('y too large');
						}
						else{

							$(function () {
						    $('#container').highcharts({
						        chart: {
						            type: 'column'
						        },
						        title: {
						            text: 'Stacked frequency of <b>' +y_value+ '</b> on <b>'+x_value +'</b>'
						        },
						        xAxis: {
						            categories: data.x_categories,
						            title: {text: '<b>'+x_value +'</b>'}
						        },
						        yAxis: {
						            min: 0,
						            title: {
						                text: 'Frequency of <b>'+ y_value+'</b> on <b>' +x_value + '</b>'
						            },
						            stackLabels: {
						                enabled: true,
						                style: {
						                    fontWeight: 'bold',
						                    color: (Highcharts.theme && Highcharts.theme.textColor) || 'gray'
						                }
						            }
						        },
						        legend: {
						            align: 'right',
						            x: -30,
						            verticalAlign: 'top',
						            y: 25,
						            floating: true,
						            backgroundColor: (Highcharts.theme && Highcharts.theme.background2) || 'white',
						            borderColor: '#CCC',
						            borderWidth: 1,
						            shadow: false
						        },
						        tooltip: {
						            formatter: function () {
						                return '<b>' + this.x + '</b><br/>' +
						                    this.series.name + ': ' + this.y + '<br/>' +
						                    'Total: ' + this.point.stackTotal;
						            }
						        },
						        plotOptions: {
						            column: {
						                stacking: 'normal',
						                dataLabels: {
						                    enabled: true,
						                    color: (Highcharts.theme && Highcharts.theme.dataLabelsColor) || 'white',
						                    style: {
						                        textShadow: '0 0 3px black'
						                    }
						                }
						            }
						        },
						        series: data.series
						    });
							});

						}

					});

				});

					$('#submit_basic_bar').on('click',function(){

					var x_value = $('#x_value_basic_bar').val();
					var y_value = $('#y_value_basic_bar').val();

					$.getJSON('http://127.0.0.1:5000/bivariate_percent_bars',{'x_value':x_value, 'y_value':y_value},function(data){

						if(data.x_or_y_missing == true){
							alert('x or y missing');
						}
						else if(data.repeated_variables == true){
							alert('repeated_variables')
						}
						else if (data.x_too_large == true){
							alert('x too large');
						}
						else if (data.y_too_large == true){
							alert('y too large');
						}
						else{

							$(function () {
						    $('#container').highcharts({
						        chart: {
						            type: 'column'
						        },
						        title: {
						            text: 'Monthly Average Rainfall'
						        },
						        subtitle: {
						            text: 'Source: WorldClimate.com'
						        },
						        xAxis: {
						            categories: data.categories,
						            crosshair: true
						        },
						        yAxis: {
						            min: 0,
						            title: {
						                text: 'Rainfall (mm)'
						            }
						        },
						        tooltip: {
						            headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
						            pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
						                '<td style="padding:0"><b>{point.y:.1f} mm</b></td></tr>',
						            footerFormat: '</table>',
						            shared: true,
						            useHTML: true
						        },
						        plotOptions: {
						            column: {
						                pointPadding: 0.2,
						                borderWidth: 0
						            }
						        },
						        series: data.series
						    });
							});

						}

						});

					});



				


			});

		if (active === false){
			$('#continue_to_bivariate').click();
		}

	});
	

});


	