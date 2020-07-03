let featured_products = document.querySelectorAll("div.featured-products-card");
let arrows = document.querySelectorAll("i.slideshow-button");
let dots = document.querySelectorAll("span.dot");

var index = 1;
var prevIndex = index;

// Display only the first product first.
showProduct(index, -1);

// Automatic slideshow
auto_slides = setInterval(() => {
    prevIndex = index;
    index++;

    if (index > featured_products.length) { index = 1; }

    showProduct(index, prevIndex);
}, 5000);

// Add click event to arrows
arrows.forEach(arrow => {
    arrow.addEventListener("click", () => {
        clearInterval(auto_slides); // When the user clicks on the arrows stop the automatic slideshow

        prevIndex = index;

        if (arrow.getAttribute("data-slideshow-action") === "right") {
            index++;

            if (index > featured_products.length) { index = 1; }
        }
        else {
            index--;

            if (index <= 0) { index = 3; }
        }

        showProduct(index, prevIndex);
    });
});

// Add click event to dots 
dots.forEach(dot => {
    dot.addEventListener("click", () => {
        clearInterval(auto_slides);

        prevIndex = index;

        index = dot.getAttribute("data-index");

        showProduct(index, prevIndex);
    })
})

function showProduct(index, prevIndex) {
    if (prevIndex != -1) {
        dots[prevIndex - 1].className = "dot";
        featured_products[prevIndex - 1].style.display = "none";
    }

    // Add the active class for the next dot
    dots[index - 1].className += " active";
    featured_products[index - 1].style.display = "block";
}