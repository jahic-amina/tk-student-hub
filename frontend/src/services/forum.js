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
  if (!response.ok) throw new Error('Greška pri dohvatanju kategorija')
  return response.json()
}


export async function getTopics({ category_id = null, search = "", page = 1, per_page = 5 } = {}) {
  // Pravimo dinamičke query parametre za URL
  let queryParams = new URLSearchParams({
    page: page.toString(),
    per_page: per_page.toString()
  })

  if (category_id !== null) {
    queryParams.append('category_id', category_id.toString())
  }

  if (search && search.trim()) {
    queryParams.append('search', search.trim())
  }

  const response = await fetch(`${BASE_URL}/forum/topics?${queryParams.toString()}`, {
    headers: getHeaders()
  })

  if (!response.ok) throw new Error('Greška pri dohvatanju tema')
  return response.json() // Vraća objekat: { items: [...], total: X, page: Y, per_page: Z }
}


export async function getTopicById(id) {
  const response = await fetch(`${BASE_URL}/forum/topics/${id}`, {
    headers: getHeaders()
  })
  if (!response.ok) throw new Error('Detalji teme se ne mogu učitati')
  return response.json()
}


export async function incrementTopicView(id) {
  const response = await fetch(`${BASE_URL}/forum/topics/${id}/view`, {
    method: 'PATCH',
    headers: getHeaders()
  })
  if (!response.ok) throw new Error('Broj pregleda se ne može ažurirati')
  return response.json()
}


export async function deleteTopic(topicId) {
  const response = await fetch(`${BASE_URL}/forum/topics/${topicId}`, {
    method: 'DELETE',
    headers: getHeaders()
  })

  if (!response.ok) {
    const errorData = await response.json().catch(() => null)
    throw new Error(errorData?.detail || 'Brisanje teme nije uspjelo.')
  }
  return response.json()
}


export async function createTopic(topicData) {
  // topicData format: { title: '...', content: '...', category_id: X, tags: [...] }
  const response = await fetch(`${BASE_URL}/forum/topics`, {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify(topicData)
  })
  if (!response.ok) throw new Error('Kreiranje teme nije uspjelo.')
  return response.json()
}


export async function createComment(commentData) {
  // commentData format: { topic_id: X, content: '...' }
  const response = await fetch(`${BASE_URL}/forum/comments`, {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify(commentData)
  })
  if (!response.ok) throw new Error('Slanje komentara nije uspjelo.')
  return response.json()
}


export default {
  getCategories,
  getTopics,
  getTopicById,
  incrementTopicView,
  deleteTopic,
  createTopic,
  createComment
}