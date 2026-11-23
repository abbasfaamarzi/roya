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
          if (el.dataset.dismissible !== "false") {
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