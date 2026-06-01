const BASE_URL = 'http://127.0.0.1:8000'

export async function registerUser(email, fullName, password) {
  const response = await fetch(`${BASE_URL}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, full_name: fullName, password })
  })
  return response.json()
}

export async function loginUser(email, password) {
  const formData = new FormData()
  formData.append('username', email)
  formData.append('password', password)

  const response = await fetch(`${BASE_URL}/auth/login`, {
    method: 'POST',
    body: formData
  })
  return response.json()
}

export async function getMe(token) {
  const response = await fetch(`${BASE_URL}/me`, {
    headers: { 'Authorization': `Bearer ${token}` }
  })
  return response.json()
}

export async function getMyProfile(token) {
  const response = await fetch(`${BASE_URL}/profiles/me`, {
    headers: { 'Authorization': `Bearer ${token}` }
  })
  return response.json()
}

export async function uploadAvatar(token, file) {
  const formData = new FormData()
  formData.append('file', file)

  const response = await fetch(`${BASE_URL}/profiles/me/avatar`, {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${token}` },
    body: formData
  })
  return response.json()
}

export async function removeAvatar(token) {
  const response = await fetch(`${BASE_URL}/profiles/me/avatar`, {
    method: 'DELETE',
    headers: { 'Authorization': `Bearer ${token}` }
  })
  return response.json()
}
export async function getAllUsers(token, { search = '', role = '', is_active = '' } = {}) {
  const params = new URLSearchParams()
  if (search) params.append('search', search)
  if (role) params.append('role', role)
  if (is_active !== '') params.append('is_active', is_active)

  const response = await fetch(`${BASE_URL}/admin/users?${params.toString()}`, {
    headers: { 'Authorization': `Bearer ${token}` }
  })
  return response.json()
}