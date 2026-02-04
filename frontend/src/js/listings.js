import { apiFetch } from "./api.js";

function profileImage(profile, fallback) {
  return profile.photo_url || fallback || "https://randomuser.me/api/portraits/lego/1.jpg";
}

function contactLine(profile) {
  const phone = profile.whatsapp || profile.phone || "";
  const email = profile.email || "";
  const parts = [];
  if (phone) parts.push(`<i class="bi bi-whatsapp"></i> ${phone}`);
  if (email) parts.push(`<i class="bi bi-envelope"></i> ${email}`);
  return parts.join(" · ");
}

function renderProfileCard(profile, fallbackImg) {
  const phone = profile.whatsapp || profile.phone || "";
  const email = profile.email || "";
  const contactText = contactLine(profile);
  const telHref = phone ? `tel:${phone.replace(/\\s+/g, "")}` : "#";

  return `
    <div class="col-12 col-md-6 col-lg-4 mb-4">
      <div class="pro-card">
        <img src="${profileImage(profile, fallbackImg)}" alt="${profile.full_name || "Perfil"}">
        <div class="pro-card-body text-center">
          <h6 class="mb-1">${profile.full_name || "Profesional"}</h6>
          <small class="text-muted">${profile.service_title || "Servicio profesional"}</small>
          <div class="my-2">
            <i class="bi bi-star-fill text-warning"></i>
            <small>4.8</small>
          </div>
          <a class="btn btn-success btn-sm" href="${telHref}">Contactar</a>
          <div class="mt-2">
            <small class="text-muted">${contactText || "Contacto disponible"}</small>
          </div>
        </div>
      </div>
    </div>
  `;
}

async function fetchProfiles(category, limit = 10) {
  const { res, data } = await apiFetch(
    `/profiles?category=${encodeURIComponent(category)}&limit=${limit}`,
    { method: "GET" }
  );
  if (!res.ok) return [];
  return data.profiles || [];
}

export async function initCategoryList({ category, containerId, fallback }) {
  const container = document.getElementById(containerId);
  if (!container) return;

  const profiles = await fetchProfiles(category, 20);
  const list = [...profiles];

  if (list.length < 2 && Array.isArray(fallback)) {
    fallback.slice(0, 2 - list.length).forEach((p) => list.push(p));
  }

  container.innerHTML = list
    .map((p, idx) => renderProfileCard(p, fallback?.[idx]?.photo_url))
    .join("");
}

export async function initHomeList({ containerId, limit = 4, fallback = [] }) {
  const container = document.getElementById(containerId);
  if (!container) return;

  const { res, data } = await apiFetch(`/profiles?limit=${limit}`, { method: "GET" });
  if (!res.ok) return;

  const profiles = data.profiles || [];
  const list = [...profiles];
  if (list.length < limit && Array.isArray(fallback)) {
    fallback.slice(0, limit - list.length).forEach((p) => list.push(p));
  }
  container.innerHTML = list.map((p, idx) => renderProfileCard(p, fallback?.[idx]?.photo_url)).join("");
}

function normalizeCategory(value) {
  return (value || "")
    .toString()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .trim()
    .toLowerCase();
}

function resolveCategoryPage(value) {
  // Mapa de entradas -> pagina destino
  const key = normalizeCategory(value);
  const map = {
    electricidad: "electricistas.html",
    electricista: "electricistas.html",
    electricistas: "electricistas.html",
    electrico: "electricistas.html",
    electricos: "electricistas.html",
    plomeria: "plomeros.html",
    plomero: "plomeros.html",
    plomeros: "plomeros.html",
    fontanero: "plomeros.html",
    fontaneros: "plomeros.html",
    sanitario: "plomeros.html",
    mecanico: "mecanicos.html",
    mecanicos: "mecanicos.html",
    tecnico: "tecnicos.html",
    tecnicos: "tecnicos.html",
    "tecnico it": "tecnicos.html",
    limpieza: "limpieza.html",
    carpinteria: "carpinteria.html",
    flete: "flete.html",
  };
  return map[key] || null;
}

function categoryCard(name) {
  const page = resolveCategoryPage(name);
  const label = name || "Categoria";
  const href = page || "#";
  const icon = "🛠️";
  return `
    <div class="col-6 col-md-3 mb-3">
      <div class="category-card p-3 text-center">
        <div class="category-icon mb-2">${icon}</div>
        <h6 class="mb-1">
          ${page ? `<a href="${href}">${label}</a>` : label}
        </h6>
      </div>
    </div>
  `;
}

function buildCategoryIndex(categories) {
  return categories.map((name) => ({
    name,
    key: normalizeCategory(name),
  }));
}

function findBestCategoryMatch(inputValue, categoriesIndex) {
  const inputKey = normalizeCategory(inputValue);
  if (!inputKey) return null;

  // Exact match first
  const exact = categoriesIndex.find((c) => c.key === inputKey);
  if (exact) return exact;

  // Prefix match (user typed beginning)
  const prefix = categoriesIndex.find((c) => c.key.startsWith(inputKey));
  if (prefix) return prefix;

  // Contains match
  const contains = categoriesIndex.find((c) => c.key.includes(inputKey));
  if (contains) return contains;

  return null;
}

export async function initCategorySearch({ inputId, datalistId, buttonId }) {
  const input = document.getElementById(inputId);
  const datalist = document.getElementById(datalistId);
  if (!input || !datalist) return;

  const { res, data } = await apiFetch("/categories", { method: "GET" });
  if (!res.ok) return;

  const categories = data.categories || [];
  const categoriesIndex = buildCategoryIndex(categories);
  datalist.innerHTML = categories.map((name) => `<option value="${name}"></option>`).join("");

  const goToCategory = () => {
    const match = findBestCategoryMatch(input.value, categoriesIndex);
    if (match) {
      input.value = match.name;
    }
    const page = resolveCategoryPage(match?.name || input.value);
    if (page) {
      window.location.href = page;
    }
  };

  input.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      event.preventDefault();
      goToCategory();
    }
  });

  input.addEventListener("blur", () => {
    const match = findBestCategoryMatch(input.value, categoriesIndex);
    if (match) {
      input.value = match.name;
    }
  });

  if (buttonId) {
    const button = document.getElementById(buttonId);
    button?.addEventListener("click", goToCategory);
  }
}

export async function initCategoriesPage({ containerId }) {
  const container = document.getElementById(containerId);
  if (!container) return;

  const { res, data } = await apiFetch("/categories", { method: "GET" });
  if (!res.ok) return;

  const categories = data.categories || [];
  container.innerHTML = categories.map((name) => categoryCard(name)).join("");
}
