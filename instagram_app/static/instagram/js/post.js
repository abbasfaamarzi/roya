document.addEventListener("click", event => {
  const like = event.target.closest(".post-like");
  const media = event.target.closest("[data-double-like]");
  const card = event.target.closest(".post-card");
  if (like) { const active = like.getAttribute("aria-pressed") !== "true"; like.setAttribute("aria-pressed", String(active)); const count = card?.querySelector(".post-likes"); if (count) { const n = Number(count.textContent.replace(/[^0-9]/g, "")) || 0; count.textContent = `${Math.max(0, n + (active ? 1 : -1)).toLocaleString("fa-IR")} پسند`; } }
  if (media && card) card.querySelector(".post-like")?.click();
  if (event.target.closest(".post-comment-focus")) card?.querySelector(".comment-form input")?.focus();
  if (event.target.closest(".post-save")) event.target.closest(".post-save").classList.toggle("is-saved");
});
document.addEventListener("submit", event => { if (!event.target.matches(".comment-form")) return; event.preventDefault(); const input = event.target.elements.comment; const value = input.value.trim(); if (!value) return; const row = document.createElement("p"); row.textContent = value; event.target.parentElement.querySelector(".comment-list").append(row); input.value = ""; });
