/*
    This Javascript is responsible for sorting the products displayed on the products page.
*/

// BEGIN: JQuery
$(function () {

    // Search bar functionality
    $('.search-bar').on("keyup", function () {
        var value = $(this).val().toLowerCase();

        $(".card").filter(function () {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });

});

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

function categorySelect(id) {
    // Based off the ID, determine what category the user selected
    var checkbox = document.getElementById(id);

    if (checkbox.checked) { // Perform a search if the checkbox is checked
        getProducts(id);
    }
    else { // Remove the associated products
        removeProducts(id);
    }
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

function getProducts(category) { // Request information from the server

    var url = 'filter/?category=' + category;

    fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
    }).then(
        response => response.json()
    ).then(
        products => displayProducts(products)
    )
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

var counter = 0;

function displayProducts(products) { // This function is responsible for displaying the results from the server
    let product_item_section = document.getElementsByClassName('product_item_section')[0];

    if (counter == 0) { // This is to prevent duplicate products from appearing multiple times
        product_item_section.innerHTML = '';
        counter++;
    }

    for (var i = 0; i < products.length; i++) { // Create the required HTML elements to display the products
        // Create the card div
        card = document.createElement('div');
        card.setAttribute('class', 'col card product-card');

        // Create the card body
        card_body = document.createElement('div');
        card_body.setAttribute('class', 'card-body');

        // Create and set the title (In this case it's the product name)
        title = document.createElement('h4');
        title.setAttribute('class', 'product_item_name');
        title.innerHTML = products[i]['name'];

        // Create and set the price for the product
        price = document.createElement('h5');
        price.innerHTML = '\$' + products[i]['price'] + ' ';

        // If the product is a featured product, add the featured badge
        if (products[i]['featured'] == true) {
            featured = document.createElement('span');
            featured.setAttribute('class', 'badge badge-warning');
            featured.innerHTML = 'Featured';
            price.appendChild(featured);
        }

        // Create and set the product's category (ex. Chairs, Tables, etc.)
        category = document.createElement('h6');
        category.setAttribute('class', 'product_item_category');
        categoryText = products[i]['category'];
        categorySubText = categoryText.charAt(0).toUpperCase();
        categoryText = categoryText.replace(categoryText.charAt(0), categorySubText);
        category.innerHTML = categoryText;

        // Create and set the product's description
        description = document.createElement('p');
        description.innerHTML = products[i]['description'];

        // Create the button 'Add to Cart'
        button_div = document.createElement('div');
        button_div.setAttribute('class', 'button_div');

        button = document.createElement('button');
        button.setAttribute('class', 'btn btn-primary cart-button');
        button.setAttribute('data-productId', products[i]['id']);
        button.setAttribute('data-action', 'add');
        button.setAttribute('onclick', 'editCart(this)');
        button.innerHTML = 'Add to Cart';

        button_div.appendChild(button);

        // Append the elements to their respective parent element
        card_body.appendChild(title);
        card_body.appendChild(price);
        card_body.appendChild(category);
        card_body.appendChild(description);
        card.appendChild(card_body);
        card.appendChild(button_div);
        product_item_section.appendChild(card);
    }
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

function removeProducts(category) { // Remove products from view (ex. User unchecks tables category, remove table products from view)
    cards = document.getElementsByClassName('card');
    categories = document.getElementsByClassName('product_item_category');

    for (var i = cards.length - 1; i >= 0; --i) {
        if (categories[i].innerHTML.toLowerCase() == category) {
            cards[i].remove();
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

function editCart(input) { // Responsible for adding products to a user's cart
    var productId = input.getAttribute('data-productId');
    var action = input.getAttribute('data-action');
    var csrftoken = getCookie('csrftoken');
    var url = '';

    // Prepare the data to send to the server
    data = {
        'productId': productId,
    }

    // Determine the URL we are going to use
    if (action === 'add') {
        url = 'add-to-cart/';
    } else if (action === 'remove') {
        url = 'remove-cart-item/';
    } else if (action === 'changeQuantity') {
        url = 'edit-cart-quantity/';
        data['quantity'] = input.value; // Append the quantity to the data we are going to send
    } else {
        return;
    }

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify(data)
    }).then((response) => {
        // If we are removing or changing the quantity on an item in the cart, then refresh the page.
        // This is to prevent the products page from resetting incase the user is viewing a specific category.
        if (action === 'remove' || action === 'changeQuantity') {
            location.reload();
        }

        return response.json()
    }).then(message => { // Depending on the response from the server, display a success or failure alert to the view.
        console.log(message)
    })
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
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