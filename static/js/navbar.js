$(document).ready(function() {
    var ShowForm = function() {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            data: $("form").serialize(),
            beforeSend: function() {
                $('#modal-fournisseur').modal('show');
                $('#modal-employee').modal('show');
                $('#modal-pharmacie').modal('show');
                $('#modal-article').modal('show');
                $('#modal-medicament').modal('show');
                $('#modal-stock').modal('show');
                $('#modal-stocke').modal('show');

            },
            success: function(data) {
                $('#modal-fournisseur .modal-content').html(data.html_form);
                $('#modal-employee .modal-content').html(data.html_form);
                $('#modal-article .modal-content').html(data.html_form);
                $('#modal-medicament .modal-content').html(data.html_form);
                $('#modal-stock .modal-content').html(data.html_form);

            }
        });
    };

    var saveForm = function() {
        var form = $(this);
        $.ajax({
            url: form.attr('data-url'),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function(data) {
                if (data.form_is_valid) {
                    $("#fournisseur-table tbody").html(data.html_fournisseur);
                    $("#id-table tbody").html(data.html_employee);
                    $("#employee-table tbody").html(data.html_employee_non);
                    $("#id-article tbody").html(data.html_article);
                    $("#id-medicament tbody").html(data.html_medicament);
                    $("#id-stock tbody").html(data.html_stock);
                    $("#modal-employee ").modal("hide");
                    $("#modal-fournisseur ").modal("hide");
                    $("#modal-article ").modal("hide");
                    $("#modal-medicament").modal("hide");
                    $("#modal-stock").modal("hide");

                } else {
                    $("#modal-fournisseur  .modal-content").html(data.html_form);
                    $("#modal-employee .modal-content").html(data.html_form);
                    $("#modal-article .modal-content").html(data.html_form);
                    $("#modal-medicament .modal-content").html(data.html_form);
                    $("#modal-stock .modal-content").html(data.html_form);

                }
            }
        });
        return false;
    };

    //create
    $('.show-form').click(ShowForm);
    $("#modal-fournisseur ").on("submit", ".create-form", saveForm);
    //update
    $('#fournisseur-table').on("click", ".show-form-update", ShowForm);
    $('#modal-fournisseur').on("submit", ".update-form", saveForm);
    //delete
    $('#fournisseur-table').on("click", ".show-form-delete", ShowForm);
    $('#modal-fournisseur').on("submit", ".delete-form", saveForm)
        //show
    $('#fournisseur-table').on("click", ".form-show", ShowForm);
    //Employee
    // update emplyee

    $('#id-table').on("click", ".show-form-updat", ShowForm);
    $('#employee-table').on("click", ".show-form-update", ShowForm);
    $('#id-table').on("click", ".show-form-delet", ShowForm);
    $('#employee-table').on("click", ".show-form-delete", ShowForm);

    $('#modal-employee').on("submit", ".update-form", saveForm);

    $('#id-article').on("click", ".form-show", ShowForm);
    $("#modal-article ").on("submit", ".create-form", saveForm);
    $('#id-article').on("click", ".show-form-delete", ShowForm);
    $('#modal-article').on("submit", ".delete-form", saveForm);
    $('#id-article').on("click", ".show-form-update", ShowForm);
    $('#modal-article').on("submit", ".update-form", saveForm);

    $('#id-medicament').on("click", ".form-show", ShowForm);
    $("#modal-medicament").on("submit", ".create-form", saveForm);
    $('#id-medicament').on("click", ".show-form-update", ShowForm);
    $('#modal-medicament').on("submit", ".update-form", saveForm);
    $('#id-medicament').on("click", ".show-form-delete", ShowForm);
    $('#modal-medicament').on("submit", ".delete-form", saveForm);

    $('#id-stock').on("click", ".form-show", ShowForm);

    $("#modal-stock").on("submit", ".create-form", saveForm);
    $('#id-stock').on("click", ".show-form-update", ShowForm);
    $('#modal-stock').on("submit", ".update-form", saveForm);
    $('#id-stock').on("click", ".show-form-delete", ShowForm);
    $('#modal-stock ').on("submit", ".delete-form", saveForm);



});


var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function() {
        var itemId = this.dataset.item
        var action = this.dataset.action

        console.log('itemId', itemId, 'Action', action)
        console.log('USER', user)
        if (user == 'Anonymoususer') {
            console.log("L'utilisateur n'est pas connecté")
        } else {
            updateUserOrder(itemId, action)
        }
    })
}


function updateUserOrder(itemId, action) {
    console.log("utilisateur est connecté")
    var url = '/update_item/'
    fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'itemId': itemId, 'action': action })
        })
        .then((response) => {
            return response.json();
        })
        .then((data) => {
                location.reload();
            }

        )
}

var updateBtn = document.getElementsByClassName('update-car')
for (i = 0; i < updateBtn.length; i++) {
    updateBtn[i].addEventListener('click', function() {
        var itemId = this.dataset.item
        var action = this.dataset.action

        console.log('itemId', itemId, 'Action', action)
        console.log('USER', user)
        if (user == 'Anonymoususer') {
            console.log("L'utilisateur n'est pas connecté")
        } else {
            updateUserOrde(itemId, action)
        }
    })
}

function updateUserOrde(itemId, action) {
    console.log("utilisateur est connecté")
    var url = '/update_article/'
    fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'itemId': itemId, 'action': action })
        })
        .then((response) => {
            return response.json();
        })
        .then((data) => {
                location.reload();
            }

        )
}
var updateBt = document.getElementsByClassName('update-ca')
for (i = 0; i < updateBt.length; i++) {
    updateBt[i].addEventListener('click', function() {
        var itemId = this.dataset.item
        var action = this.dataset.action

        console.log('itemId', itemId, 'Action', action)
        console.log('USER', user)
        if (user == 'Anonymoususer') {
            console.log("L'utilisateur n'est pas connecté")
        } else {
            updateUserOrd(itemId, action)
        }
    })
}

function updateUserOrd(itemId, action) {
    console.log("utilisateur est connecté")
    var url = '/vente_delete/'
    fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'itemId': itemId, 'action': action })
        })
        .then((response) => {
            return response.json();
        })
        .then((data) => {
                location.reload();
            }

        )
}

function updateUserOrde(itemId, action) {
    console.log("utilisateur est connecté")
    var url = '/update_article/'
    fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'itemId': itemId, 'action': action })
        })
        .then((response) => {
            return response.json();
        })
        .then((data) => {
                location.reload();
            }

        )
}
var updateBt = document.getElementsByClassName('update-commande')
for (i = 0; i < updateBt.length; i++) {
    updateBt[i].addEventListener('click', function() {
        var itemId = this.dataset.item
        var action = this.dataset.action

        console.log('itemId', itemId, 'Action', action)
        console.log('USER', user)
        if (user == 'Anonymoususer') {
            console.log("L'utilisateur n'est pas connecté")
        } else {
            updateUserrd(itemId, action)
        }
    })
}

function updateUserrd(itemId, action) {
    console.log("utilisateur est connecté")
    var url = '/update_commande/'
    fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'itemId': itemId, 'action': action })
        })
        .then((response) => {
            return response.json();
        })
        .then((data) => {
                location.reload();
            }

        )
}

var updateBts = document.getElementsByClassName('update-pane')

for (i = 0; i < updateBts.length; i++) {
    updateBts[i].addEventListener('click', function() {
        var itemId = this.dataset.item
        var action = this.dataset.action

        console.log('itemId', itemId, 'Action', action)
        console.log('USER', user)
        if (user == 'Anonymoususer') {
            console.log("L'utilisateur n'est pas connecté")
        } else {
            updaeUserOrder(itemId, action)
        }
    })
}

function updaeUserOrder(itemId, action) {
    console.log("utilisateur est connecté")
    var url = '/update_online/'
    fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'itemId': itemId, 'action': action })
        })
        .then((response) => {
            return response.json();
        })
        .then((data) => {
                location.reload();
            }

        )
}

function addCookieItem(itemId, action) {
    console.log('User is not authenticated')

    if (action == 'add') {
        if (cart[itemId] == undefined) {
            cart[itemId] = { 'quantity': 1 }

        } else {
            cart[itemId]['quantity'] += 1
        }
    }

    if (action == 'remove') {
        cart[itemId]['quantity'] -= 1

        if (cart[itemId]['quantity'] <= 0) {
            console.log('Item should be deleted')
            delete cart[itemId];
        }
    }
    console.log('CART:', cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"

    location.reload()
}