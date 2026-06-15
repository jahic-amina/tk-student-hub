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

export async function getReports() {
  const res = await fetch(`${BASE_URL}/admin/reports`, { headers: getHeaders() });
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

export async function createAnnouncement(content) {
  const res = await fetch(`${BASE_URL}/admin/announcements`, { method: 'POST', headers: getHeaders(), body: JSON.stringify({ content }) });
  return res.json();
}

export async function deleteAnnouncement(annId) {
  const res = await fetch(`${BASE_URL}/admin/announcements/${annId}`, { method: 'DELETE', headers: getHeaders() });
  return res.json();
}