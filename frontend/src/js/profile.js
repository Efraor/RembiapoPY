import { apiFetch } from "./api.js";

function setMsg(text) {
  const el = document.getElementById("msg");
  if (el) el.textContent = text || "";
}

async function fetchMe() {
  const { res, data } = await apiFetch("/me", { method: "GET" });
  if (!res.ok) return null;
  return data;
}

async function fetchProfile() {
  const { res, data } = await apiFetch("/profile", { method: "GET" });
  if (!res.ok) return null;
  return data.profile || null;
}

function readForm() {
  return {
    full_name: document.getElementById("fullName")?.value || "",
    role: document.getElementById("role")?.value || "user",
    category: document.getElementById("category")?.value || "",
    service_title: document.getElementById("serviceTitle")?.value || "",
    phone: document.getElementById("phone")?.value || "",
    whatsapp: document.getElementById("whatsapp")?.value || "",
    email: document.getElementById("email")?.value || "",
    city: document.getElementById("city")?.value || "",
    bio: document.getElementById("bio")?.value || "",
    photo_url: document.getElementById("photoUrl")?.value || "",
  };
}

function fillForm(profile, me) {
  if (me?.email && document.getElementById("email")) {
    document.getElementById("email").value = profile?.email || me.email || "";
  }
  if (profile?.full_name && document.getElementById("fullName")) {
    document.getElementById("fullName").value = profile.full_name;
  }
  if (profile?.role && document.getElementById("role")) {
    document.getElementById("role").value = profile.role;
  }
  if (profile?.category && document.getElementById("category")) {
    document.getElementById("category").value = profile.category;
  }
  if (profile?.service_title && document.getElementById("serviceTitle")) {
    document.getElementById("serviceTitle").value = profile.service_title;
  }
  if (profile?.phone && document.getElementById("phone")) {
    document.getElementById("phone").value = profile.phone;
  }
  if (profile?.whatsapp && document.getElementById("whatsapp")) {
    document.getElementById("whatsapp").value = profile.whatsapp;
  }
  if (profile?.city && document.getElementById("city")) {
    document.getElementById("city").value = profile.city;
  }
  if (profile?.bio && document.getElementById("bio")) {
    document.getElementById("bio").value = profile.bio;
  }
  if (profile?.photo_url && document.getElementById("photoUrl")) {
    document.getElementById("photoUrl").value = profile.photo_url;
  }
}

function toggleProFields() {
  const role = document.getElementById("role")?.value || "user";
  const proSection = document.getElementById("proFields");
  if (!proSection) return;
  proSection.style.display = role === "pro" ? "block" : "none";
}

async function saveProfile(payload) {
  // Guarda perfil (POST /api/profile)
  const { res, data } = await apiFetch("/profile", {
    method: "POST",
    body: payload,
  });
  if (!res.ok) {
    setMsg(data.error || "No se pudo guardar el perfil.");
    return null;
  }
  return data.profile;
}

export async function initCreateProfilePage() {
  setMsg("");

  const me = await fetchMe();
  const profile = await fetchProfile();
  fillForm(profile, me);

  const pendingRole = localStorage.getItem("pendingRole");
  if (pendingRole && document.getElementById("role")) {
    document.getElementById("role").value = pendingRole;
    toggleProFields();
  }

  document.getElementById("role")?.addEventListener("change", toggleProFields);
  toggleProFields();

  document.getElementById("btnSaveProfile")?.addEventListener("click", async () => {
    const payload = readForm();
    const saved = await saveProfile(payload);
    if (!saved) return;

    localStorage.removeItem("pendingRole");

    await apiFetch("/auth/logout", { method: "POST" });
    window.location.href = "login.html";
  });
}

export async function initEditProfilePage() {
  setMsg("");

  const me = await fetchMe();
  const profile = await fetchProfile();
  fillForm(profile, me);

  // Modo lectura -> editar (toggling en UI)
  document.getElementById("role")?.addEventListener("change", toggleProFields);
  toggleProFields();

  document.getElementById("btnSaveProfile")?.addEventListener("click", async () => {
    const payload = readForm();
    const saved = await saveProfile(payload);
    if (!saved) return;

    setMsg("Perfil actualizado.");
  });
}

export async function initPublishPage() {
  setMsg("");

  const me = await fetchMe();
  const profile = await fetchProfile();
  fillForm(profile, me);

  if (document.getElementById("role")) {
    document.getElementById("role").value = "pro";
  }
  toggleProFields();

  document.getElementById("btnPublish")?.addEventListener("click", async () => {
    const payload = readForm();
    payload.role = "pro";

    const saved = await saveProfile(payload);
    if (!saved) return;

    const category = (payload.category || "electricistas").toLowerCase();
    window.location.href = `${category}.html`;
  });
}
