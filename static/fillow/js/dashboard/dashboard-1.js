(function($) {
	// 이메일 분류 현황 함수
	var emailchart = function(){
		// 받은 새로운 이메일이 없으면 표시 안함
		if (total === 0) {
			return;
		}

		var labels = data['labels'];
		var count = data['count'];

		var options = {
			series: count,
			chart: {
				type: 'pie',
				height:230,
				chart: {
					fontFamily: 'Noto Sans KR, sans-serif',
					fontSize: '14px',
				},
				events: {
					click: function(event, chartContext, {dataPointIndex}) {
						// Redirect to a specific URL when any bar is clicked
						window.location.href = '/email-inbox/';
					}}
			},
			labels: labels,
			dataLabels:{
				enabled: false
			},
			stroke: {
				width: 0,
			},
			colors:color = [
				"#fc2e53",
				"#ffbf00",
				"#09bd3c",
				"#128a7e",
				"#369fc2",
				"#ffa7d7",
				"#6238fc",
				"#d653c1",
				"#c8c8c8",
			],
			legend: {
				position: 'bottom',
				show: false
			},
			responsive: [{
				breakpoint: 1800,
				options: {
					chart: {
						height:200
					},
				}
			}]
		};

		var chart = new ApexCharts(document.querySelector("#emailchart"), options);
		chart.render();
	};

	var barChart1 = function(){
		if( tasks_sum > 0 ){
			var options = {
				chart: {
					type: 'bar',
					height:230,
					fontFamily: 'Noto Sans KR, sans-serif',
					fontSize: '14px',
					events: {
						click: function(event, chartContext, {dataPointIndex}) {
							// Redirect to a specific URL when any bar is clicked
							window.location.href = '/schedule/';
						}
					},
					toolbar: {
						show: false // 이미지 저장 메뉴를 숨깁니다.
					},
				},
				series: [{
					name : "할 일 개수",
					data: Object.values(tasks)
					}],
				plotOptions: {
					bar: {
						horizontal: false,
						columnWidth: '55%',
					},
				},
				xaxis: {
					categories: Object.keys(tasks),
				},
				yaxis: {
					labels: {
						formatter: function (value) {
							return parseInt(value); // Formats the y-axis labels to integers
						}
					}
				},
				colors: ['#008FFB', '#00E396', '#FEB019', '#FF4560', '#775DD0', '#546E7A', '#26a69a', '#D10CE8']
			};

			var chart = new ApexCharts(document.querySelector("#barChart_1"), options);
			chart.render();
		};
	}
	
 	var dlabChartlist = function(){
	/* Function ============ */
		return {
			init:function(){
			},
			
			
			load:function(){
				emailchart();
				barChart1();
			},
			
			resize:function(){
			}
		}
	
	}();

	jQuery(window).on('load',function(){
		setTimeout(function(){
			dlabChartlist.load();
		}, 1000); 
		
	});
})(jQuery);