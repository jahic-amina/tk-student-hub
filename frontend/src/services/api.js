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

export async function uploadMaterial(formData) {
  const token = localStorage.getItem('token')
  const response = await fetch(`${BASE_URL}/materials/upload`, {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${token}` },
    body: formData
  })
  return response
}
export async function getMaterials() {
  const response = await fetch(`${BASE_URL}/materials`)
  return response.json()
}

export async function getMaterial(id) {
  const response = await fetch(`${BASE_URL}/materials/${id}`)
  return response.json()
}


//amer
export async function deleteMaterial(id) {
  const token = localStorage.getItem('token')
  const response = await fetch(`${BASE_URL}/materials/${id}`, {
    method: 'DELETE',
    headers: { 
      'Authorization': `Bearer ${token}` 
    }
  })
  return response 
}
export async function getSubjects() {
  const res = await fetch('http://127.0.0.1:8000/materials/subjects')
  return res.json()
}

export async function getComments(materialId) {
  const response = await fetch(`${BASE_URL}/materials/${materialId}/comments`)
  return response.json()
}

export async function postComment(materialId, content) {
  const token = localStorage.getItem('token')
  const response = await fetch(`${BASE_URL}/materials/${materialId}/comments`, {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ content, material_id: materialId })
  })
  if (!response.ok) {
      throw new Error('Greška pri slanju komentara.')
  }
  return response.json()
}