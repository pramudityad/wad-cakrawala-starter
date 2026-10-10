const BASE_URL = 'http://localhost:8000'

function formatDetail(detail) {
  if (typeof detail === 'string') return detail
  if (Array.isArray(detail)) {
    return detail.map((e) => `${e.loc?.at(-1) ?? 'field'}: ${e.msg}`).join('; ')
  }
  return 'Terjadi kesalahan yang tidak diketahui.'
}

async function request(path, options = {}) {
  const res = await fetch(`${BASE_URL}${path}`, options)
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
