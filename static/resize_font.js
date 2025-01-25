let text = document.getElementById('text');
let fontBigger = document.getElementById('bigger');
let fontSmaller = document.getElementById('smaller');

text.style.fontSize = '20px';
console.log(text.style.fontSize);

fontBigger.onclick = function() {
    text.style.fontSize = parseInt(text.style.fontSize) + 1 + 'px';
    console.log("font is bigger");
};

fontSmaller.onclick = function() {
    text.style.fontSize = parseInt(text.style.fontSize) - 1 + 'px';
    console.log('font is smaller');
};