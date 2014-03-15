function navigate(link) {
     //$("#application").remove();
     $(".span16").innerHTML="";
     $(".span16").prepend(animationBar());
     $(".span16").load(link);
      window.history.pushState({}, "", link);
}

function animationBar() {
    return '<div class="progress progress-striped active"><div class="progress-bar" style="width: 100%"></div></div>'
}
