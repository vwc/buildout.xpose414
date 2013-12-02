/*jslint white:false, onevar:true, undef:true, nomen:true, eqeqeq:true, plusplus:true, bitwise:true, regexp:true, newcap:true, immed:true, strict:false, browser:true */
/*global jQuery:false, document:false */
'use strict';

(function ($) {
    $(document).ready(function () {
        if ($('body').hasClass('lt-ie7')) {return; }

        $('div[data-appui="ajaxcxn"]').each(function () {
            var sourceUrl = $(this).data('appui-uri');
            var targetDiv = $(this).data('appui-target');
            $.getJSON(sourceUrl, function (data) {
                $(targetDiv).empty();
                var htmlString = '';
                $.each(data.items, function (i, item) {
                    //alert('This item:' + item.title);
                    htmlString += '<div class="row"><div class="col col-lg-4">';
                    htmlString += '<img src="' + item.img + '" /></div>';
                    htmlString += '<div class="col col-lg-8"><h5><a href="' + item.url + '">' + item.title + '</a></h5>';
                    htmlString += '<p class="discreet">' + item.zip + ' ' + item.city + '</p>';
                    htmlString += '</div></div>';
                    htmlString += '<div class="visualClear">&nbsp;</div>';
                });
                $('#json-venues').html(htmlString);
            });
        });

    }
    );
}(jQuery));