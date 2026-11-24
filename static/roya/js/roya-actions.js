/* Roya Language browser-to-Django event bridge and Instagram demo UI. */
(function (global, document) {
  "use strict";
  if (global.RoyaActions) return;

  function readConfigs() {
    return Array.from(document.querySelectorAll('script[id^="roya-actions-config-"]'))
      .map(function (node) {
        try { return JSON.parse(node.textContent || "{}"); }
        catch (error) { console.error("[Roya] Invalid action configuration", error); return null; }
      }).filter(Boolean);
  }

  function findBinding(target, eventName, configs) {
    for (var node = target; node && node.nodeType === 1; node = node.parentElement) {
      if (!node.id) continue;
      for (var index = configs.length - 1; index >= 0; index -= 1) {
        var actions = configs[index].actions || {};
        var binding = actions[node.id] && actions[node.id][eventName];
        if (binding) return { binding: binding, element: node, config: configs[index] };
      }
    }
    return null;
  }

  function eventData(event, element) {
    var target = event.target;
    var data = { type: event.type };
    if (target && "value" in target) data.value = target.value;
    if (target && "checked" in target) data.checked = !!target.checked;
    if (event.key) data.key = event.key;
    var createOverlay = element && element.closest ? element.closest(".ig-create-overlay") : null;
    if (createOverlay) {
      var caption = createOverlay.querySelector(".ig-caption-field input, .ig-caption-field textarea");
      if (caption) data.value = caption.value;
    }
    if (event.type === "submit" && element instanceof HTMLFormElement) {
      data.form = Object.fromEntries(new FormData(element).entries());
    }
    return data;
  }

  function showToast(message) {
    if (!message) return;
    var previous = document.querySelector(".ig-toast");
    if (previous) previous.remove();
    var toast = document.createElement("div");
    toast.className = "ig-toast";
    toast.setAttribute("role", "status");
    toast.textContent = String(message);
    document.body.appendChild(toast);
    global.setTimeout(function () { toast.remove(); }, 2800);
  }

  function closeViewer() {
    var overlay = document.querySelector(".ig-viewer-overlay");
    if (overlay) overlay.remove();
  }

  function showViewer(type, data) {
    closeViewer();
    var overlay = document.createElement("div");
    overlay.className = "ig-viewer-overlay";
    overlay.addEventListener("click", function (event) {
      if (event.target === overlay) closeViewer();
    });

    var dialog = document.createElement("section");
    dialog.className = "ig-viewer-dialog";
    dialog.setAttribute("role", "dialog");
    dialog.setAttribute("aria-modal", "true");

    var close = document.createElement("button");
    close.type = "button";
    close.className = "ig-viewer-close";
    close.setAttribute("aria-label", "بستن");
    close.textContent = "×";
    close.addEventListener("click", closeViewer);
    dialog.appendChild(close);

    var title = document.createElement("div");
    title.className = "ig-viewer-title";
    title.textContent = type === "story" ? ("استوری " + (data.username || "")) : (data.username || "پست");
    dialog.appendChild(title);

    var imageUrl = type === "story" ? data.image : (data.image || (data.post && data.post.image));
    if (imageUrl) {
      var image = document.createElement("img");
      image.className = "ig-viewer-image";
      image.src = String(imageUrl);
      image.alt = type === "story" ? (data.username || "استوری") : ((data.post && data.post.caption) || "تصویر پست");
      dialog.appendChild(image);
    }

    if (type === "post") {
      var post = data.post || {};
      var caption = document.createElement("div");
      caption.className = "ig-viewer-copy";
      caption.textContent = (post.username ? post.username + "  " : "") + (post.caption || "");
      dialog.appendChild(caption);
      var meta = document.createElement("div");
      meta.className = "ig-viewer-meta";
      meta.textContent = String(post.likes || 0) + " پسند  ·  " + String(post.comments_count || 0) + " دیدگاه";
      dialog.appendChild(meta);
    } else if (!imageUrl) {
      var empty = document.createElement("div");
      empty.className = "ig-viewer-copy";
      empty.textContent = "برای این استوری تصویری ثبت نشده است.";
      dialog.appendChild(empty);
    }

    overlay.appendChild(dialog);
    document.body.appendChild(overlay);
    close.focus();
  }

  function applyResult(result, element) {
    if (!result || typeof result !== "object") return;
    if (result.updates && typeof result.updates === "object") {
      Object.keys(result.updates).forEach(function (selector) {
        try {
          var target = document.querySelector(selector);
          if (target) target.textContent = String(result.updates[selector]);
        } catch (error) { console.warn("[Roya] Invalid update selector", selector); }
      });
    }

    if (element && typeof result.liked === "boolean") {
      element.setAttribute("aria-pressed", String(result.liked));
      element.classList.toggle("is-liked", result.liked);
    }
    if (element && Number.isFinite(Number(result.likes))) {
      var postCard = element.closest(".ig-post-card");
      var count = postCard && postCard.querySelector(".ig-post-likes");
      if (count) count.textContent = String(result.likes) + " پسند";
    }
    if (element && typeof result.saved === "boolean") {
      element.setAttribute("aria-pressed", String(result.saved));
      element.classList.toggle("is-saved", result.saved);
    }
    if (element && typeof result.following === "boolean") {
      var row = element.closest(".ig-suggestion-row");
      var label = row && row.querySelector(".ig-follow-button .roya-button__label");
      if (label) label.textContent = result.following ? "دنبال می‌کنید" : "دنبال کردن";
      element.setAttribute("aria-pressed", String(result.following));
    }

    if (result.modal === "story" || result.modal === "post") showViewer(result.modal, result);
    if (result.open_create) {
      var createOverlay = document.querySelector(".ig-create-overlay");
      if (createOverlay) {
        createOverlay.classList.add("is-open");
        var captionField = createOverlay.querySelector(".ig-caption-field input, .ig-caption-field textarea");
        if (captionField) captionField.focus();
      }
    }
    if (result.close_create) {
      var overlay = document.querySelector(".ig-create-overlay");
      if (overlay) overlay.classList.remove("is-open");
    }
    if (typeof result.filter_text === "string") {
      var query = result.filter_text.toLocaleLowerCase();
      document.querySelectorAll(".ig-post-card").forEach(function (card) {
        card.hidden = !!query && !card.textContent.toLocaleLowerCase().includes(query);
      });
    }
    if (result.navigate_to) {
      var targetId = String(result.navigate_to).replace(/^#/, "");
      var destination = document.getElementById(targetId);
      if (destination) destination.scrollIntoView({ behavior: "smooth", block: "start" });
    }
    if (result.share_text) {
      var shareText = String(result.share_text);
      var copyShareText = function () {
        if (global.navigator && global.navigator.clipboard && global.navigator.clipboard.writeText) {
          global.navigator.clipboard.writeText(shareText).then(function () { showToast("متن پست کپی شد."); })
            .catch(function () { showToast(shareText); });
        } else {
          showToast(shareText);
        }
      };
      if (global.navigator && global.navigator.share) {
        global.navigator.share({ text: shareText }).catch(copyShareText);
      } else {
        copyShareText();
      }
    }
    if (result.notice) showToast(result.notice);
    if (result.reload) global.location.reload();
  }

  async function dispatch(event, eventName) {
    var configs = readConfigs();
    if (!configs.length) return;
    var match = findBinding(event.target, eventName, configs);
    if (!match) return;
    if (eventName === "on_submit") event.preventDefault();

    var config = match.config;
    try {
      var response = await fetch(config.endpoint, {
        method: "POST",
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": config.csrf_token || ""
        },
        body: JSON.stringify({
          action: match.binding.action,
          component_id: match.element.id,
          event: eventData(event, match.element),
          args: match.binding.args || {}
        })
      });
      var payload = await response.json();
      if (!response.ok || !payload.ok) throw new Error(payload.error || "Action request failed.");
      applyResult(payload.result, match.element);
      document.dispatchEvent(new CustomEvent("roya:action-success", {
        detail: { action: match.binding.action, component: match.element, result: payload.result }
      }));
    } catch (error) {
      console.error("[Roya] Action failed:", error);
      showToast("اجرای عملیات ناموفق بود.");
      document.dispatchEvent(new CustomEvent("roya:action-error", {
        detail: { action: match.binding.action, component: match.element, error: error }
      }));
    }
  }

  var eventMap = {
    pointerdown: "on_press",
    pointerup: "on_release",
    click: "on_click",
    change: "on_change",
    submit: "on_submit",
    focusin: "on_focus",
    focusout: "on_blur"
  };
  Object.keys(eventMap).forEach(function (nativeName) {
    document.addEventListener(nativeName, function (event) { dispatch(event, eventMap[nativeName]); }, true);
  });

  document.addEventListener("click", function (event) {
    var overlay = document.querySelector(".ig-create-overlay.is-open");
    if (overlay && event.target === overlay) overlay.classList.remove("is-open");
  });
  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
      closeViewer();
      var overlay = document.querySelector(".ig-create-overlay.is-open");
      if (overlay) overlay.classList.remove("is-open");
    }
  });

  global.RoyaActions = { dispatch: dispatch, readConfigs: readConfigs, applyResult: applyResult };
})(window, document);