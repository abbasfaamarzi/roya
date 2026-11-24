const overlay = document.querySelector("[data-create-overlay]");
document.addEventListener("instagram:open-create", () => { if (overlay) { overlay.hidden = false; overlay.querySelector("textarea")?.focus(); } });
document.addEventListener("click", event => { if (event.target.closest("[data-close-create]") || event.target === overlay) if (overlay) overlay.hidden = true; });
document.addEventListener("submit", event => { if (!event.target.matches(".create-post-form")) return; event.preventDefault(); const caption = event.target.elements.caption.value.trim(); if (caption) alert("پست نمایشی آماده شد: " + caption); if (overlay) overlay.hidden = true; event.target.reset(); });
document.addEventListener("keydown", event => { if (event.key === "Escape" && overlay) overlay.hidden = true; });
