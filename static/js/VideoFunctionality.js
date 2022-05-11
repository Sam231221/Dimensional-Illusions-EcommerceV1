var video=document.querySelectorAll('video')
video.forEach(play=>play.addEventListener('click',()=>{
      play.classList.toggle('active');

      if (play.paused){
          play.play();

      }
      else{
          play.pause();
          play.currentTime=0;
      }
  }))

$(document).ready(function(){
    $(".videocontroller").hover(function(){
        $(this).children("video")[0].play();
    },
    function(){
    $(this).children("video")[0].pause();
    });
});
