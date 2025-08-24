const img = document.getElementById("cat-img");
const statusEl = document.getElementById("status");
const btn = document.getElementById("btn-new");
const auto = document.getElementById("auto-refresh");

let timer = null;

async function fetchCat() {
  try {
    statusEl.textContent = "Loading…";
    const res = await fetch("/api/cat", { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to load cat");
    const data = await res.json();
    const url = data.url;
    // Preload then swap
    const pre = new Image();
    pre.onload = () => {
      img.src = url;
      statusEl.textContent = "Meow ✨";
    };
    pre.onerror = () => {
      statusEl.textContent = "Failed to load image";
    };
    pre.src = url;
  } catch (e) {
    statusEl.textContent = "Error: " + e.message;
  }
}

function setAutoRefresh(enabled) {
  if (timer) { clearInterval(timer); timer = null; }
  if (enabled) {
    timer = setInterval(fetchCat, 10000);
  }
}

btn.addEventListener("click", fetchCat);
auto.addEventListener("change", (e) => setAutoRefresh(e.target.checked));

// Initial load
fetchCat();
