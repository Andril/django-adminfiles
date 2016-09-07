(function($) {
    $(function(){
        $('.adminfilespicker').each(
            function(){
            var href = '/adminfiles/all/?field='+this.id;
            console.log($(this).attr("class"));
            if ($(this).attr("class").indexOf('galleryfield') !== -1){
                href += '&extra=gallery';
            }
            if (this.options) {
                $(this).siblings('a.add-another').remove();
                href += '&field_type=select';
            }
            $(this).after('<iframe frameborder="0" style="border:none; width:755px; height:270px;" src="' + href + '"></iframe>');
        });
    });
})(jQuery);
