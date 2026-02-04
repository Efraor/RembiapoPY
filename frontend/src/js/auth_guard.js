// Guard for pages that require an active session.
const API_BASE = "http://127.0.0.1:5000";

async function requireAuth() {
  try {
    // Verifica si hay sesion valida
    const res = await fetch(`${API_BASE}/api/me`, {
      method: "GET",
      credentials: "include",
    });

    if (!res.ok) {
      // No hay sesión válida
      window.location.href = "login.html"; // <-- tu página de login
      return;
    }

    // (Opcional) Si querés usar el usuario en el HTML
    const data = await res.json();
    window.currentUser = data.user || data;
  } catch (e) {
    // Si el backend no está corriendo o hay error de red
    window.location.href = "login.html";
  }
}
