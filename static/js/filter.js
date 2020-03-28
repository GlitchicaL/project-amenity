/*
    This Javascript is responsible for sorting the products displayed on the products page.
*/

// BEGIN: JQuery
$(function () {
    // Search bar functionality
    $('#search_bar').on("keyup", function () {
        var value = $(this).val().toLowerCase();

        $(".product_item").filter(function () {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
});

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

var counter = 0;

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

function categorySelect(id) {
    var checkbox = document.getElementById(id);
    var category = id.substr(9); // Based off the ID, determine what category the user selected

    if (checkbox.checked) { // Perform a search if the checkbox is checked
        searchProducts(category);
    }
    else { // Remove the associated products
        removeProducts(category);
    }
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

function searchProducts(category) { // Request information from the server
    xhttp = new XMLHttpRequest();

    var url = 'filter/?category=' + category;
    console.log(url);

    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var products = JSON.parse(this.responseText);
            addProducts(products); // Once we get the products we need to add it to the HTML
        }
    };

    xhttp.open("GET", url, true);
    xhttp.send();
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

function addProducts(products) { // This function is responsible for displaying the results from the server
    let product_item_section = document.getElementsByClassName('product_item_section')[0];

    if (counter == 0) {
        product_item_section.innerHTML = '';
        counter++;
    }

    for (var i = 0; i < products.length; i++) { // Create the required HTML elements to display the products
        div = document.createElement('div');
        div.setAttribute('class', 'product_item');

        title = document.createElement('h3');
        title.setAttribute('class', 'product_item_name');
        title.innerHTML = products[i]['name'];

        price = document.createElement('h4');
        price.innerHTML = '\$' + products[i]['price'];

        category = document.createElement('h4');
        category.setAttribute('class', 'product_item_category');
        categoryText = products[i]['category'];
        categorySubText = categoryText.charAt(0).toUpperCase();
        categoryText = categoryText.replace(categoryText.charAt(0), categorySubText);
        category.innerHTML = categoryText;

        description = document.createElement('p');
        description.innerHTML = products[i]['description'];

        product_item_section.appendChild(div);
        div.appendChild(title);
        div.appendChild(price);
        div.appendChild(category);
        div.appendChild(description);
    }
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

function removeProducts(category) {
    products = document.getElementsByClassName('product_item');
    categories = document.getElementsByClassName('product_item_category');

    for (var i = products.length - 1; i >= 0; --i) {
        if (categories[i].innerHTML.toLowerCase() == category) {
            products[i].remove();
        }
    }
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

function sortProducts(id) { // Responsible for sorting alphabetical order or by price.
    // Determine how we want to sort... alphabetical order, lowest price, etc.
    // Maybe implement JQuery for this?
    return;
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/*
    NOTE:
        This function will SOMETIMES sort the products in alphabetical order, not 100%
        of the time... Maybe implement JQuery?
*/
function toggleLetterOrder(id) {
    let products = document.getElementsByClassName('product_item');
    let products_name = document.getElementsByClassName('product_item_name');

    let products_html = []; // Copy of products (HTML only)
    let name = []; // Name of product

    var firstPosition = [];
    var html_to_replace_position;
    var html_to_replace = '<h4>If you see this... something bad happened</h4>';

    for (var i = 0; i < products.length; i++) {
        products_html[i] = products[i].innerHTML; // Get the HTML of all the 'products'

        firstPosition[i] = products_html[i].indexOf(products_name[i].innerHTML); // Get index of product name
        //console.log(firstPosition[i]);

        name[i] = products_html[i].substr(firstPosition[i], products_name[i].innerHTML.length); // Get the product name

        //console.log(name[i]);
    }

    if (id == 'radio_az') {
        name.sort();
    }

    if (id == 'radio_za') {
        name.sort();
        name.reverse();
    }

    for (var i = 0; i < products.length; i++) {
        if (name[i] != products_name[i].innerHTML) { // After sorting, if the names do not match...
            // Swap the HTML around?

            // Grab 'products' html, store in a temp var
            temp = products[i].innerHTML;

            // Replace 'products' html with the correct html (In order to do this we have to find the correct HTML)
            for (var j = 0; j < products.length; j++) {
                // We can find the correct HTML by comparing names
                for (var k = 0; k < products.length; k++) {
                    if (name[j] == products_name[k].innerHTML) {
                        html_to_replace_position = j;

                        products[k].innerHTML = products_html[html_to_replace_position];
                        products[html_to_replace_position] = temp;
                        break;
                    }
                }
            }
            //console.log('Found a no match\n' + temp);
        }
        else {
            //console.log('Found a match');
        }
    }
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////