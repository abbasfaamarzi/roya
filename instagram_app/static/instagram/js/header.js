document.addEventListener("click", event => { if (event.target.closest("[data-open-create]")) document.dispatchEvent(new CustomEvent("instagram:open-create")); });
