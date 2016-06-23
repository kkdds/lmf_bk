var ws = null;
$(document).ready(function(){
  $('.connect').click(function() {
	if(ws==null) {
	  connect();
	}else{
	  disconnect();
	}
	update_ui();
	return false;
  });
});
function connect() {
	disconnect();
	$.post('sta',{p:$('#pwd').val(),m:'login',d:'36'},function(r){
		var rj=JSON.parse(r);
		if(rj.p!='error'){
		  ws=setInterval("getSta()", 500);	
		  //log('Connected');
		  update_ui();
		}else{
		  disconnect();
		  $("#log_info").text("密码错误");
		  return false;			  
		}
	});
  }
function disconnect(){
  if(ws!= null){
	clearInterval(ws);
	//log('Disconnected');
	ws = null;
	update_ui();
  }
}
function update_ui(){
  if(ws==null){
	  $(".overlay_init").css("display","block");
	  $("#modal_init").css("display","block");	  
  }else{
	  $(".overlay_init").css("display","none");
	  $("#modal_init").css("display","none");
  }
}
function log(msg){
  //var control = $('#log');
  //control.html(control.html() + msg + '<br/>');
  //control.scrollTop(control.scrollTop() + 1000);
  console.log(msg);
}