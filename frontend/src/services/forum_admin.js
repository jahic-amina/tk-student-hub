const BASE_URL = 'http://127.0.0.1:8000';

function getHeaders() {
  const token = localStorage.getItem('token') || localStorage.getItem('access_token');
  return {
    'Content-Type': 'application/json',
    'Authorization': token ? `Bearer ${token}` : ''
  };
}

export async function getUsers() {
  const res = await fetch(`${BASE_URL}/admin/users`, { headers: getHeaders() });
  return res.json();
}

export async function changeUserRole(userId, role) {
  const res = await fetch(`${BASE_URL}/admin/users/${userId}/role?role=${role}`, { method: 'PATCH', headers: getHeaders() });
  return res.json();
}

export async function getReports(status = 'pending') {
  const res = await fetch(`${BASE_URL}/admin/reports?status=${status}`, { headers: getHeaders() });
  return res.json();
}

export async function dismissReport(reportId) {
  const res = await fetch(`${BASE_URL}/admin/reports/${reportId}`, { method: 'DELETE', headers: getHeaders() });
  return res.json();
}

export async function toggleTopicLock(topicId) {
  const res = await fetch(`${BASE_URL}/admin/topics/${topicId}/lock`, { method: 'PATCH', headers: getHeaders() });
  return res.json();
}

export async function createAnnouncement(title, content, durationDays) {
  const res = await fetch(`${BASE_URL}/admin/announcements`, { 
    method: 'POST', 
    headers: getHeaders(), 
    body: JSON.stringify({ title, content, duration_days: durationDays }) 
  });
  return res.json();
}

export async function getAllAnnouncements() {
  const res = await fetch(`${BASE_URL}/admin/announcements/all`, { headers: getHeaders() });
  return res.json();
}

export async function updateAnnouncement(annId, data) {
  const res = await fetch(`${BASE_URL}/admin/announcements/${annId}`, {
    method: 'PATCH',
    headers: getHeaders(),
    body: JSON.stringify(data)
  });
  return res.json();
}

export async function deleteAnnouncement(annId) {
  const res = await fetch(`${BASE_URL}/admin/announcements/${annId}`, { method: 'DELETE', headers: getHeaders() });
  return res.json();
}

export async function getHandledReports() {
  const res = await fetch(`${BASE_URL}/admin/reports?status=resolved`, { headers: getHeaders() });
  return res.json();
}

export async function getGuidelines() {
  const res = await fetch(`${BASE_URL}/forum/guidelines/`, { headers: getHeaders() });
  return res.json();
}

export async function createGuideline(title, content, order = 0) {
  const res = await fetch(`${BASE_URL}/forum/guidelines/`, {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify({ title, content, order })
  });
  return res.json();
}

export async function updateGuideline(id, data) {
  const res = await fetch(`${BASE_URL}/forum/guidelines/${id}`, {
    method: 'PATCH',
    headers: getHeaders(),
    body: JSON.stringify(data)
  });
  return res.json();
}

export async function deleteGuideline(id) {
  const res = await fetch(`${BASE_URL}/forum/guidelines/${id}`, {
    method: 'DELETE',
    headers: getHeaders()
  });
  return res.json();
}

export async function postAdminNotice(topicId, content) {
  const res = await fetch(`${BASE_URL}/forum/comments/${topicId}/admin-notice`, {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify({ content })
  });
  return res.json();
}

export async function adminPullToReports(topicId) {
  const res = await fetch(`${BASE_URL}/admin/topics/${topicId}/pull-to-reports`, {
    method: 'POST',
    headers: getHeaders()
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || 'Greška pri povlačenju u prijave.');
  }
  return res.json();
}

export async function reopenReport(reportId) {
  const res = await fetch(`${BASE_URL}/admin/reports/${reportId}/reopen`, {
    method: 'PATCH',
    headers: getHeaders()
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || 'Greška pri vraćanju prijave.');
  }
  return res.json();
}

export async function resolveReport(reportId, action, explanation) {
  const res = await fetch(`${BASE_URL}/admin/reports/${reportId}/resolve`, {
    method: 'PATCH',
    headers: getHeaders(),
    body: JSON.stringify({ action, explanation })
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || 'Greška pri rješavanju prijave.');
  }
  return res.json();
}