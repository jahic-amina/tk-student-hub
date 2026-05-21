const BASE_URL = 'http://127.0.0.1:8000'

async function parseResponse(response) {
  if (!response.ok) {
    const message = await response.text()
    throw new Error(message || `Request failed with status ${response.status}`)
  }

  return response.json()
}

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

export async function registerCompany(data) {
  console.log(data)
  const response = await fetch(`${BASE_URL}/companies/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  })
  return response
}

export async function getPublicAds() {
  const response = await fetch(`${BASE_URL}/public-ads/`)
  return parseResponse(response)
}

export async function getApprovedCompanies() {
  const response = await fetch(`${BASE_URL}/companies/`)
  return parseResponse(response)
}