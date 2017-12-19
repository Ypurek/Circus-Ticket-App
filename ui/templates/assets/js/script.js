function minH() {
	var minHeight = jQuery('body').height() - jQuery('.header').height() - jQuery('.footer').height();
	jQuery('.minH').css('min-height',minHeight);
}


jQuery(document).ready(function( $ ) {
	
	$('.menuButton a').on('click', function(event) {
        event.preventDefault();
        $('.header').toggleClass('open');
        $('.header .menuBox').stop().slideToggle();
	});
	
	$('.dateInput').datepicker();
	
	var timeSlider = $("#timeSlider").bootstrapSlider({
		min: 420,
		max: 1380,
		step: 15,
		value: [ 720, 1200 ],
		range: true,
		tooltip: 'hide'
	});
	
	if (timeSlider) {
		timeSlider.on('change',function(){
			var value = timeSlider.bootstrapSlider('getValue');
			
			var hours1 = Math.floor(value[0] / 60);
			var minutes1 = value[0] - (hours1 * 60);
			if (hours1.length == 1) hours1 = '0' + hours1;
	        if (minutes1.length == 1) minutes1 = '0' + minutes1;
	        if (minutes1 == 0) minutes1 = '00';
	        
	        hours1 = hours1;
	        minutes1 = minutes1;
	        
	        if (hours1 == 0){
	            minutes1 = minutes1;
	        }

	        $('.time1').val(hours1+':'+minutes1);

	        var hours2 = Math.floor(value[1] / 60);
	        var minutes2 = value[1] - (hours2 * 60);

	        if(hours2.length == 1) hours2 = '0' + hours2;
	        if(minutes2.length == 1) minutes2 = '0' + minutes2;
	        if(minutes2 == 0) minutes2 = '00';
	        hours2 = hours2;
	        minutes2 = minutes2;

	        $('.time2').val(hours2+':'+minutes2);
			
		});
	}
	
	var priceSlider = $("#priceSlider").bootstrapSlider({
		min: 0,
		max: 2000,
		step: 50,
		value: [ 0, 1000 ],
		range: true,
		tooltip: 'hide'
	});
	
	if (priceSlider) {
		priceSlider.on('change',function(){
			var value = priceSlider.bootstrapSlider('getValue');
			
			var price1 = value[0];
	        $('.price1').val(price1);

	        var price2 = value[1];
	        $('.price2').val(price2);
			
		});
	}
	
	$('.showDes').on('click',function(){
		var showDes = '.' + $(this).attr('id');
		if($(this).hasClass('vis')) {
			$(this).removeClass('vis');
			$(showDes).stop(true, true).slideUp('slow');
		} else {
			$(this).addClass('vis');
			$(showDes).stop(true, true).slideDown('slow');
		}
	})
	
	minH();
	
	$('.itemsAmountPlus').on('click',function(){
		var quantity = $(this).parent().children('input').val();
		if (quantity == '') { 
			quantity = 1 
		} else { 
			if (quantity < 99) { 
				quantity = parseInt(quantity) + 1 
			}
		};
		$(this).parent().children('input').val(quantity);
	})
	
	$('.itemsAmountMinus').on('click',function(){
		var quantity = parseInt($(this).parent().children('input').val());
		if (quantity > 0) quantity = quantity - 1;
		$(this).parent().children('input').val(quantity);
	})
	
	$('.quantity input').keydown(function(e) {
		if (e.key.length == 1 && e.key.match(/[^0-9'".]/)){
		    return false;
		};
	});
	
	$('.cardInput input').mask("9999 9999 9999 9999");

	if ($('.loginform')){
		$('body').addClass('home');
	}
	
});



window.onscroll = function() {
	 
}

jQuery(window).resize(function () {
	minH();
});

jQuery(window).bind("orientationchange",function(e){
	minH();
	//location.reload();
})
 