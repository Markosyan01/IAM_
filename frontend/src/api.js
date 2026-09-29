const KEY = "codelab_token";
export const token = {
  get: () => localStorage.getItem(KEY),
  set: (v) => localStorage.setItem(KEY, v),
  clear: () => localStorage.removeItem(KEY),
};

export async function api(path, { method = "GET", body } = {}) {
  const headers = { "Content-Type": "application/json" };
  const t = token.get();
  if (t) headers.Authorization = `Bearer ${t}`;
  const res = await fetch(`/api${path}`, {
    method, headers, body: body ? JSON.stringify(body) : undefined,
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const err = new Error(data.detail || "generic");
    err.status = res.status;
    throw err;
  }
  return data;
}
