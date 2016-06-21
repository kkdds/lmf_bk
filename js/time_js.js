/*
 Copyright (c) 2012, Northfield X Ltd
 https://github.com/knorthfield/pietimer/
*/
(function(d){var k={seconds:10,color:"#F1C40F",height:100,width:100},e=3*Math.PI/2,g=Math.PI/180,f=function(b,a,c){null===a.width&&(a.width=b.width());null===a.height&&(a.height=b.height());this.settings=a;this.jquery_object=b;this.interval_id=null;this.current_value=360;this.initial_time=new Date;this.accrued_time=0;this.callback=c;this.is_paused=!0;this.is_reversed="undefined"!=typeof a.is_reversed?a.is_reversed:!1;this.jquery_object.html('<canvas class="pie_timer" width="'+a.width+
'" height="'+a.height+'"></canvas><div class="pie_timer_div"><div style="height:30px"></div><span id="els_time">'+this.settings.seconds+' s</span></div>');this.canvas=this.jquery_object.children(".pie_timer")[0]};f.prototype={start:function(){this.is_paused&&(this.initial_time=new Date-this.accrued_time,0>=this.current_value&&(this.current_value=360),this.interval_id=setInterval(d.proxy(this.run_timer,this),1000),this.is_paused=!1)},pause:function(){this.is_paused||(this.accrued_time=new Date-this.initial_time,clearInterval(this.interval_id),this.is_paused=!0)},run_timer:function(){if(this.canvas.getContext)if(this.elapsed_time=
(new Date-this.initial_time)/1E3,this.current_value=360*Math.max(0,this.settings.seconds-this.elapsed_time)/this.settings.seconds,0>=this.current_value)clearInterval(this.interval_id),this.canvas.width=this.settings.width,d.isFunction(this.callback)&&this.callback.call(),this.is_paused=!0;else{this.canvas.width=this.settings.width;var b=this.canvas.getContext("2d"),a=[this.canvas.width,this.canvas.height],c=Math.min(a[0],a[1])/2,a=[a[0]/2,a[1]/2],h=this.is_reversed;b.beginPath();b.moveTo(a[0],a[1]);
b.arc(a[0],a[1],c,h?e-(360-this.current_value)*g:e-this.current_value*g,e,h);b.closePath();
b.fillStyle=this.settings.color;b.fill();
$('#els_time').text(parseInt(this.settings.seconds-this.elapsed_time+1)+' s');
}}};var l=function(b,a){var c=d.extend({},k,b);return this.each(function(){var b=d(this),e=new f(b,c,a);b.data("pie_timer",e)})},m=function(b){b in f.prototype||d.error("Method "+b+" does not exist on jQuery.pietimer");var a=Array.prototype.slice.call(arguments,1);return this.each(function(){var c=d(this).data("pie_timer");if(!c)return!0;c[b].apply(c,a)})};d.fn.pietimer=
function(b){return"object"===typeof b||!b?l.apply(this,arguments):m.apply(this,arguments)}})(jQuery);

/* 方法 样式 2 */
var intDiff = 60;//倒计时总秒数量
function timer(intDiff){
	var objTimer = window.setInterval(function(){
	var day=0,
		hour=0,
		minute=0,
		second=0;//时间默认值		
	if(intDiff > 0){
		minute = Math.floor(intDiff / 60);
		second = Math.floor(intDiff) - (minute * 60);
	}else{
		timesup();
		window.clearInterval(objTimer);
	}
	if (minute <= 9) minute = '0' + minute;
	if (second <= 9) second = '0' + second;
	$('#minute_show').html('<s></s>'+minute);
	$('#second_show').html('<s></s>'+second);
	intDiff--;
	}, 1000);
} 