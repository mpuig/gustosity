
/*================================================================*/
/*  TRIGGER EQUAL COLUMNS AT 767 px
/*================================================================*/
$(window).load(function(){
if (document.documentElement.clientWidth > 767) { //if client width is greater than 767px load equal columns

(function($) {

    $.fn.eqHeights = function() {

        var el = $(this);
        if (el.length > 0 && !el.data('eqHeights')) {
            $(window).bind('resize.eqHeights', function() {
                el.eqHeights();
            });
            el.data('eqHeights', true);
        }
        return el.each(function() {
            var curHighest = 0;
            $(this).children().each(function() {
                var el = $(this),
                    elHeight = el.height('auto').height();
                if (elHeight > curHighest) {
                    curHighest = elHeight;
                }
            }).height(curHighest);
        });
    };

    $('#equalHeights,#equalHeightsA,#equalHeightsB,#equalHeightsC,#equalHeightsD').eqHeights(); /*one time per page unless you make another id to add here */

}(jQuery));
} // end if
}); // end windowload


/*================================================================*/
/*  FADE ALL EXCEPT HOVERED
/*================================================================*/
$(document).ready(function() {
$('.image-widget li').hover(function(){
    $(this).siblings().addClass('fade');
    }, function(){
    $(this).siblings().removeClass('fade');
    });
});



/*================================================================*/
/*  MOBILE NAV TRIGGER
/*================================================================*/
$(document).ready(function(){

$('.mobile_nav a').click(function(){
    $('#main_menu').slideToggle(400);
    $(this).toggleClass('active'); return false;
});

/*================================================================*/
/*  ADD CLASSES TO VARIOUS THINGS TO FIX IE
/*================================================================*/
$(".sort li:first-child").addClass('first');
$(".sort li:last-child, .footerPosts li:last-child, .footerCredits ul li:last-child").addClass('last');

$(".features li:nth-child(odd)").addClass('odd');
$(".features li:nth-child(even)").addClass('even');

});


/*================================================================*/
/*  BACK TO TOP
/*================================================================*/

$(document).ready(function(){

    // hide .backToTop first
    $(".backToTop").hide();

    // fade in .gototop
    $(function () {
        $(window).scroll(function () {
            if ($(this).scrollTop() > 100) {
                $('.backToTop').fadeIn();
            } else {
                $('.backToTop').fadeOut();
            }
        });

        // scroll body to 0px on click
        $('.backToTop a').click(function () {
            $('body,html').animate({
                scrollTop: 0
            }, 800);
            return false;
        });
    });

});


/*================================================================*/
/*  SEARCH
/*================================================================*/
/*
$(document).ready(function(){

    //$('.search input').hide();

$('.search #search-trigger').click(function(){

    $(".search input").slideToggle('fast').focus();
       //$(".preheader .user").hide('fast');
        $(this).toggleClass('active');
      });

    $('.search input').blur(function(){
      $(this).hide('fast');
      $("#search-trigger").removeClass('active');
     //$('.preheader .user').show('fast');
    });

});
*/

/*================================================================*/
/*  FORGOT PASSWORD (on login page)
/*================================================================*/

$(document).ready(function(){

    $('.forgot-password').hide();

$('.forgotpw, .forgot-password .closeforgot').click(function(){

    $(".forgot-password").slideToggle('fast').focus();
      });




});



/*================================================================*/
/*  SIMPLE ACCORDION
/*================================================================*/

$(document).ready(function(){

//  var allPanels = $('.s-accordion li.s-wrap div.s-content').hide();

//  $('.s-accordion li.s-wrap .trigger a').click(function() {
//   $(this).addClass('active')
//    allPanels.slideUp();
//     if($(this).parent().next().is(':hidden'))
//      {
//     $(this).parent().next().slideDown();
//      }
//   return false;
//  });

       $('.s-accordion li.s-wrap div.s-content').hide();
       $('.s-accordion li.s-wrap .trigger a').click(function(){
          if ($(this).hasClass('active')) {
               $(this).removeClass('active');
               $(this).parent().next().slideUp();
          } else {
               $('.s-accordion li.s-wrap .trigger a').removeClass('active');
               $(this).addClass('active');
               $('.s-accordion li.s-wrap div.s-content').slideUp();
               $(this).parent().next().slideDown();
          }
          return false;
       });

});




/*================================================================*/
/*  TOOL TIPS and POP OVERS
/*================================================================*/

  $(function(){

    $('.titletip, ul.social li a').tooltip({});
    $(".detailsPop").popover({trigger: 'hover'});
});

/*================================================================*/
/*  SMOOTH SCROLL to ANCHOR (DIV WITH ID)
/*================================================================*/

$(document).ready(function($) {

    $(".scrollto, .container.visible-phone.hidden-tablet.hidden-desktop .btn").click(function(event){
        event.preventDefault();
        $('html,body').animate({scrollTop:$(this.hash).offset().top}, 800);return false;
    });
});


/*================================================================*/
/*  ADD ACTIVE CLASS TO MENU - DEMO only you can remove this if you want, your CMS should be set up so that the active class is added via php
/*================================================================*/
$(document).ready(function(){
   var path = location.pathname.substring(1);
   if ( path )
    //  $('#main_menu li a[href$="' + path + '"]').parents('li').addClass('active');
        $('#main_menu li a[href$="' + path + '"]').parents('li').last().addClass('active');
        $('#main_menu li a[href$="' + path + '"]').parents('li').first().addClass('active');
        $('#main_menu li a[href$="' + path + '"]').parent('li').addClass('active');
 });

 $(document).ready(function(){
   var path = location.pathname.substring(1);
   if ( path )
          $('ul.navigation li a[href$="' + path + '"]').parents('li').addClass('active');
 });
