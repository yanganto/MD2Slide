var slide = null;
var preview_offset = 1;
var slide_btns = document.querySelectorAll('.slide_btn');
for (var i=0; i < slide_btns.length; i++){
    slide_btns[i].addEventListener('click', function(e){
        slide = window.open('/' + e.target.dataset.slide);
        document.getElementById('title').innerHTML = e.target.dataset.slide.replace('/slide', '');
        preview.src = '/' + e.target.dataset.slide + '#2';
    });
}
document.querySelector('body').addEventListener('keyup', function(e){
    evt = e || window.event;
    var keyCode = evt.keyCode;
    var preview = document.getElementById('preview');
    if (keyCode == 40 || keyCode == 32 ||  keyCode == 34){
        slide.window.location = slide.window.location.pathname + '#' + (parseInt(slide.window.location.hash.replace('#', '')) + 1);
        preview.src = slide.window.location.pathname + '#' + (parseInt(slide.window.location.hash.replace('#', '')) + preview_offset);
    }

    if (keyCode == 38 || keyCode == 33){
        slide.window.location = slide.window.location.pathname + '#' + (parseInt(slide.window.location.hash.replace('#', '')) - 1);
        preview.src = slide.window.location.pathname + '#' + (parseInt(slide.window.location.hash.replace('#', '')) + preview_offset);
    }
    if (keyCode == 27){
        slide.window.location = slide.window.location.pathname;
        preview.src = slide.window.location.pathname + '#' + (parseInt(slide.window.location.hash.replace('#', '')) + preview_offset);
    }
    console.log(keyCode);
});