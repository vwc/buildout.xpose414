/*jslint white:false, onevar:true, undef:true, nomen:true, eqeqeq:true, plusplus:true, bitwise:true, regexp:true, newcap:true, immed:true, strict:false, browser:true */
/*global jQuery:false, document:false */

(function ($) {
    'use strict';
    $(document).ready(function () {
        if ($('body').hasClass('lt-ie7')) {return; }
        $('div[data-appui="bummer"]').on({
            mouseenter: function () {
                $(this).find('.contentpanel-editbar').removeClass('fadeOutUp').addClass('fadeInLeft').show();
            },
            mouseleave: function () {
                $(this).find('.contentpanel-editbar').removeClass('fadeInLeft').addClass('fadeOutUp');
            }
        });
        // Test if CSS transitions are supported
        if (!Modernizr.csstransitions) {
            $(function () {
                $('.dim-in').on('load', function () {
                    $(this).animate({opacity: '1'}, {queue: false, duration: 500});
                });
            });
        }
    });
}(jQuery));