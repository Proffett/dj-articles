//   window.addEventListener('load', initialize, false);

// function initialize() {
//   document.getElementsByClassName('article_img_list')[0].addEventListener('mouseover', function (e) {
//     var left = window.getComputedStyle(e.target).getPropertyValue('left');

//     left = parseInt(left, 10);
//     moveImg(left, 100);

//   }, false);
// }

// function moveImg(left, numMoves) {
//   document.getElementsByClassName('article_img_list')[0].style.left = left + 'px';

//   if (numMoves > 0) {
//     numMoves--;
//     left++;
//     setTimeout(moveImg,10,left,numMoves);
//   }
//   else {
//     return;
//   }
// }

// let gps = navigator.geolocation.getCurrentPosition(
//   function (position) {
//     for (key in position.coords) {
//       document.write(key+': '+ position.coords[key]);
//       document.write('<br>');
//     }
//   }
// )

// console.log('pizdec', '1+5');


// window.addEventListener('DOMContentLoaded', function() {
//   var v = document.getElementById('v');
//   navigator.getUserMedia = (navigator.getUserMedia ||
//     navigator.webkitGetUserMedia ||
//     navigator.mediaDevices.getUserMedia ||
//     navigator.msGetUserMedia);
//   if (navigator.getUserMedia) {
//     navigator.getUserMedia (
//       {
//         video: true,
//         audio: false
//       },
//       function(stream) {
//         var url = window.URL || window.webkitURL;
//         v.src = url ? url.createObjectURL(stream) : stream;
//         v.play();
//       },
//       // function(error) {
//       //   alert('Ошибка (код ошибки ' + error.code + ')');
//       //   return;
//       // }
//     );
//   }
//   else {
//     alert('не поддерживается утсройство');
//     return;
//   };
// });