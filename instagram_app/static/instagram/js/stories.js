document.addEventListener("click", event => { const story = event.target.closest("[data-story-user]"); if (story) { story.classList.add("is-viewed"); story.setAttribute("aria-pressed", "true"); } });
