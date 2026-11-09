/* Aviso de cookies + Microsoft Clarity.
   Clarity solo se carga si la persona acepta. La elección se guarda en localStorage ("pa_consent").
   Cualquier enlace con el atributo data-cookies vuelve a abrir el aviso. */
(function () {
  var CLARITY_ID = "z9unz2wa1b";
  var KEY = "pa_consent";

  function get() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function set(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }

  var loaded = false;
  function loadClarity() {
    if (loaded) return; loaded = true;
    (function (c, l, a, r, i, t, y) {
      c[a] = c[a] || function () { (c[a].q = c[a].q || []).push(arguments); };
      t = l.createElement(r); t.async = 1; t.src = "https://www.clarity.ms/tag/" + i;
      y = l.getElementsByTagName(r)[0]; y.parentNode.insertBefore(t, y);
    })(window, document, "clarity", "script", CLARITY_ID);
    window.clarity("consentv2", { ad_Storage: "denied", analytics_Storage: "granted" });
  }

  var css =
    ".pa-ck{position:fixed;left:12px;right:12px;bottom:calc(12px + env(safe-area-inset-bottom,0px));z-index:9999;max-width:520px;margin:0 auto;" +
    "display:flex;align-items:center;gap:12px;flex-wrap:wrap;background:#2f5a43;color:#f5f1e4;border-radius:16px;" +
    "padding:12px 14px 12px 16px;box-shadow:0 8px 24px rgba(0,0,0,.18);font:500 13px/1.45 Montserrat,system-ui,sans-serif}" +
    ".pa-ck p{margin:0;flex:1 1 200px}.pa-ck a{color:inherit;font-weight:600;text-decoration:underline}" +
    ".pa-ck .b{display:flex;gap:8px;flex:none;margin-left:auto}" +
    ".pa-ck button{min-height:34px;padding:0 14px;border-radius:999px;cursor:pointer;font:700 12.5px Montserrat,system-ui,sans-serif;" +
    "border:1px solid rgba(245,241,228,.55);background:transparent;color:#f5f1e4}" +
    ".pa-ck button:hover{background:rgba(245,241,228,.12)}";

  // Textos según el idioma de la página (la home puede estar en castellano, catalán o inglés)
  var TXT = {
    es: ["Usamos cookies de analítica (Microsoft Clarity) para mejorar la web.", "Más info", "Rechazar", "Aceptar"],
    ca: ["Fem servir galetes d'analítica (Microsoft Clarity) per millorar la web.", "Més info", "Rebutjar", "Acceptar"],
    en: ["We use analytics cookies (Microsoft Clarity) to improve the site.", "More info", "Reject", "Accept"]
  };

  var box;
  function show() {
    if (box) return;
    if (!document.getElementById("pa-ck-css")) {
      var s = document.createElement("style"); s.id = "pa-ck-css"; s.textContent = css;
      document.head.appendChild(s);
    }
    box = document.createElement("div");
    box.className = "pa-ck"; box.setAttribute("role", "dialog"); box.setAttribute("aria-label", "Cookies");
    var t = TXT[document.documentElement.lang] || TXT.es;
    box.innerHTML =
      "<p>" + t[0] + " <a href=\"/privacy.html#cookies\">" + t[1] + "</a></p>" +
      "<div class=\"b\"><button type=\"button\" class=\"n\">" + t[2] + "</button><button type=\"button\" class=\"y\">" + t[3] + "</button></div>";
    box.querySelector(".y").onclick = function () { set("yes"); hide(); loadClarity(); };
    box.querySelector(".n").onclick = function () {
      var was = get() === "yes"; set("no"); hide();
      if (was) location.reload(); // si retira el consentimiento, recargamos para descargar Clarity
    };
    document.body.appendChild(box);
  }
  function hide() { if (box) { box.remove(); box = null; } }

  function init() {
    var c = get();
    if (c === "yes") loadClarity();
    else if (c !== "no") show();
    // si cambian el idioma con el aviso abierto, se vuelve a pintar en el idioma nuevo
    document.addEventListener("pa:lang", function () { if (box) { hide(); show(); } });
    document.addEventListener("click", function (e) {
      var a = e.target.closest && e.target.closest("[data-cookies]");
      if (a) { e.preventDefault(); show(); }
    });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
