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
