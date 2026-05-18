const BASE_URL = 'http://127.0.0.1:8000'

function getHeaders() {
  const token = localStorage.getItem('token') || localStorage.getItem('access_token')
  const headers = { 'Content-Type': 'application/json' }
  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }
  return headers
}

export async function getCategories() {
  const response = await fetch(`${BASE_URL}/forum/categories`, {
    headers: getHeaders()
  })
  return response.json()
}

