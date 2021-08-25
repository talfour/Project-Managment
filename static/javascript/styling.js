let arrow = document.querySelectorAll(".fa-chevron-down");

for (var i = 0; i < arrow.length; i++) {
	arrow[i].addEventListener("click", (e) => {
		let arrowParent = e.target.parentElement.parentElement;

		arrowParent.classList.toggle("showMenu");
	});
}

let sidebar = document.querySelector(".sidebar");
const sidebarBtn = document.getElementById("sidebarCollapse");

sidebarBtn.addEventListener("click", () => {
	sidebar.classList.toggle("close");
});
