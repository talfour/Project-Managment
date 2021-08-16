let card = NaN;
const csrftoken = getCookie("csrftoken");
let target_id = 0;

function insertAfter(referenceNode, newNode) {
	referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
}

function addMessage(messageText, messageType) {
	const nav = document.getElementsByClassName("navbar");
	let messExists = document.getElementById("message");
    console.log(messExists)
    if(messExists){
        messExists.remove()
    }
	let message = document.createElement("div");
	message.setAttribute("id", "message");
	message.innerHTML = `<div class="alert alert-${messageType} alert-dismissible fade show text-center" role="alert">
    ${messageText}
    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
  </div>`;
	insertAfter(nav[0], message);
}

function allowDrop(ev) {
	ev.preventDefault();
}

function drag(ev) {
	ev.dataTransfer.setData("text", ev.target.dataset.id);
	card = ev.target;
	return (target_id = ev.target.dataset.id);
}

function drop(ev) {
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
			if (response.message == "Task status changed") {
				ev.target.appendChild(card);
				addMessage(response.message, "success");
			} else {
				addMessage(response.message, "danger");
			}
			console.log(response);
		});
}

function assign_me(ev) {
	ev.preventDefault();
	console.log(ev);
	task_id = ev.explicitOriginalTarget.parentElement.parentElement.dataset.id;
	if (task_id == null) {
		task_id = ev.explicitOriginalTarget.dataset.id;
	}

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
			ev.target.remove();
		});
}
