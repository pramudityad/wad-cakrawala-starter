const BASE_URL = 'http://localhost:8000'

function formatDetail(detail) {
  if (typeof detail === 'string') return detail
  if (Array.isArray(detail)) {
    return detail.map((e) => `${e.loc?.at(-1) ?? 'field'}: ${e.msg}`).join('; ')
  }
  return 'Terjadi kesalahan yang tidak diketahui.'
}

let onUnauthorized = () => {}
export function setUnauthorizedHandler(fn) {
  onUnauthorized = fn
}

async function request(path, options = {}) {
  // credentials: cookie httpOnly dikirim browser; JS tidak pernah memegang token
  const res = await fetch(`${BASE_URL}${path}`, { credentials: 'include', ...options })
  if (res.status === 401 && !path.startsWith('/auth/login')) onUnauthorized()
  if (!res.ok) {
    const body = await res.json().catch(() => null)
    throw new Error(body ? formatDetail(body.detail) : res.statusText)
  }
  if (res.status === 204) return null
  return res.json()
}

export function listSessions(search = '', signal) {
  const query = search ? `?search=${encodeURIComponent(search)}` : ''
  return request(`/sessions${query}`, { signal })
}

export function createSession(payload) {
  return request('/sessions', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
}

export function deleteSession(id) {
  return request(`/sessions/${id}`, { method: 'DELETE' })
}

const json = (method, body) => ({
  method,
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(body),
})

export const register = (email, password) => request('/auth/register', json('POST', { email, password }))
export const login = (email, password) => request('/auth/login', json('POST', { email, password }))
export const logout = () => request('/auth/logout', { method: 'POST' })
export const me = () => request('/auth/me')

export const registerFor = (sessionId) =>
  request(`/sessions/${sessionId}/registrations`, { method: 'POST' })
export const cancelRegistration = (id) => request(`/registrations/${id}`, { method: 'DELETE' })
