$(function() {
  $('.example_a')
    .on('mouseenter', function(e) {
			var parentOffset = $(this).offset(),
      		relX = e.pageX - parentOffset.left,
      		relY = e.pageY - parentOffset.top;
			$(this).find('span').css({top:relY, left:relX})
            //alert(relY, relX)
    })
    .on('mouseout', function(e) {
			var parentOffset = $(this).offset(),
      		relX = e.pageX - parentOffset.left,
      		relY = e.pageY - parentOffset.top;
    	$(this).find('span').css({top:relY, left:relX})
    });
  $('[href="#"]').click(function(){return false});


  $('#delbtn').on("click", function MyFunctionCheckButtonDeleteAccount(){
   var inputNumber = document.getElementById("input_delete_account").value;

   if (isNaN(inputNumber)){
        //alert(inputNumber + " is not a number of an account");
        /*var span4 = document.createElement("SPAN");
        var textalert4 = document.createTextNode(inputNumber + " is not a number");
        var span_add4 = span4.appendChild(textalert4);*/
        document.getElementById("div_empty_number").style.display= 'block';
        //document.getElementById("div_empty_number").style.display = none;
        return false;

        }


   if (inputNumber == ""){
        //alert("there's no number account");
        /*var span5 = document.createElement("SPAN");
        var textalert5 = document.createTextNode("please enter a valid number");
        var span_add5 = span5.appendChild(textalert5);*/
        document.getElementById("div_wrong_number").style.display= 'block';
        return false;

        }


   });

   $("#button_add_client").on("click", function FunctionToCheckAddingClient(){

   var input_add_firstname= document.getElementById("firstname_add_client").value;
   var input_add_lastname = document.getElementById("lastname_add_client").value;
   var input_add_email= document.getElementById("email_add_client").value;
   var input_check_password1 = document.getElementById("pass1").value
   var input_check_password2 = document.getElementById("pass2").value


   if (input_add_firstname=="" || /\s/.test(input_add_firstname)){

       document.getElementById("div_input_firstname").style.display= 'block';
       return false;

    }
   if (input_add_lastname =="" || /\s/.test(input_add_lastname)){

       document.getElementById("div_input_lastname").style.display= 'block';
       return false;


   }
   if (input_add_email=="" || /\s/.test(input_add_email)){

       document.getElementById("div_input_email").style.display= 'block';
       return false;

    }
    if (input_check_password1 != input_check_password2){
        document.getElementById("div_input_pwd2").style.display= 'block';
        return false;
    }

   })
   $("#del_a_client").on("click", function FunctionToCheckDeletingClient(){

   var input_del_firstname= document.getElementById("delete_firstname").value;
   var input_del_lastname = document.getElementById("delete_lastname").value;
   var input_del_email= document.getElementById("delete_email").value;

   if (input_del_firstname =="" || /\s/.test(input_del_firstname)){
       /*var span1 = document.createElement("SPAN");
       var textalert1 = document.createTextNode("please enter a firstname");
       var span_add1= span1.appendChild(textalert1);*/
       document.getElementById("del_firstname").style.display= 'block';
       return false;

    }
   if (input_del_lastname =="" || /\s/.test(input_del_lastname)){
       /*var span2 = document.createElement("SPAN");
       var textalert2 = document.createTextNode("please enter a lastname");
       var span_add2= span2.appendChild(textalert2);*/
       document.getElementById("del_lastname").style.display= 'block';
       return false;


   }
   if (input_del_email =="" || /\s/.test(input_del_email)){
       /*var span3 = document.createElement("SPAN");
       var textalert3 = document.createTextNode("please enter a firstname");
       var span_add3= span3.appendChild(textalert3);*/
       document.getElementById("del_email").style.display= 'block';
       return false;

    }

   })
       $("#button_check_client").on("click", function FunctionToCheckClient(){

   var input_check_email= document.getElementById("email_check_client").value;
   var input_check_password = document.getElementById("password_check_client").value;


   if (input_check_email=="" || /\s/.test(input_check_email)){
       /*var span3 = document.createElement("SPAN");
       var textalert3 = document.createTextNode("please enter a firstname");
       var span_add3= span3.appendChild(textalert3);*/
       document.getElementById("div_input_check_email").style.display= 'block';
       return false;

    }
       if (input_check_password=="" || /\s/.test(input_check_password)){
       /*var span3 = document.createElement("SPAN");
       var textalert3 = document.createTextNode("please enter a firstname");
       var span_add3= span3.appendChild(textalert3);*/
       document.getElementById("div_input_check_pwd").style.display= 'block';
       return false;

    }

    })
    $("#button_check_admin").on("click", function FunctionToCheckAdmin(){


   var input_check_password = document.getElementById("password_check_admin").value;


       if (input_check_password=="" || /\s/.test(input_check_password)){
       /*var span3 = document.createElement("SPAN");
       var textalert3 = document.createTextNode("please enter a firstname");
       var span_add3= span3.appendChild(textalert3);*/
       document.getElementById("div_input_check_pwd_admin").style.display= 'block';
       return false;

    }

    })

    if (window.history.replaceState){
        window.history.replaceState (null, null, window.location.href)
    }

});

/*function myFunction() {
  document.getElementById("myDIV").style.WebkitAnimationDelay = "0s";  // Code for Chrome, Safari, and Opera
  document.getElementById("myDIV").style.animationDelay = "0s";
};*/

