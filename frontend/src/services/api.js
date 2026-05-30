const BASE_URL = 'http://127.0.0.1:8000'

async function parseResponse(response) {
  if (!response.ok) {
    const message = await response.text()
    throw new Error(message || `Request failed with status ${response.status}`)
  }
  return response.json()
}

function authHeaders(token) {
  return {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  }
}

// --- Auth ---

export async function registerUser(email, fullName, password) {
  const response = await fetch(`${BASE_URL}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, full_name: fullName, password })
  })
  return parseResponse(response)
}

export async function loginUser(email, password) {
  const formData = new FormData()
  formData.append('username', email)
  formData.append('password', password)

  const response = await fetch(`${BASE_URL}/auth/login`, {
    method: 'POST',
    body: formData
  })
  return parseResponse(response)
}

export async function loginCompany(email, password) {
  const formData = new FormData()
  formData.append('username', email)
  formData.append('password', password)

  const response = await fetch(`${BASE_URL}/auth/company/login`, {
    method: 'POST',
    body: formData
  })
  return parseResponse(response)
}

// --- Users ---

export async function getMe(token) {
  const response = await fetch(`${BASE_URL}/me`, {
    headers: authHeaders(token)
  })
  return parseResponse(response)
}

// --- Companies ---

export async function registerCompany(data) {
  const response = await fetch(`${BASE_URL}/companies/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  })
  return parseResponse(response)
}

export async function uploadCompanyLogo(companyId, file, token) {
  const formData = new FormData()
  formData.append('logo', file)

  const response = await fetch(`${BASE_URL}/companies/${companyId}/logo`, {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${token}` },
    body: formData
  })
  return parseResponse(response)
}

export async function getApprovedCompanies() {
  const response = await fetch(`${BASE_URL}/companies/`)
  return parseResponse(response)
}

// --- Ads ---

export async function getAds() {
  const response = await fetch(`${BASE_URL}/ads/`)
  return parseResponse(response)
}

export async function getAdById(id) {
  const response = await fetch(`${BASE_URL}/ads/${id}`)
  return parseResponse(response)
}