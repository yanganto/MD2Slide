var slide = null;
var note = null;
var preview_offset = 1;
var slide_btns = document.querySelectorAll('.slide_btn');

function show_notes(){
    for (var i=0; i < slide_btns.length; i++)
        slide_btns[i].style.display = 'none';
    document.getElementById('note').style.display = 'inline';
}
function hide_notes(){
    for (var i=0; i < slide_btns.length; i++)
        slide_btns[i].style.display = 'inline';
    document.getElementById('note').style.display = 'none';
}

for (var i=0; i < slide_btns.length; i++){
    slide_btns[i].addEventListener('click', function(e){
        slide = window.open('/' + e.target.dataset.slide, e.target.dataset.slide, 'scrollbars=yes, width=800, height=600, top=0, left=0');
        document.getElementById('title').innerHTML = e.target.dataset.slide.replace('/slide', '');
        preview.src = '/' + e.target.dataset.slide + '#2';
        var oReq = new XMLHttpRequest();
        oReq.addEventListener("load", function(){
            notes = JSON.parse(oReq.responseText);
            document.getElementById('note').innerHTML = notes['#1'].note;
        }, false);
        oReq.open("GET", '/' + e.target.dataset.slide.replace('/slide', '/note'), true);
        oReq.send()
        show_notes();
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
            document.getElementById('note').innerHTML = notes[slide.window.location.hash].note;
        }else{
            var uris = preview.src.split('#')
            preview.src = uris[0] + '#' + (parseInt(uris[1]) + 1);
        }
    }

    if (keyCode == 38 || keyCode == 33){
        if(slide){
            slide.window.location = slide.window.location.pathname + '#' + (parseInt(slide.window.location.hash.replace('#', '')) - 1);
            preview.src = slide.window.location.pathname + '#' + (parseInt(slide.window.location.hash.replace('#', '')) + preview_offset);
            document.getElementById('note').innerHTML = notes[slide.window.location.hash].note;
        }else{
            var uris = preview.src.split('#')
            preview.src = uris[0] + '#' + (parseInt(uris[1]) - 1);
        }
    }
    if (keyCode == 27){
        if(slide){
            slide.window.close();
        }
        preview.src = '/help#1';
        hide_notes();
        document.getElementById('title').innerHTML = 'Slide List';
    }
});
function controlState(status){
    if (status){
        document.bgColor = 'white';
        document.body.style.backgroundColor = 'white';
        document.getElementById('info').style.display = 'none';
    }else{
        document.bgColor = '#222';
        document.body.style.backgroundColor = '#777';
        document.getElementById('info').style.display = 'inline';
    }
}
document.getElementById('info').style.display = 'none';
