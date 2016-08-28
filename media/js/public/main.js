var throttle = function(func, delay, at_least) {
  var timer = null, previous = null;
  return function() {
    var now = +new Date();
    if (!previous) { previous = now; }
    if (now - previous > at_least) {
      func();
      previous = now;
    } else {
      clearTimeout(timer);
      timer = setTimeout(func, delay);
    }
  };
};

app.fnChangeView = function() {
  var path = window.location.pathname;
  if (path.indexOf('/signin') != -1) {
    if ($("#id_flag").val() == 'Admin') {
      $("#form_header").html("This site is for internal administration.");
    } else {
      $("#form_header").html("This site is for Lab Demo. Login with <code style='color:#ffc107; background-color:#fcf8e3;'>demo</code>:<code>demo</code>");
    }

    $("#sys-modal > .modal-dialog > .modal-content > .modal-header > .modal-title").html('<span class="glyphicon glyphicon-camera" aria-hidden="true"></span>&nbsp;&nbsp;Lab Demo');
    $("#sys-head").html("Demo Variations").addClass("label-violet").removeClass("label-success");
    $('<ul id="sys-ul" style="text-align:left;"><li><b>Mock-up</b> <i><u>charts, tables and data entries</u></i> are used for demonstration.</li><li><i><u>Data links and external URLs</u></i> are <b>disabled</b>.</li><li><i><u>Slack messages, file uploads, and emails</u></i> are <b>disabled</b>.</li><li><i><u>External site</u></i> is <b>excluded</b>. Production server is held at <a href="https://daslab.stanford.edu" target="_blank">DasLab Website&nbsp;&nbsp;<span class="glyphicon glyphicon-new-window" aria-hidden="true"></span></a>.</li><br/><li><i><u>Static files and database</u></i> are restored to <b>default</b> every 30 min.</li><br/></ul>').insertAfter("#sys-msg");
    $("#demo_msg").on("click", function() { $("#sys-modal").modal("show"); });
  } else if (path.indexOf('/password') != -1) {
    $("#form_pw").on("submit", function(e) {
      e.preventDefault();
      $("#sys-head").html("Change Password");
      $("#sys-msg").html("This will verify and update your password (not included for this demo).");
      $("#sys-modal").modal("show");
      setTimeout(function() { $("#sys-modal").modal("hide"); }, 1000);
    });
  }

  $("body").fadeTo(100, 1);
  if (window.location.hash) { $('html, body').stop().animate({"scrollTop": $(window.location.hash).offset().top - 75}, 500); }
  if (typeof app.callbackChangeView === "function") { app.callbackChangeView(); }
};

$(document).ready(function() {
  app.fnChangeView();

  var today = new Date();
  $("#cp_year").text(today.getFullYear());

  if (window.innerWidth <= 768) {
    var obj = document.getElementById('center');
    obj.style.height = 'auto';
  }
});


$(window).on("scroll", throttle(function() {
  if ($(this).scrollTop() > $(window).height() / 2) {
    $('#top > div').animate({'right': '5%', 'opacity': 0.85}, 125);
  } else {
    $('#top > div').animate({'right': '-5%', 'opacity': 0}, 125);
  }
}, 200, 500));

window.onpopstate = function() { location.reload(); };
