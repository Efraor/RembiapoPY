// API client: wraps fetch and normalizes JSON responses.
// Base de la API (backend Flask)
export const API_BASE = "http://127.0.0.1:5000/api";

export async function apiFetch(path, { method = "GET", body = null } = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    method,
    // Incluye cookies de sesion en todas las peticiones
    credentials: "include",
    headers: { "Content-Type": "application/json" },
    body: body ? JSON.stringify(body) : null,
  });

  const data = await res.json().catch(() => ({}));
  return { res, data };
}
