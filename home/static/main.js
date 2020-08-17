function imageScroll(element, childNo) {
    childNo--;
    let photos = element.parentElement.parentElement.querySelectorAll(
        ".photos .photo"
    );
    photos.forEach((photo) => {
        photo.style.display = "none";
    });
    element.parentElement.querySelectorAll(".point").forEach((ele) => {
        ele.classList.remove("point-curr");
    });
    element.classList.add("point-curr");
    photos[childNo].style.display = "block";
}

function addToCart(plant) {
    console.log(plant);
    let request = new XMLHttpRequest();
    request.open("GET", `/add-to-cart/?plantId=${plant}`);
    request.onreadystatechange = function () {
        console.log(this.status, this.responseText);
    };
    request.send();
}

document.querySelectorAll(".point:first-child").forEach((ele) => {
    ele.classList.add("point-curr");
});
