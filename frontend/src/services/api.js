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

export async function getMyProfile(token) {
  const response = await fetch(`${BASE_URL}/profiles/me`, {
    headers: { 'Authorization': `Bearer ${token}` }
  })
  return response.json()
}

export async function uploadAvatar(token, file) {
  const formData = new FormData()
  formData.append('file', file)

  const response = await fetch(`${BASE_URL}/profiles/me/avatar`, {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${token}` },
    body: formData
  })
  const data = await response.json()
  
  if (data.profilna_slika_url) {
    data.profilna_slika_url = data.profilna_slika_url + '?t=' + Date.now()
  }
  
  return data
}

export async function removeAvatar(token) {
  const response = await fetch(`${BASE_URL}/profiles/me/avatar`, {
    method: 'DELETE',
    headers: { 'Authorization': `Bearer ${token}` }
  })
  return response.json()
}

export async function getMyActivity(token, limit = 3, offset = 0) {
  const response = await fetch(`${BASE_URL}/api/users/me/activity?limit=${limit}&offset=${offset}`, {
    headers: { 'Authorization': `Bearer ${token}` }
  })
  return response.json()
}
export async function getAllUsers(token, { search = '', role = '', is_active = '' } = {}) {
  const params = new URLSearchParams()
  if (search) params.append('search', search)
  if (role) params.append('role', role)
  if (is_active !== '') params.append('is_active', is_active)

  const response = await fetch(`${BASE_URL}/admin/users?${params.toString()}`, {
    headers: { 'Authorization': `Bearer ${token}` }
  })
  return response.json()
}

async function handleAdminFetch(response, defaultErrorMessage) {
  // 1. Provjera da li je backend vratio 403 (Forbidden)
  if (response.status === 403) {
    const clone = response.clone(); // Kloniramo odgovor da ga možemo pročitati
    try {
      const errorData = await clone.json();
      if (errorData?.detail?.includes("deaktiviran")) {
        // Logika za odjavu i preusmjeravanje
        localStorage.removeItem('token');
        localStorage.removeItem('access_token');
        alert("Vaš nalog je deaktiviran. Kontaktirajte administratora za reaktivaciju.");
        window.location.href = '/login';
        
        throw new Error("Akcija prekinuta: Nalog je deaktiviran.");
      }
    } catch (e) {
      
    }
  }

  // 2. Standardna provjera za ostale greške (400, 404, 500...)
  if (!response.ok) {
    throw new Error(defaultErrorMessage);
  }

  return await response.json();
}
// Aktivacija korisnika
export async function activateUser(token, userId) {
  const response = await fetch(`${BASE_URL}/admin/users/${userId}/activate`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  });

  return handleAdminFetch(response, 'Greška pri aktivaciji korisnika');
}

// Deaktivacija korisnika
export async function deactivateUser(token, userId) {
  const response = await fetch(`${BASE_URL}/admin/users/${userId}/deactivate`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  });

  return handleAdminFetch(response, 'Greška pri deaktivaciji korisnika');
}

// Trajno brisanje korisnika
export async function deleteUser(token, userId) {
  const response = await fetch(`${BASE_URL}/admin/users/${userId}`, {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  });

  return handleAdminFetch(response, 'Greška pri brisanju korisnika');
}

