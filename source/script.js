
let x = 0,y = 0,  dirX = 1,  dirY = 1;
const speed = 4;
let dvd = document.getElementById("dvd");
let stage = document.getElementById("buehne");
let btn = document.querySelector("button")
console.log(document.getElementById("dvd"));
const dvdWidth = dvd.clientWidth;
const dvdHeight = dvd.clientHeight;
const screenHeight = document.body.clientHeight;
const screenWidth = document.body.clientWidth;
var nusic = document.getElementById("myAudio"); 
nusic.loop=true;
stage.style.width = screenWidth
stage.style.height = screenHeight

 
btn.onclick = function(){
    nusic.play();
    window.requestAnimationFrame(animate);
}



function animate() {
    if (y + dvdHeight >= screenHeight || y < 0) {
      dirY *= -1;
    }
    if (x + dvdWidth >= screenWidth || x < 0) {
        dirX *= -1;
    }
    
    x += dirX * speed;
    y += dirY * speed;
    dvd.style.left = x + "px";
    dvd.style.top = y + "px";
    window.requestAnimationFrame(animate);
  }
