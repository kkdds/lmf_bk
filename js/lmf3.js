var Gcaitime=5;
var Gvname='js';
var Gpcai='01';
var Gscly=0;
var Gshowtype='all';
var shell_sta='9';
var running_sta='9';
$(document).ready(function(){
    //$(".runscr").css("display","none");

    $('.runModalScr').modal({
        trigger:'.runModalScr',
        olay:'div.overlay',
        modals:'div#modal2',//手动设置时间
        close:'.closeBtn'
    });
	
  $("#setMtimebtn").click(function(){	 
    var cctime=parseInt($('#setMtime').val()); 
	if(isNaN(cctime)){
		return false;
	}
	Gcaitime=cctime;
	sec2minsec();

	$('div.overlay').hide();
	$('div.modal').hide();
	return false;
  });
	
  $(".scr_div").click(function(){
	  if(running_sta==true){
		  return false;
	  }
	  $(".scr_div").css("background-image","none");
	  $(".time-item").css("display","none");
	  $(".item_div").css("display","block");
	  $(".scr_div").scrollTop(Gscly);
	  //$(".menubtn").prop("disabled",false);
	  //$(".menubtn:eq(1)").prop("disabled",true);
	  do_show_cai_class();
	  return false;
  });

  $(".imgzone").click(function(){
	  if(running_sta==true){
		  return false;
	  }
	  Gcaitime=$(this).parent().attr("caitime");
	  sec2minsec();
	  
	  Gvname=$(this).parent().attr("vname");
	  Gpcai=$(this).parent().attr("bgp");
	  Gscly=$(".scr_div").scrollTop();
	  $(".scr_div").css("background-image","url('"+Gpcai+"')");
	  $(".item_div").css("display","none");
	  $(".time-item").css("display","block");
	  
	  return false;
  });
/*
  $(".selzone").click(function(){
	  $(this).toggleClass("myselcai");
	  return false;
  });*/
});
function sec2minsec(){
  intDiff=parseInt(Gcaitime);
  minute = Math.floor(intDiff / 60) ;
  second = Math.floor(intDiff) - (minute * 60);
  if (minute <= 9) minute = '0' + minute;
  if (second <= 9) second = '0' + second;
  $('#minute_show').html('<s></s>'+minute);
  $('#second_show').html('<s></s>'+second);  
}
function timesup(){
	//$('#els_time').text('时间到');
	//$('#btnoff').prop("disabled", true);
	running_sta=false;
	shell_sta=false;
	//alert('done');
	//$.post('sta',{p:$('#pwd').val(),m:'gpiooff',d:'fm'},function(r){
		//var rj=JSON.parse(r);
	//});
}
function doonoff(obj){
	if(running_sta=='0'){
	  //$('#timep').pietimer('start');
	  timer(parseInt(Gcaitime));
	  //$('#btnon').prop("disabled", true);
	  $.post('sta',{p:$('#pwd').val(),m:'gpioon',d:'fm',t:Gcaitime},function(r){
		  //var rj=JSON.parse(r);
		  //$('#btnoff').prop("disabled", false);
	  });
	}else if(running_sta=='1'){
	  //$('#timep').pietimer('pause');
	  //$('#btnoff').prop("disabled", true);
	  $.post('sta',{p:$('#pwd').val(),m:'gpiooff',d:'fm'},function(r){
		  //var rj=JSON.parse(r);
		  //$('#btnon').prop("disabled", false);
	  });
	}
	return false;
}
function getSta(){
	clearInterval(ws);
	$.post('sta',{p:$('#pwd').val(),m:'sta',d:453},function(r){
		var rj=JSON.parse(r);
		shell_sta=rj.shell_sta;
		running_sta=rj.running_sta;
		tempture1=rj.tmp1+40;
		$("#namescreen").text(tempture1.toFixed(1));
		update_sta();
		ws=setInterval("getSta()", 500);
	}).error(function() { 
		disconnect();
	});
}
function update_sta(){
	if(shell_sta=='2'){
		//$('#onoff').prop("disabled",false);
	}
	if(running_sta=='0'){
		//$('.disable_when_running').prop("disabled",false);
		$('#btnon').prop("disabled", false);
		$('#btnoff').prop("disabled", true);
	}
	if(running_sta=='1'){
		//$('.disable_when_running').prop("disabled",true);
		$('#btnoff').prop("disabled", false);
	}  
}
var video_sta=true;
function video_on_off(obj){
	if(video_sta){
	  $.post('video',{p:$('#pwd').val(),m:'play',d:Gvname,i:Gpcai},function(r){
		  //$(obj).val('停止播放');
	  });
	}else{
	  $.post('video',{p:$('#pwd').val(),m:'stop',i:Gpcai},function(r){
		  //$(obj).val('播放视频');
	  });
	}
	video_sta=!video_sta;	
}
function shell_up(){
	  $.post('sta',{p:$('#pwd').val(),m:'shell',d:'up'},function(r){
	  });
}
function shell_dw(){
	  $.post('sta',{p:$('#pwd').val(),m:'shell',d:'dw'},function(r){
	  });
}
var sta_slave=true;
function slave_on_off(obj){
	if(sta_slave){
	  $.post('sta',{p:$('#pwd').val(),m:'gpioon',d:'fs',t:1},function(r){
		  //$(obj).val('保温 开');
	  });
	}else{
	  $.post('sta',{p:$('#pwd').val(),m:'gpiooff',d:'fs'},function(r){
		  //$(obj).val('保温 关');
	  });
	}
	sta_slave=!sta_slave;	
}
var sta_shaokao=true;
function shaokao_on_off(){
	if(sta_shaokao){
	  $.post('sta',{p:$('#pwd').val(),m:'gpioon',d:'sk',t:1},function(r){
		  //$('#btn_sk').val('烧烤 开');
		  $('.disable_when_running').prop("disabled",true);
	  });
	}else{
	  $.post('sta',{p:$('#pwd').val(),m:'gpiooff',d:'sk'},function(r){
		  //$('#btn_sk').val('烧烤 关');
		  $('.disable_when_running').prop("disabled",false);
	  });
	}
	sta_shaokao=!sta_shaokao;	
}
var main_steam=true;
function main_steam_on_off(obj){
	if(main_steam){
	  $.post('sta',{p:$('#pwd').val(),m:'gpioon',d:'ms',t:1},function(r){
		  //$(obj).val('蒸汽 开');
	  });
	}else{
	  $.post('sta',{p:$('#pwd').val(),m:'gpiooff',d:'ms'},function(r){
		  //$(obj).val('蒸汽 关');
	  });
	}
	main_steam=!main_steam;	
}
var liusui_b=true;
function liusui_b_on_off(obj,speed){
	if(!liusui_b){
		speed='0';
	}
	$.post('sta',{p:$('#pwd').val(),m:'pump2',spd:speed},function(r){
		
	});
	liusui_b=!liusui_b;	
}
function liusui_on_off(obj,speed){
	$('#btnqg_big_wat').prop("disabled",false);
	$('#btnqg_sml_wat').prop("disabled",false);
	$('#btnqg_off_wat').prop("disabled",false);
	$.post('sta',{p:$('#pwd').val(),m:'pump2',spd:speed},function(r){
		if(r.b==100){
			$(obj).prop("disabled",true);
		}else if(r.b==50){
			$(obj).prop("disabled",true);
		}else{
			$(obj).prop("disabled",true);
		}
	});
}
function show_cai_class(showtype,cbtn){
	$(".scr_div").css("background-image","none");
	//$(".menubtn").prop("disabled",false);
	//$(cbtn).prop("disabled",true);
	$(".classsel").removeClass("classsel");
	$(cbtn).addClass("classsel");
	$(".scr_div").scrollTop();
	Gshowtype=showtype;
	do_show_cai_class();
}
function do_show_cai_class(){
	showtype=Gshowtype;
	$(".item_div").css("display","none");
	switch (showtype){
	case 'my':
		$(".myselcai").parent().css("display","block");
		$(".top_div").css("visibility","hidden");
		$(".classsel>.opbutton").css("background-color","rgba(51, 51, 51, 0.8)");
	break;
	case 'all':
		$(".item_div").css("display","block");
	break;
	case '10':
		$(".caiclass10").css("display","block");
	break;
	case '20':
		$(".caiclass20").css("display","block");
	break;
	case '30':
		$(".caiclass30").css("display","block");
	break;
	case '40':
		$(".caiclass40").css("display","block");
	break;
	case '50':
		$(".caiclass50").css("display","block");
	break;
	case '60':
		$(".caiclass60").css("display","block");
	break;
	case '70':
		$(".caiclass70").css("display","block");
	break;
	}
}