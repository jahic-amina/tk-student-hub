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

export async function getTopics(categoryId = null, page = 1, size = 5) {
  let url = `http://127.0.0.1:8000/forum/topics?page=${page}&size=${size}`;
  
  if (categoryId !== null) {
    url += `&category_id=${categoryId}`;
  }

  const response = await fetch(url, {
    headers: getHeaders()
  });
  
  if (!response.ok) {
    throw new Error('Greška pri dohvatanju tema');
  }
  
  return response.json(); // Ovo sada vraća objekat sa { items, total, page, size }
}