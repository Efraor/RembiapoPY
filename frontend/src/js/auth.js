// Auth page logic: local login/register and Google identity flow.
// Maneja el login del usuario (Google y formulario)

import { apiFetch } from "./api.js";

function showMsg(text) {

    // Muestra mensajes de error o estado en pantalla

  document.getElementById("msg").textContent = text || "";
}

function setToken(token) {
  if (token) {
    localStorage.setItem("token", token);
  }
}

// Login local (email + password)

async function handleLogin() {
  showMsg("");

  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  const { res, data } = await apiFetch("/users/login", {
    method: "POST",
    body: { email, password },
  });

  if (!res.ok) {
    showMsg(data.error || "No se pudo iniciar sesión.");
    return;
  }

  setToken(data.token);
  window.location.href = "menu_basico.html";
}

// Registro local (email + password)

async function handleRegister() {
  showMsg("");

  const name = document.getElementById("regName")?.value || "";
  const email = document.getElementById("regEmail")?.value || "";
  const role = document.getElementById("regRole")?.value || "user";
  const password = document.getElementById("regPassword")?.value || "";

  const { res, data } = await apiFetch("/users/register", {
    method: "POST",
    body: { name, email, role, password },
  });

  if (!res.ok) {
    showMsg(data.error || "No se pudo registrar.");
    return;
  }

  setToken(data.token);
  localStorage.setItem("pendingRole", role);
  window.location.href = "crear_perfil.html";
}


// Login con Google


async function handleGoogleCredential(response) {

    // Envía el token de Google al backend para validación

  showMsg("");

  const { res, data } = await apiFetch("/auth/google", {
    method: "POST",
    body: { credential: response.credential },
  });

  if (!res.ok) {
    showMsg(data.error || "Google login falló.");
    return;
  }

  setToken(data.token);
  window.location.href = "menu_basico.html";
}

function initGoogleButton() {
  const GOOGLE_CLIENT_ID =
    "877002585907-ne7tte3vil46lrasqmj4np2kqq4l8t4l.apps.googleusercontent.com";

  if (!window.google?.accounts?.id) {
    showMsg("No cargó Google Identity Services. Revisá conexión o el script.");
    return;
  }

  window.google.accounts.id.initialize({
    client_id: GOOGLE_CLIENT_ID,
    callback: handleGoogleCredential,
  });

  window.google.accounts.id.renderButton(
    document.getElementById("googleBtn"),
    { theme: "outline", size: "large", width: 360 }
  );
}

// Init page

export function initLoginPage() {

    // Inicializa botones y eventos del login

    // Botones login / register

  document.getElementById("btnLogin")?.addEventListener("click", handleLogin);
  document.getElementById("btnRegister")?.addEventListener("click", () => {
    window.location.href = "register.html";
  });

  // Google Identity Services
  initGoogleButton();
}

export function initRegisterPage() {
  document.getElementById("btnDoRegister")?.addEventListener("click", handleRegister);
  initGoogleButton();
}