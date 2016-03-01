  $(function (){
    $(window).on("load resize",function(){
      $(".fill-screen").css("height",window.innerHeight);
    });

  //scroll suave
   $('nav a, .down-button a').bind('click', function () {
        $('html, body').stop().animate({
            scrollTop: $($(this).attr('href')).offset().top - 100
        }, 1500, 'easeInOutExpo');
        event.preventDefault();
    });
 
 });