$(function () {
    $('[data-toggle="tooltip"]').tooltip();

    $(".form-control-outline").each(function () {
        if ($(this).val().trim().length > 0) {
            $(this).next('label').addClass('has-input');
        }
    });

    try {
        $('#my-dt').DataTable({
            responsive: true,
        });
    } catch { }

    try {

    } catch { }

    $('#my-simple-dt').DataTable({
        'responsive': true,
        "paging": false,
        "ordering": false,
        "info": false,
        'searching': false,
    });

    $(".rippler").ripple({
        effectClass: 'rippler-effect',
        effectSize: 16, // Default size (width & height)
        addElement: 'div', // e.g. 'svg'(feature)
        duration: 200
    });

    $('.custom-file-input').on('change', function () {
        //get the file name
        var fileName = $(this).val();
        //replace the "Choose a file" label
        $(this).next('.custom-file-label').html(fileName);
    });

    $('.product-image-thumb').on('click', function () {
        const image_element = $(this).find('img');
        $('.product-image').prop('src', $(image_element).attr('src'))
        $('.product-image-thumb.active').removeClass('active');
        $(this).addClass('active');
    });

    $('.quantity-right-plus').click(function (e) {
        e.preventDefault();
        // Get the field name
        var quantity = parseInt($('#quantity').val() || 1) || 1;
        // If is not undefined
        $('#quantity').val(quantity + 1);
        // Increment
    });

    $('.quantity-left-minus').click(function (e) {
        e.preventDefault();
        // Get the field name
        var quantity = parseInt($('#quantity').val() || 1) || 1;
        // Increment
        if (quantity > 1) {
            $('#quantity').val(quantity - 1);
        }
    });

});

$(document).on('change keyup keydown focus', '.form-control-outline', function () {
    if ($(this).val().trim().length > 0) {
        $(this).next('label').addClass('has-input');
    } else {
        $(this).next('label').removeClass('has-input');
    }
});

// init Lazy Load Images
document.addEventListener("DOMContentLoaded", function () {
    $(window).on('load', function () {
        yall({
            observeChanges: true
        });
    });
});

$(document).on('click', '#dark-light-switch', function (event) {
    event.preventDefault();
    $(this).tooltip('hide');
    let theme = $('body').attr('data-mode') ?? 'light';
    $(this).attr('data-original-title', `Turn on ${theme} mode`);
    if (theme == 'dark') {
        // theme = 'light';
        $('body').attr('data-mode', theme = 'light');
        $(this).children('i').removeClass('fa-sun').addClass('fa-moon');
    } else {
        // theme = 'dark';
        $('body').attr('data-mode', theme = 'dark');
        $(this).children('i').removeClass('fa-moon').addClass('fa-sun');
    }
    // $(this).attr('data-original-title', `Turn on ${theme} mode`);
    Cookies.set("theme", theme, { expires: 365 });
});

$(document).on("click", ".btn-copy", function () {
    /* Get the text field */
    var copyText = document.getElementById($(this).data('target'));

    /* Select the text field */
    copyText.select();
    copyText.setSelectionRange(0, 99999); /*For mobile devices*/

    /* Copy the text inside the text field */
    document.execCommand("copy");

    $(this).attr('title', 'Copied!');
    $(this).tooltip('dispose');
    $(this).tooltip('show');
    ResetTooltip(this, 'Click to Copy');
});

function ResetTooltip(element, newTitle) {
    setTimeout(function () {
        $(element).attr('title', newTitle);
        $(element).tooltip('dispose');
        $(element).tooltip();
    }, 3000);
}