var slide = null;
var preview_offset = 1;
var slide_btns = document.querySelectorAll('.slide_btn');
for (var i=0; i < slide_btns.length; i++){
    slide_btns[i].addEventListener('click', function(e){
        //slide = window.open('/' + e.target.dataset.slide);
        slide = window.open('/' + e.target.dataset.slide, e.target.dataset.slide, 'scrollbars=yes, width=800, height=600, top=0, left=0');
        document.getElementById('title').innerHTML = e.target.dataset.slide.replace('/slide', '');
        preview.src = '/' + e.target.dataset.slide + '#2';
    });
}
document.querySelector('body').addEventListener('keyup', function(e){
    evt = e || window.event;
    var keyCode = evt.keyCode;
    var preview = document.getElementById('preview');
    if (keyCode == 40 || keyCode == 32 ||  keyCode == 34){
        if(slide){
            slide.window.location = slide.window.location.pathname + '#' + (parseInt(slide.window.location.hash.replace('#', '')) + 1);
            preview.src = slide.window.location.pathname + '#' + (parseInt(slide.window.location.hash.replace('#', '')) + preview_offset);
        }else{
            var uris = preview.src.split('#')
            preview.src = uris[0] + '#' + (parseInt(uris[1]) + 1);
        }
    }

    if (keyCode == 38 || keyCode == 33){
        if(slide){
            slide.window.location = slide.window.location.pathname + '#' + (parseInt(slide.window.location.hash.replace('#', '')) - 1);
            preview.src = slide.window.location.pathname + '#' + (parseInt(slide.window.location.hash.replace('#', '')) + preview_offset);
        }else{
            var uris = preview.src.split('#')
            preview.src = uris[0] + '#' + (parseInt(uris[1]) - 1);
        }
    }
    if (keyCode == 27){
        if(slide){
            slide.window.location = slide.window.location.pathname;
            preview.src = slide.window.location.pathname + '#' + (parseInt(slide.window.location.hash.replace('#', '')) + preview_offset);
        }else{
            var uris = preview.src.split('#')
            preview.src = uris[0] + '#1';
        }
    }
});