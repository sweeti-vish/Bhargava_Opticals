// ---------- Shop data (edit here) ----------
const SERVICES = [
  {name:"Eye Testing", desc:"Eye check-up facility available at the shop. Know your power before you buy."},
  {name:"Frames", desc:"Wide range of spectacle frames for men, women and kids."},
  {name:"Sunglasses", desc:"Polarised and branded sunglasses for sun and style."},
  {name:"Contact Lenses", desc:"Contact lenses from trusted brands, with guidance on use and care."},
  {name:"Lenses & Coatings", desc:"Quality spectacle lenses, including clear-vision coatings."},
  {name:"Hearing Machines", desc:"कान की मशीन यहाँ मिलती है. Hearing machines are available at the shop."}
];
const BRANDS = ["Polo Ralph Lauren","Polaroid","Bausch + Lomb","Ray-Ban","Crizal","Yash Optics & Lens"];
const LOCATIONS = [
  {name:"Chandni Chowk, Sironj (M.P.)", info:"Shop 1"},
  {name:"Chhipeti Bazar, Sironj (M.P.)", info:"Shop 2"},
  {name:"6264036246", info:"Phone / WhatsApp"},
  {name:"7477016198", info:"Phone"}
];
// Sample timings: replace with real ones. days: 0 = Sunday
const HOURS = {open:10, close:20, closedDay:0};


// ---------- Helpers ----------
const $ = (s, el=document) => el.querySelector(s);
const esc = t => t.replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));

// ---------- Render ----------

$("#svcGrid").innerHTML = SERVICES.map(s =>
  `<article class="svc" data-name="${esc(s.name)}"><h3>${esc(s.name)}</h3><p>${esc(s.desc)}</p></article>`).join("");
$("#yr").textContent = new Date().getFullYear();

// ---------- Open / closed status ----------
(function(){
  const now = new Date(), h = now.getHours(), el = $("#openStatus");
  const open = now.getDay() !== HOURS.closedDay && h >= HOURS.open && h < HOURS.close;
  el.textContent = open ? "Open now" : "Closed now";
  el.classList.add(open ? "open" : "closed");
})();

// ---------- Search with 3 modes ----------
let mode = "all";
const q = $("#q"), list = $("#results"), chip = $("#modeChip");
const labels = {all:"All", service:"Services", brand:"Brands", location:"Locations"};

function index(){
  const rows = [];
  if (mode==="all"||mode==="service") SERVICES.forEach(s => rows.push({t:s.name, k:"Service", href:"#services", svc:s.name}));
  if (mode==="all"||mode==="brand")   BRANDS.forEach(b => rows.push({t:b, k:"Brand", href:"#dashboard"}));
  if (mode==="all"||mode==="location") LOCATIONS.forEach(l => rows.push({t:l.name, k:l.info, href:"#dashboard"}));
  return rows;
}
function search(){
  const term = q.value.trim().toLowerCase();
  if (!term){ list.hidden = true; return; }
  const hits = index().filter(r => r.t.toLowerCase().includes(term));
  list.innerHTML = hits.length
    ? hits.map(r => `<li><a href="${r.href}" ${r.svc?`data-go="${esc(r.svc)}"`:""}><span>${esc(r.t)}</span><small>${r.k}</small></a></li>`).join("")
    : `<li class="none">No match in ${labels[mode].toLowerCase()}. Try another word.</li>`;
  list.hidden = false;
}
q.addEventListener("input", search);
document.addEventListener("click", e => { if (!e.target.closest(".search")) list.hidden = true; });

// Three-line menu: choose search type
const menuBtn = $("#menuBtn"), drawer = $("#drawer");
menuBtn.addEventListener("click", () => {
  const open = drawer.hidden;
  drawer.hidden = !open;
  menuBtn.setAttribute("aria-expanded", open);
});
drawer.addEventListener("click", e => {
  const b = e.target.closest(".mode");
  if (!b) return;
  mode = b.dataset.mode;
  drawer.querySelectorAll(".mode").forEach(x => x.classList.toggle("active", x === b));
  chip.textContent = labels[mode];
  q.focus(); search();
});
document.addEventListener("keydown", e => { if (e.key === "Escape"){ drawer.hidden = true; list.hidden = true; menuBtn.setAttribute("aria-expanded", false);} });

// Highlight a service card when jumped to from search or quick chips
document.addEventListener("click", e => {
  const a = e.target.closest("[data-go]");
  if (!a) return;
  const card = [...document.querySelectorAll(".svc")].find(c => c.dataset.name === a.dataset.go);
  if (card){ card.classList.add("flash"); setTimeout(() => card.classList.remove("flash"), 1800); }
  list.hidden = true;
});

// Highlight active nav link while scrolling
const links = [...document.querySelectorAll(".top-nav a")];
const io = new IntersectionObserver(entries => entries.forEach(en => {
  if (en.isIntersecting) links.forEach(l => l.classList.toggle("on", l.getAttribute("href") === "#" + en.target.id));
}), {threshold:.4});
document.querySelectorAll(".page").forEach(p => io.observe(p));