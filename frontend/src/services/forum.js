const BASE_URL = 'http://127.0.0.1:8000';

// Pomoćna funkcija za dobijanje zaglavlja sa tokenom
function getHeaders() {
  const token = localStorage.getItem('token') || localStorage.getItem('access_token');
  const headers = { 'Content-Type': 'application/json' };
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  return headers;
}

// Centralizovana funkcija za obradu odgovora i izvlačenje grešaka sa backenda
async function handleResponse(response, defaultErrorMessage) {
  if (response.ok) {
    // Ako nema sadržaja (24 No Content), vrati prazan objekat ili true
    if (response.status === 204) return { success: true };
    return response.json();
  }

  // Ako server vrati grešku, pokušaj izvući detaljnu poruku (npr. sa FastAPI-ja: error.detail)
  try {
    const errorData = await response.json();
    throw new Error(errorData?.detail || defaultErrorMessage);
  } catch (e) {
    // U slučaju da odgovor nije JSON, baci podrazumijevanu poruku
    throw new Error(e.message || defaultErrorMessage);
  }
}

export async function getCategories() {
  const response = await fetch(`${BASE_URL}/forum/categories`, {
    headers: getHeaders()
  });
  return handleResponse(response, 'Greška pri dohvatanju kategorija.');
}

export async function getTopics({ category_id = null, search = "", page = 1, per_page = 5 } = {}) {
  let queryParams = new URLSearchParams({
    page: page.toString(),
    per_page: per_page.toString()
  });

  if (category_id !== null) {
    queryParams.append('category_id', category_id.toString());
  }

  if (search && search.trim()) {
    queryParams.append('search', search.trim());
  }

  const response = await fetch(`${BASE_URL}/forum/topics?${queryParams.toString()}`, {
    headers: getHeaders()
  });

  return handleResponse(response, 'Greška pri dohvatanju tema.');
}

export async function getTopicById(id) {
  const response = await fetch(`${BASE_URL}/forum/topics/${id}`, {
    headers: getHeaders()
  });
  return handleResponse(response, 'Detalji teme se ne mogu učitati.');
}

export async function incrementTopicView(id) {
  const response = await fetch(`${BASE_URL}/forum/topics/${id}/view`, {
    method: 'PATCH',
    headers: getHeaders()
  });
  return handleResponse(response, 'Broj pregleda se ne može ažurirati.');
}

export async function deleteTopic(topicId) {
  const response = await fetch(`${BASE_URL}/forum/topics/${topicId}`, {
    method: 'DELETE',
    headers: getHeaders()
  });
  return handleResponse(response, 'Brisanje teme nije uspjelo.');
}

export async function createTopic(topicData) {
  const response = await fetch(`${BASE_URL}/forum/topics`, {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify(topicData)
  });
  return handleResponse(response, 'Kreiranje teme nije uspjelo.');
}

export async function createComment(commentData) {
  const response = await fetch(`${BASE_URL}/forum/comments`, {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify(commentData)
  });
  return handleResponse(response, 'Slanje komentara nije uspjelo.');
}

export async function voteOnComment(commentId, value) {
  const response = await fetch(`${BASE_URL}/forum/comments/${commentId}/vote`, {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify({ value })
  });
  return handleResponse(response, 'Glasanje nije uspjelo.');
}

export async function toggleBestAnswer(commentId) {
  const response = await fetch(`${BASE_URL}/forum/comments/${commentId}/best-answer`, {
    method: 'PATCH',
    headers: getHeaders()
  });
  return handleResponse(response, 'Označavanje najboljeg odgovora nije uspjelo.');
}

export async function getPopularTags() {
  const response = await fetch(`${BASE_URL}/forum/tags`, {
    headers: getHeaders()
  });
  return handleResponse(response, 'Greška pri dohvatanju tagova.');
}

export async function deleteComment(commentId) {
  const response = await fetch(`${BASE_URL}/forum/comments/${commentId}`, {
    method: 'DELETE',
    headers: getHeaders()
  });
  return handleResponse(response, 'Brisanje komentara nije uspjelo.');
}

export default {
  getCategories,
  getTopics,
  getTopicById,
  incrementTopicView,
  deleteTopic,
  createTopic,
  createComment,
  voteOnComment,
  toggleBestAnswer,
  getPopularTags,
  deleteComment
};