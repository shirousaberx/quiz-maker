let radio_idx = document.getElementsByClassName("choice").length;

function insert_choice(node) {
    let choice_node = 
    `<div class="choice input-group mt-2">
        <div class="input-group-text">
            <input class="form-check-input mt-0" type="radio" name="choice" value="${radio_idx}" required>
        </div>
        <input type="text" name="${radio_idx}" class="form-control" required>
        <button class="btn btn-danger" type="button" onclick="delete_choice(this)"><i class="bi bi-trash-fill"></i></button>
    </div>`

    // check if there are choices exist
    // if it does, add choice after the last choice
    // if it doesnt, add choice after "add button"
    let choices = document.getElementsByClassName("choice");
    if (choices.length === 0) {    // no choices
        node.insertAdjacentHTML("afterend", choice_node);
    } else {
        node.parentElement.insertAdjacentHTML("beforeend", choice_node);
    }

    radio_idx += 1;
}

function delete_choice(node) {
    let choices = document.getElementsByClassName("choice");
    if (choices.length > 2) {
        node.parentElement.remove();
    } else {
        alert('There must be at least 1 choice');
    }
}