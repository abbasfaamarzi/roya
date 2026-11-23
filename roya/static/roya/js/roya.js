/* Roya JS runtime: lifecycle, events, behaviors */
(function (global) {
  "use strict";

  const Roya = {
    version: "0.2.0",
    registry: new Map(),
    bus: new Map(),

    register(name, factory) {
      this.registry.set(name, factory);
    },

    emit(type, detail) {
      const payload = { type, timestamp: Date.now(), detail: detail || {} };
      (this.bus.get(type) || []).forEach((h) => {
        try { h(payload); } catch (err) { console.error("[Roya]", err); }
      });
    },

    on(type, handler) {
      if (!this.bus.has(type)) this.bus.set(type, []);
      this.bus.get(type).push(handler);
      return () => this.off(type, handler);
    },

    off(type, handler) {
      const list = this.bus.get(type) || [];
      const i = list.indexOf(handler);
      if (i >= 0) list.splice(i, 1);
    },

    mount(root) {
      const scope = root || document;
      scope.querySelectorAll("[data-roya-component]").forEach((el) => {
        if (el.dataset.royaMounted === "true") return;
        const name = el.dataset.royaComponent;
        const factory = this.registry.get(name);
        try {
          if (factory) factory(el);
          else this.mountBuiltin(name, el);
          el.dataset.royaMounted = "true";
        } catch (err) { console.error("[Roya] mount failed:", name, err); }
      });
    },

    mountBuiltin(name, el) {
      if (name === "date_picker" || name === "time_picker") {
        const input = el.querySelector("input");
        if (!input) return;
        const eventPrefix = name === "date_picker" ? "date-picker" : "time-picker";
        input.addEventListener("input", () => this.emit(eventPrefix + ":input", { id: el.id, value: input.value }));
        input.addEventListener("change", () => this.emit(eventPrefix + ":change", { id: el.id, value: input.value }));
        return;
      }
      if (name === "bottom_sheet") {
        el.querySelectorAll("[data-roya-sheet-dismiss]").forEach((button) => button.addEventListener("click", () => {
          const isBackdrop = button.classList.contains("roya-bottom-sheet__backdrop");
          const canClose = el.dataset.dismissible !== "false" && (!isBackdrop || el.dataset.closeOnBackdrop !== "false");
          if (canClose) {
            el.classList.remove("is-open"); el.hidden = true;
            this.emit("bottom-sheet:close", { id: el.id });
          }
        }));
        if (!el.hidden) requestAnimationFrame(() => el.classList.add("is-open"));
        return;
      }
      if (name === "virtual_list") this.mountVirtualList(el);
    },

    mountVirtualList(el) {
      const viewport = el.querySelector(".roya-virtual-list__viewport");
      const windowEl = el.querySelector(".roya-virtual-list__window");
      const spacer = el.querySelector(".roya-virtual-list__spacer");
      if (!viewport || !windowEl || !spacer) return;
      const items = JSON.parse(el.dataset.items || "[]");
      const rowHeight = Math.max(1, Number(el.dataset.itemHeight) || 48);
      const overscan = Math.max(0, Number(el.dataset.overscan) || 0);
      spacer.style.height = (items.length * rowHeight) + "px";
      let scheduled = false;
      const render = () => {
        scheduled = false;
        const first = Math.max(0, Math.floor(viewport.scrollTop / rowHeight) - overscan);
        const visible = Math.ceil(viewport.clientHeight / rowHeight) + overscan * 2;
        const last = Math.min(items.length, first + visible);
        windowEl.style.transform = `translateY(${first * rowHeight}px)`;
        const fragment = document.createDocumentFragment();
        for (let index = first; index < last; index += 1) {
          const row = document.createElement("div");
          row.className = "roya-virtual-list__item";
          row.style.height = rowHeight + "px";
          row.setAttribute("role", "listitem");
          row.setAttribute("aria-posinset", String(index + 1));
          row.setAttribute("aria-setsize", String(items.length));
          row.textContent = items[index];
          row.addEventListener("click", () => this.emit("virtual-list:item-click", {
            id: el.id, index, value: items[index]
          }));
          fragment.appendChild(row);
        }
        windowEl.replaceChildren(fragment);
      };
      viewport.addEventListener("scroll", () => {
        if (!scheduled) { scheduled = true; requestAnimationFrame(render); }
      }, { passive: true });
      render();
    },
  };

  Roya.behaviors = {
    ripple(el) {
      el.addEventListener("pointerdown", (e) => {
        const rect = el.getBoundingClientRect();
        const span = document.createElement("span");
        const size = Math.max(rect.width, rect.height) * 2;
        span.style.cssText =
          `position:absolute;border-radius:50%;pointer-events:none;` +
          `width:${size}px;height:${size}px;` +
          `left:${e.clientX - rect.left - size / 2}px;` +
          `top:${e.clientY - rect.top - size / 2}px;` +
          `background:currentColor;opacity:.25;` +
          `transform:scale(0);transition:transform .4s ease-out,opacity .4s ease-out;`;
        el.appendChild(span);
        requestAnimationFrame(() => {
          span.style.transform = "scale(1)";
          span.style.opacity = "0";
        });
        setTimeout(() => span.remove(), 450);
      });
    },
    hover(el) {
      el.addEventListener("pointerenter", () => {
        el.dataset.hovering = "true";
        Roya.emit("hover:enter", { target: el.id });
      });
      el.addEventListener("pointerleave", () => {
        delete el.dataset.hovering;
        Roya.emit("hover:leave", { target: el.id });
      });
    },
    focusRing(el) {
      el.addEventListener("focus", () => Roya.emit("focus:enter", { target: el.id }));
      el.addEventListener("blur", () => Roya.emit("focus:leave", { target: el.id }));
    },
  };

  if (typeof document !== "undefined") {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", () => Roya.mount());
    } else {
      Roya.mount();
    }
  }

  global.Roya = Roya;
})(window);


/* Roya component interaction layer. Delegated native events work for mouse,
   touch, pen and keyboard; all controls remain usable without a pointer. */
(function (global) {
  "use strict";
  const R = global.Roya;
  if (!R || R.__interactionLayer) return;
  R.__interactionLayer = true;

  const emit = (name, type, detail) => R.emit(type, Object.assign({ id: name.id }, detail || {}));
  const closest = (el, selector, root) => {
    const node = el.closest(selector);
    return node && root.contains(node) ? node : null;
  };
  const setActive = (nodes, active, className) => nodes.forEach((node) => {
    const yes = node === active;
    node.classList.toggle(className || "is-active", yes);
    if (node.hasAttribute("aria-selected")) node.setAttribute("aria-selected", String(yes));
    if (node.hasAttribute("aria-current")) {
      if (yes) node.setAttribute("aria-current", "page");
      else node.removeAttribute("aria-current");
    }
  });

  const oldMount = R.mountBuiltin.bind(R);
  R.mountBuiltin = function (name, el) {
    oldMount(name, el);
    const q = (s) => el.querySelector(s);
    const all = (s) => Array.from(el.querySelectorAll(s));

    if (name === "button" || name === "fab" || name === "icon_button") {
      const button = q("button");
      if (button) {
        if (R.behaviors && R.behaviors.ripple) R.behaviors.ripple(button);
        button.addEventListener("click", () => {
        if (name === "icon_button") {
          const selected = button.getAttribute("aria-pressed") !== "true";
          button.setAttribute("aria-pressed", String(selected));
          emit(el, "icon_button:toggle", { selected });
        }
        emit(el, name === "button" ? "button:click" : name === "fab" ? "fab:click" : "icon_button:click");
        });
      }
    }

    if (name === "checkbox") {
      const input = q('input[type="checkbox"]');
      if (input) {
        if (input.dataset.indeterminate === "true") input.indeterminate = true;
        input.addEventListener("change", () => {
        emit(el, "change", { checked: input.checked, value: input.value });
        emit(el, input.checked ? "check" : "uncheck", { checked: input.checked });
        });
      }
    }
    if (name === "switch") {
      const input = q('input[type="checkbox"]');
      if (input) input.addEventListener("change", () => {
        emit(el, "switch:change", { checked: input.checked, value: input.value });
        emit(el, input.checked ? "switch:on" : "switch:off", { checked: input.checked });
      });
    }
    if (name === "radio_group") {
      all('input[type="radio"]').forEach((input) => input.addEventListener("change", () => {
        if (input.checked) emit(el, "radio:change", { value: input.value });
      }));
    }
    if (name === "select") {
      const select = q("select");
      if (select) select.addEventListener("change", () => {
        const value = select.multiple ? Array.from(select.selectedOptions).map(o => o.value) : select.value;
        emit(el, "select:change", { value });
        emit(el, "select:select", { value });
      });
    }
    if (name === "slider") {
      const input = q('input[type="range"]');
      if (input) {
        const output = q("[data-roya-slider-value]");
        input.addEventListener("input", () => {
          if (output) output.textContent = input.value;
          emit(el, "input", { value: Number(input.value) });
        });
        input.addEventListener("change", () => emit(el, "change", { value: Number(input.value) }));
        input.addEventListener("pointerdown", () => emit(el, "slide:start", { value: Number(input.value) }));
        ["pointerup", "pointercancel", "blur"].forEach(type => input.addEventListener(type, () => emit(el, "slide:end", { value: Number(input.value) })));
      }
    }
    if (name === "tabs") {
      const tabs = all('[role="tab"], .roya-tab');
      const activate = (tab) => {
        setActive(tabs, tab, "roya-tab--active");
        tabs.forEach(t => t.setAttribute("aria-selected", String(t === tab)));
        emit(el, "tab:change", { index: Number(tab.dataset.index || tabs.indexOf(tab)), label: tab.textContent.trim() });
        emit(el, "tab:select", { index: Number(tab.dataset.index || tabs.indexOf(tab)) });
      };
      tabs.forEach((tab, index) => {
        tab.setAttribute("tabindex", tab.classList.contains("roya-tab--active") ? "0" : "-1");
        tab.addEventListener("click", () => activate(tab));
        tab.addEventListener("keydown", (event) => {
          if (!["ArrowRight", "ArrowLeft", "Home", "End"].includes(event.key)) return;
          event.preventDefault();
          const next = event.key === "Home" ? 0 : event.key === "End" ? tabs.length - 1 :
            (index + (event.key === "ArrowRight" ? 1 : -1) + tabs.length) % tabs.length;
          tabs[next].focus(); activate(tabs[next]);
        });
      });
    }
    if (name === "list") {
      all("[data-roya-list-item]").forEach((item, index) => {
        const activate = () => {
        if (el.dataset.selectable === "true") {
          if (el.dataset.selectionMode !== "multiple") all("[data-roya-list-item]").forEach(n => n.classList.remove("is-selected"));
          item.classList.toggle("is-selected");
          emit(el, "list:item-select", { index, selected: item.classList.contains("is-selected") });
          emit(el, "list:change", { index });
        }
        emit(el, "list:item-click", { index, value: item.dataset.value || item.textContent.trim() });
        };
        item.addEventListener("click", activate);
        item.addEventListener("keydown", event => {
          if (event.key === "Enter" || event.key === " ") { event.preventDefault(); activate(); }
        });
      });
    }
    if (name === "card" && el.classList.contains("roya-card--clickable")) {
      el.setAttribute("tabindex", el.getAttribute("tabindex") || "0");
      el.addEventListener("click", () => emit(el, "card:click"));
      el.addEventListener("keydown", e => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); emit(el, "card:click"); } });
    }
    if (name === "chip" && el.dataset.clickable === "true") {
      el.addEventListener("click", () => {
        const selected = !el.classList.contains("is-selected");
        el.classList.toggle("is-selected", selected);
        el.setAttribute("aria-pressed", String(selected));
        emit(el, selected ? "chip:select" : "chip:deselect", { selected });
        emit(el, "chip:click", { selected });
      });
      el.addEventListener("keydown", event => {
        if (event.key === "Enter" || event.key === " ") { event.preventDefault(); el.click(); }
      });
    }
    if (name === "navigation_bar" || name === "navigation_rail") {
      const items = all("[data-roya-nav-item]");
      items.forEach((item, index) => item.addEventListener("click", () => {
        setActive(items, item);
        emit(el, "navigation:change", { index, value: item.dataset.value || item.textContent.trim() });
        emit(el, "navigation:select", { index, value: item.dataset.value || item.textContent.trim() });
      }));
    }
    if (name === "navigation_drawer") {
      const close = () => { el.hidden = true; emit(el, "drawer:close"); };
      all("[data-roya-drawer-close]").forEach(b => b.addEventListener("click", close));
      all("[data-roya-drawer-item]").forEach((item, index) => item.addEventListener("click", () => {
        all("[data-roya-drawer-item]").forEach(n => n.classList.remove("is-active"));
        item.classList.add("is-active");
        emit(el, "drawer:item-select", { index, value: item.dataset.value || item.textContent.trim() });
        if (el.dataset.autoClose === "true") close();
      }));
      el.addEventListener("keydown", event => { if (event.key === "Escape") close(); });
      if (el.dataset.open === "true") { el.hidden = false; emit(el, "drawer:open"); }
    }
    if (name === "bottom_sheet") {
      const panel = q(".roya-bottom-sheet__panel");
      const handle = q(".roya-bottom-sheet__handle");
      if (handle && panel) {
        let startY = null;
        handle.style.touchAction = "none";
        handle.addEventListener("pointerdown", event => {
          startY = event.clientY;
          if (handle.setPointerCapture) handle.setPointerCapture(event.pointerId);
        });
        handle.addEventListener("pointerup", event => {
          if (startY !== null && event.clientY - startY > 80 && el.dataset.dismissible !== "false") {
            el.classList.remove("is-open");
            el.hidden = true;
            emit(el, "bottom-sheet:close", { reason: "swipe" });
          }
          startY = null;
        });
        handle.addEventListener("pointercancel", () => { startY = null; });
      }
      el.addEventListener("keydown", event => {
        if (event.key === "Escape" && el.dataset.dismissible !== "false" && el.dataset.closeOnEscape !== "false") {
          el.classList.remove("is-open"); el.hidden = true;
        }
      });
    }
    if (name === "dialog") {
      const close = (reason) => {
        if (el.dataset.dismissible !== "false" && el.dataset.persistent !== "true" &&
            (reason !== "outside" || el.dataset.closeOnOutside !== "false")) {
          el.hidden = true; emit(el, "dialog:close");
        }
      };
      const backdrop = q(".roya-dialog__backdrop");
      if (backdrop) backdrop.addEventListener("click", () => close("outside"));
      all("[data-roya-dialog-close]").forEach(button => button.addEventListener("click", () => close("button")));
      el.addEventListener("keydown", e => { if (e.key === "Escape" && el.dataset.closeOnEscape !== "false") close("escape"); });
      if (!el.hidden) { document.body.dataset.royaDialogOpen = "true"; }
      const observer = new MutationObserver(() => {
        if (el.hidden) delete document.body.dataset.royaDialogOpen;
        else document.body.dataset.royaDialogOpen = "true";
      });
      observer.observe(el, { attributes: true, attributeFilter: ["hidden"] });
    }
    if (name === "appbar") {
      const navBtn = q("[data-roya-appbar-nav]");
      if (navBtn) {
        navBtn.addEventListener("click", () => {
          const isOpen = el.dataset.menuOpen === "true";
          const next = !isOpen;
          el.dataset.menuOpen = String(next);
          emit(el, next ? "appbar:menu-open" : "appbar:menu-close", { icon: (navBtn.textContent || "").trim() });
          emit(el, "appbar:action", { action: "nav", open: next });
        });
      }
      all("[data-roya-appbar-action]").forEach((btn) => {
        btn.addEventListener("click", () => {
          emit(el, "appbar:action", { icon: btn.dataset.icon, action: btn.dataset.icon });
        });
      });
    }
    if (name === "tooltip") {
      const trigger = q("[data-roya-tooltip-trigger]");
      if (trigger) {
        const show = () => { el.classList.add("is-visible"); emit(el, "tooltip:show"); };
        const hide = () => { el.classList.remove("is-visible"); emit(el, "tooltip:hide"); };
        if (el.dataset.trigger === "click") trigger.addEventListener("click", () => el.classList.contains("is-visible") ? hide() : show());
        else if (el.dataset.trigger === "focus") {
          trigger.addEventListener("focus", show); trigger.addEventListener("blur", hide);
        } else if (el.dataset.trigger !== "manual") {
          trigger.addEventListener("pointerenter", show); trigger.addEventListener("pointerleave", hide);
          trigger.addEventListener("focus", show); trigger.addEventListener("blur", hide);
          trigger.addEventListener("click", () => el.classList.contains("is-visible") ? hide() : show());
        }
      }
    }
  };

  // Public helpers for controlled overlays. Can be called by application code.
  R.open = function (id) {
    const el = document.getElementById(id);
    if (!el) return false;
    el.hidden = false;
    if (el.dataset.royaComponent === "bottom_sheet") requestAnimationFrame(() => el.classList.add("is-open"));
    if (el.dataset.royaComponent === "dialog") document.body.dataset.royaDialogOpen = "true";
    R.emit((el.dataset.royaComponent || "component") + ":open", { id });
    return true;
  };
  R.close = function (id) {
    const el = document.getElementById(id);
    if (!el) return false;
    el.classList.remove("is-open");
    el.hidden = true;
    if (el.dataset.royaComponent === "dialog") delete document.body.dataset.royaDialogOpen;
    R.emit((el.dataset.royaComponent || "component") + ":close", { id });
    return true;
  };
  document.addEventListener("click", (event) => {
    const trigger = event.target.closest("[data-roya-open]");
    if (trigger) {
      event.preventDefault();
      R.open(trigger.dataset.royaOpen);
    }
  });

  // Mount components added after the initial page load (HTMX, partial updates, etc.).
  if (global.MutationObserver && document.body) {
    const observer = new MutationObserver(records => records.forEach(record =>
      record.addedNodes.forEach(node => {
        if (node.nodeType === 1) {
          if (node.matches && node.matches("[data-roya-component]")) R.mount(node.parentNode || document);
          else R.mount(node);
        }
      })
    ));
    observer.observe(document.body, { childList: true, subtree: true });
  }
})(window);