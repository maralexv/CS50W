let myelement = document.querySelector('h1');

function getRandomColor() {
  let letters = '0123456789ABCDEF';
  let color = '#';
  for (var i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
}

function setElementColor() {
  myelement.style.color = getRandomColor();
}

setInterval('setElementColor()', 222);