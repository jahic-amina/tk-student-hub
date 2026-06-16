const BASE_URL = 'http://127.0.0.1:8000';

function getHeaders() {
  const token = localStorage.getItem('token') || localStorage.getItem('access_token');
  const headers = { 'Content-Type': 'application/json' };
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  return headers;
}

async function handleResponse(response, defaultErrorMessage) {
  if (response.ok) {
    if (response.status === 204) return { success: true };
    return response.json();
  }
  try {
    const errorData = await response.json();
    throw new Error(errorData?.detail || defaultErrorMessage);
  } catch (e) {
    throw new Error(e.message || defaultErrorMessage);
  }
}

export async function getCategories() {
  const response = await fetch(`${BASE_URL}/forum/categories`, { headers: getHeaders() });
  return handleResponse(response, 'Greška pri dohvatanju kategorija.');
}

export async function getTopics({ category_id = null, search = "", page = 1, per_page = 5, sort_by = "najnovije", unanswered = false, days_old = null } = {}) {
  let queryParams = new URLSearchParams({ page: page.toString(), per_page: per_page.toString(), sort_by: sort_by });
  if (category_id !== null) queryParams.append('category_id', category_id.toString());
  if (search && search.trim()) queryParams.append('search', search.trim());
  if (unanswered) queryParams.append('unanswered', 'true');
  if (days_old !== null && days_old > 0) queryParams.append('days_old', days_old.toString());

  const response = await fetch(`${BASE_URL}/forum/topics?${queryParams.toString()}`, { headers: getHeaders() });
  return handleResponse(response, 'Greška pri dohvatanju tema.');
}

export async function getTopicById(id) {
  const response = await fetch(`${BASE_URL}/forum/topics/${id}`, { headers: getHeaders() });
  return handleResponse(response, 'Detalji teme se ne mogu učitati.');
}

export async function incrementTopicView(id) {
  const response = await fetch(`${BASE_URL}/forum/topics/${id}/view`, { method: 'PATCH', headers: getHeaders() });
  return handleResponse(response, 'Broj pregleda se ne može ažurirati.');
}

export async function deleteTopic(topicId) {
  const response = await fetch(`${BASE_URL}/forum/topics/${topicId}`, { method: 'DELETE', headers: getHeaders() });
  return handleResponse(response, 'Brisanje teme nije uspjelo.');
}

export async function createTopic(topicData) {
  const response = await fetch(`${BASE_URL}/forum/topics`, { method: 'POST', headers: getHeaders(), body: JSON.stringify(topicData) });
  return handleResponse(response, 'Kreiranje teme nije uspjelo.');
}

export async function createComment(commentData) {
  const response = await fetch(`${BASE_URL}/forum/comments`, { method: 'POST', headers: getHeaders(), body: JSON.stringify(commentData) });
  return handleResponse(response, 'Slanje komentara nije uspjelo.');
}

export async function voteOnComment(commentId, value) {
  const response = await fetch(`${BASE_URL}/forum/comments/${commentId}/vote`, { method: 'POST', headers: getHeaders(), body: JSON.stringify({ value }) });
  return handleResponse(response, 'Glasanje nije uspjelo.');
}

export async function toggleTopicLike(topicId) {
  const response = await fetch(`${BASE_URL}/forum/topics/${topicId}/like`, {
    method: 'POST',
    headers: getHeaders()
  });

  return handleResponse(response, 'Lajkovanje teme nije uspjelo.');
}

export async function toggleTopicDislike(topicId) {
  const response = await fetch(`${BASE_URL}/forum/topics/${topicId}/dislike`, {
    method: 'POST',
    headers: getHeaders()
  });

  return handleResponse(response, 'Dislajkovanje teme nije uspjelo.');
}

export async function toggleBestAnswer(commentId) {
  const response = await fetch(`${BASE_URL}/forum/comments/${commentId}/best-answer`, { method: 'PATCH', headers: getHeaders() });
  return handleResponse(response, 'Označavanje najboljeg odgovora nije uspjelo.');
}

export async function getPopularTags() {
  const response = await fetch(`${BASE_URL}/forum/tags`, { headers: getHeaders() });
  return handleResponse(response, 'Greška pri dohvatanju tagova.');
}

export async function deleteComment(commentId) {
  const response = await fetch(`${BASE_URL}/forum/comments/${commentId}`, { method: 'DELETE', headers: getHeaders() });
  return handleResponse(response, 'Brisanje komentara nije uspjelo.');
}

export async function updateComment(commentId, content) {
  const response = await fetch(`${BASE_URL}/forum/comments/${commentId}`, { method: 'PUT', headers: getHeaders(), body: JSON.stringify({ content }) });
  return handleResponse(response, 'Editovanje komentara nije uspjelo.');
}

export async function reportTopic(topicId, reason) {
  const response = await fetch(`${BASE_URL}/forum/topics/${topicId}/report`, { method: 'POST', headers: getHeaders(), body: JSON.stringify({ reason }) });
  return handleResponse(response, 'Prijavljivanje nije uspjelo.');
}

export async function getActiveAnnouncements() {
  const response = await fetch(`${BASE_URL}/forum/topics/announcements/active`, { headers: getHeaders() });
  return handleResponse(response, 'Greška pri učitavanju obavještenja.');
}

export async function getActiveReports() {
  const response = await fetch(`${BASE_URL}/forum/topics/reports/active`, { method: 'GET', headers: getHeaders() });
  return handleResponse(response, 'Neuspješno učitavanje prijava za moderaciju.');
}

export async function handleReportAction(reportId, action, explanation) {
  const response = await fetch(`${BASE_URL}/forum/topics/reports/${reportId}/action?action=${action}`, { method: 'PATCH', headers: getHeaders(), body: JSON.stringify({ explanation: explanation }) });
  if (response.ok) {
    return response.json();
  } else {
    const errorData = await response.json();
    let errorMsg = 'Greška pri izvršavanju akcije nad prijavom.';
    if (errorData?.detail) {
      errorMsg = Array.isArray(errorData.detail) 
        ? errorData.detail.map(e => e.msg).join(', ') 
        : errorData.detail;
    }
    throw new Error(errorMsg);
  }
}

export async function getSearchSuggestions(query = "", options = {}) {
  let url = `${BASE_URL}/forum/topics/suggestions`;
  if (query && query.trim()) url += `?search=${encodeURIComponent(query.trim())}`;
  const response = await fetch(url, { headers: getHeaders(), ...options });
  return handleResponse(response, 'Greška pri dohvatanju sugestija.');
}

// Globalni widget popularnih tema (Zadnjih 7 dana)
export async function getPopularTopics() {
  const response = await fetch(`${BASE_URL}/forum/topics/popular`, { headers: getHeaders() });
  return handleResponse(response, 'Greška pri dohvatanju popularnih tema.');
}

// Kontekstualni widget popularnih tema u kategoriji
export async function getCategoryPopularTopics(categoryId) {
  const response = await fetch(`${BASE_URL}/forum/topics/category-popular/${categoryId}`, { headers: getHeaders() });
  return handleResponse(response, 'Greška pri dohvatanju popularnih tema kategorije.');
}

// Widget za slične teme (unutar otvorene teme)
export async function getRelatedTopics(topicId) {
  const response = await fetch(`${BASE_URL}/forum/topics/${topicId}/related`, { headers: getHeaders() });
  return handleResponse(response, 'Greška pri dohvatanju povezanih tema.');
}

// Endpoint za uređivanje teme (dostupan samo originalnom autoru i adminima)
export async function updateTopic(topicId, data) {
  const response = await fetch(`${BASE_URL}/forum/topics/${topicId}`, {
    method: 'PUT',
    headers: getHeaders(),
    body: JSON.stringify(data)
  });
  return handleResponse(response, 'Editovanje teme nije uspjelo.');
}

export async function uploadTopicAttachments(topicId, files) {
  const token = localStorage.getItem('token') || localStorage.getItem('access_token');
  const formData = new FormData();
  files.forEach(file => formData.append('files', file));
  
  const response = await fetch(`${BASE_URL}/forum/attachments/topic/${topicId}`, {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${token}` },
    body: formData
  });
  return handleResponse(response, 'Upload fajlova nije uspio.');
}

export async function uploadCommentAttachments(commentId, files) {
  const token = localStorage.getItem('token') || localStorage.getItem('access_token');
  const formData = new FormData();
  files.forEach(file => formData.append('files', file));

  const response = await fetch(`${BASE_URL}/forum/attachments/comment/${commentId}`, {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${token}` },
    body: formData
  });
  return handleResponse(response, 'Upload fajlova nije uspio.');
}