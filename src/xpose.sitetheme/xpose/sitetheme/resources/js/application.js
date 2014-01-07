/*jslint white:false, onevar:true, undef:true, nomen:true, eqeqeq:true, plusplus:true, bitwise:true, regexp:true, newcap:true, immed:true, strict:false, browser:true */
/*global jQuery:false, document:false */

(function ($) {
    'use strict';
    $(document).ready(function () {
        if ($('body').hasClass('lt-ie7')) {return; }

        $('div[data-appui="ajaxcxn"]').each(function () {
            var sourceUrl = $(this).data('appui-uri');
            var targetDiv = $(this).data('appui-target');
            var htmlString = '';
            $.ajax({
                url: sourceUrl,
                timeout: 3000,
                success: function () {
                    htmlString += '<span class="text-danger">Not available</span>';
                    $(targetDiv).html(htmlString);
                }
            });
        });
    });
}(jQuery));