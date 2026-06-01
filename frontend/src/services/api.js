const BASE_URL = 'http://127.0.0.1:8000'

async function parseResponse(response) {
  if (!response.ok) {
    const message = await response.text()
    throw new Error(message || `Request failed with status ${response.status}`)
  }
  return response.json()
}

function authHeaders(token) {
  const headers = {
    'Content-Type': 'application/json'
  }

  if (token && token !== 'null' && token !== 'undefined') {
    headers.Authorization = `Bearer ${token}`
  }

  return headers
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

export async function registerCompany(data, logoFile) {
  const formData = new FormData()

  Object.entries(data).forEach(([key, value]) => {
    formData.append(key, value)
  })

  formData.append('logo', logoFile)

  const response = await fetch(`${BASE_URL}/companies/`, {
    method: 'POST',
    body: formData
  })
  return parseResponse(response)
}

export async function uploadCompanyLogo(companyId, file, token) {
  const formData = new FormData()
  formData.append('logo', file)

  const response = await fetch(`${BASE_URL}/companies/${companyId}/upload-logo`, {
    method: 'PATCH',
    headers: { 'Authorization': `Bearer ${token}` },
    body: formData
  })
  return parseResponse(response)
}

export async function getApprovedCompanies() {
  const response = await fetch(`${BASE_URL}/companies/`)
  return parseResponse(response)
}

export async function getAdminCompanies(token) {
  const response = await fetch(`${BASE_URL}/companies/admin`, {
    headers: authHeaders(token)
  })
  return parseResponse(response)
}

export async function updateCompanyStatus(companyId, status, token) {
  const response = await fetch(`${BASE_URL}/companies/${companyId}/status`, {
    method: 'PATCH',
    headers: authHeaders(token),
    body: JSON.stringify(status)
  })
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

export async function deleteCompany(companyId, token) {
  const response = await fetch(`${BASE_URL}/companies/${companyId}`, {
    method: 'DELETE',
    headers: authHeaders(token)
  })
  if (!response.ok) {
    const message = await response.text()
    throw new Error(message || `Request failed with status ${response.status}`)
  }
}

export async function restoreCompany(companyId, token) {
  const response = await fetch(`${BASE_URL}/companies/${companyId}/restore`, {
    method: 'PATCH',
    headers: authHeaders(token)
  })
  return parseResponse(response)
}

export async function getCompanyById(id) {
  const response = await fetch(`${BASE_URL}/companies/${id}`)
  return parseResponse(response)
}
 
export async function getAdsByCompany(companyId) {
  const response = await fetch(`${BASE_URL}/ads/?company_id=${companyId}`)
  return parseResponse(response)
}

// --- Applications ---

export async function uploadFile(file) {
  const formData = new FormData()
  formData.append('file', file)

  const response = await fetch(`${BASE_URL}/applications/upload-cv`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`
    },
    body: formData
  })
  return parseResponse(response)
}

export async function createApplication(applicationData, token) {
  const response = await fetch(`${BASE_URL}/applications/`, {
    method: 'POST',
    headers: authHeaders(token),
    body: JSON.stringify(applicationData)
  })
  return parseResponse(response)
}

export async function getApplicationsByAd(adId, token, isCompany = false) {
  const endpoint = isCompany
    ? `${BASE_URL}/applications/company/by-ad/${adId}`
    : `${BASE_URL}/applications/?ad_id=${adId}`

  if (!token || token === 'null' || token === 'undefined') {
    return []
  }

  const response = await fetch(endpoint, {
    headers: authHeaders(token)
  })
  return parseResponse(response)
}

export async function updateApplicationStatus(applicationId, status, feedback, token, isCompany) {
  const endpoint = isCompany 
    ? `${BASE_URL}/applications/company/${applicationId}`
    : `${BASE_URL}/applications/${applicationId}`
  
  const body = { status }
  if (feedback !== undefined && feedback !== null) {
    body.admin_feedback = feedback
  }

  const response = await fetch(endpoint, {
    method: 'PATCH',
    headers: authHeaders(token),
    body: JSON.stringify(body)
  })
  return parseResponse(response)
}