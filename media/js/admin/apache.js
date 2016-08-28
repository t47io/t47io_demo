var $ = django.jQuery;


$(document).ready(function() {
    $("[data-toggle='popover']").popover({trigger: "hover"});
    $("[data-toggle='tooltip']").tooltip();
    $("ul.breadcrumb").append('<li class="active"><span style="color: #000;" class="glyphicon glyphicon-grain"></span>&nbsp;&nbsp;Apache Status</li>');
});

