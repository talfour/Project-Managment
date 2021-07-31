let card = NaN
const csrftoken = getCookie("csrftoken");
let target_id = 0

function allowDrop(ev){
    ev.preventDefault();
}

function drag(ev){
    ev.dataTransfer.setData("text", ev.target.dataset.id)
    card = ev.target
    return target_id = ev.target.dataset.id
}

function drop(ev){
    ev.preventDefault();
    fetch(`/project/task-status-change/`, {
        credentials: "include",
        method: "POST",
        mode: "same-origin",
        headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({
            task_id: target_id,
            new_status: ev.target.dataset.status,
        }),
    })
    .then((response) => response.json())
    .then((response) => {
        if(response.message == "Task status changed"){
            ev.target.appendChild(card);
        }
    })
    
}

function assign_me(ev){
    ev.preventDefault();
    task_id = ev.explicitOriginalTarget.parentElement.parentElement.dataset.id
    fetch(`/project/task-assign-user/`, {
        credentials: "include",
        method: "POST",
        mode: "same-origin",
        headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({
            task_id: task_id,
        }),
    })
    .then((response) => response.json())
    .then((response) => {
        ev.target.remove()
    })
}