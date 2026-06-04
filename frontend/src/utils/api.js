export const API = 'http://localhost:5000/api'

// Sends an authenticated request. Sets Content-Type and serializes
// body automatically when a body object is provided.
export function apiRequest(url, { method = 'GET', body } = {}) {
  return fetch(`${API}${url}`, {
    method,
    credentials: 'include',
    ...(body
      ? { headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) }
      : {}),
  })
}
