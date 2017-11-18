// Get the modal
var modal = document.getElementById('imageModal');

// Get the image and insert it inside the modal - use its "alt" text as a caption

var modalImg = document.getElementById("img01");
var captionText = document.getElementById("caption");


// Get the <span> element that closes the modal
//var span = document.getElementsByClassName("close")[0];
var span = document.getElementById("closemodal");
//var span =  $('#closemodal.close');

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
    modal.style.display = "none";
    console.log('close!');
}


$(".image-row-gallery").on('click','.myImg',imageModelPopUp)

function imageModelPopUp(){
    console.log('Click!');
    modal.style.display = "block";
    modalImg.src = this.src;
    captionText.innerHTML = this.alt;
}
