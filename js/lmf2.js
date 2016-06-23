var Gcaitime=5;
var Gvname='js';
var Gpcai='01';
var Gscly=0;
var Gshowtype='all';
var shell_sta='9';
var running_sta='9';
$(document).ready(function(){
  $(".scr_div").click(function(){
	  if(running_sta==true){
		  return false;
	  }
	  $(".scr_div").css("background-image","none");
	  $(".item_div").css("display","block");
	  $(".scr_div").scrollTop(Gscly);
	  do_show_cai_class();
	  return false;
  });

  $(".imgzone").click(function(){
	  Gpcai=$(this).parent().attr("bgp");
	  Gscly=$(".scr_div").scrollTop();
	  $(".scr_div").css("background-image","url('"+Gpcai+"')");
	  $(".item_div").css("display","none");
	  return false;
  });

  $(".selzone").click(function(){
	  var obj=this;
	  $.post('setting',{
		  m:'addcai',
		  s:$(this).is('.myselcai'),
		  c:$(this).parent().attr('raw'),
	  },function(r){
		  var rj=JSON.parse(r);		  
		  if(rj.p=='add'){
			  $(obj).addClass("myselcai");
		  }else{
			  $(obj).removeClass("myselcai");
		  }
	  });	  
	  return false;
  });

});
function show_cai_class(showtype,cbtn){
	$(".scr_div").css("background-image","none");
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