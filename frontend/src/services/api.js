const BASE_URL = "http://127.0.0.1:8000";

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
  const formData = new FormData();
  formData.append("username", email);
  formData.append("password", password);

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
  const token = localStorage.getItem('token')
  if (!token || token === 'null' || token === 'undefined') {
    throw new Error('Not authenticated')
  }

  const formData = new FormData()
  formData.append('file', file)

  const response = await fetch(`${BASE_URL}/applications/upload-cv`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`
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

// --- Bookmarks ---

export async function getBookmarks(token) {
  const response = await fetch(`${BASE_URL}/bookmarks/`, {
    headers: authHeaders(token)
  })
  return parseResponse(response)
}

export async function addBookmark(adId, token) {
  const response = await fetch(`${BASE_URL}/bookmarks/`, {
    method: 'POST',
    headers: authHeaders(token),
    body: JSON.stringify({ ad_id: adId })
  })
  return parseResponse(response)
}

export async function removeBookmark(bookmarkId, token) {
  const response = await fetch(`${BASE_URL}/bookmarks/${bookmarkId}`, {
    method: 'DELETE',
    headers: authHeaders(token)
  })
  if (!response.ok) {
    const message = await response.text()
    throw new Error(message || `Request failed with status ${response.status}`)
  }
  return true;
}

// --- Notifications (Konačna i popravljena verzija) ---

export const notificationService = {
  getMyNotifications: async () => {

    const token = localStorage.getItem('token') || localStorage.getItem('company_token');
    
    const response = await fetch(`${BASE_URL}/notifications/me`, {
      method: 'GET',
      headers: authHeaders(token)
    })
    return parseResponse(response)
  },

  markAsRead: async (id) => {
    const token = localStorage.getItem('token') || localStorage.getItem('company_token');
    const response = await fetch(`${BASE_URL}/notifications/${id}/read`, {
      method: 'PUT',
      headers: authHeaders(token)
    })
    return parseResponse(response)
  },

  markAllAsRead: async () => {
    const token = localStorage.getItem('token') || localStorage.getItem('company_token');
    const response = await fetch(`${BASE_URL}/notifications/read-all`, {
      method: 'PUT',
      headers: authHeaders(token)
    })
    return parseResponse(response)
  },

  clearAll: async () => {
    const token = localStorage.getItem('token') || localStorage.getItem('company_token');
    const response = await fetch(`${BASE_URL}/notifications/clear-all`, {
      method: 'DELETE',
      headers: authHeaders(token)
    });
    
    if (!response.ok) {
      const message = await response.text();
      throw new Error(message || `Request failed with status ${response.status}`);
    }
    
    return true;
  }
}


export async function uploadMaterial(formData) {
  const token = localStorage.getItem("token");
  const response = await fetch(`${BASE_URL}/materials/upload`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
    body: formData,
  });
  return response;
}


export async function getMaterial(id) {
  const response = await fetch(`${BASE_URL}/materials/${id}`);
  return response.json();
}

//amer
export async function deleteMaterial(id) {
  const token = localStorage.getItem("token");
  const response = await fetch(`${BASE_URL}/materials/${id}`, {
    method: "DELETE",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return response;
}
export async function getSubjects() {
  const res = await fetch(`${BASE_URL}/materials/subjects`);
  return res.json();
}
export async function getMaterials(filters = {}) {
  const params = new URLSearchParams();

  
  if (filters.years && filters.years.length > 0) {
    filters.years.forEach(y => params.append('years', y));
  }
  if (filters.types && filters.types.length > 0) {
    filters.types.forEach(t => params.append('types', t));
  }
  if (filters.subject_id) {
    params.append('subject_id', filters.subject_id);
  }

  const queryString = params.toString();
  
  
  const url = queryString 
    ? `${BASE_URL}/materials/?${queryString}` 
    : `${BASE_URL}/materials/`;

  const token = localStorage.getItem("token");
  const headers = authHeaders(token);

  try {
    const response = await fetch(url, {
      method: "GET",
      headers,
    });
    
    if (response.status === 401) {
       console.error("Niste ulogovani ili je token istekao");
       return [];
    }

    if (!response.ok) throw new Error('Mrežna greška');
    return await response.json();
  } catch (error) {
    console.error("Greška u API pozivu:", error);
    return [];
  }
}

export async function toggleBookmark(materialId) {
  const token = localStorage.getItem("token");
  const response = await fetch(`${BASE_URL}/materials/${materialId}/bookmark`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.json();
}

//

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

export async function getPlatformStats(token, period = 'month') {
  try {
    const response = await fetch(`http://localhost:8000/admin/stats?period=${period}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    if (!response.ok) throw new Error('Greška pri dohvatu statistike');
    return await response.json();
  } catch (error) {
    console.error(error);
    return null;
  }
}
export async function deleteComment(materialId, commentId) {
  const token = localStorage.getItem('token')
  const response = await fetch(`${BASE_URL}/materials/${materialId}/comments/${commentId}`, {
      method: 'DELETE',
      headers: {
          'Authorization': `Bearer ${token}`
      }
  })
  if (!response.ok) {
      throw new Error('Greška pri brisanju komentara.')
  }
}

export async function getPendingMaterials() {
  const token = localStorage.getItem("token");
  const response = await fetch(`${BASE_URL}/materials/pending`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.json();
}

export async function approveMaterial(id) {
  const token = localStorage.getItem("token");
  const response = await fetch(`${BASE_URL}/materials/${id}/approve`, {
    method: "PATCH",
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.json();
}

export async function rejectMaterial(id) {
  const token = localStorage.getItem("token");
  const response = await fetch(`${BASE_URL}/materials/${id}/reject`, {
    method: "PATCH",
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.json();
}

export async function updateMaterial(id, title, description, file) {
  const token = localStorage.getItem("token");
  const formData = new FormData();
  formData.append('title', title);
  formData.append('description', description);
  if (file) {
    formData.append('file', file);
  }
  const response = await fetch(`${BASE_URL}/materials/${id}/update`, {
    method: "PATCH",
    headers: {
      Authorization: `Bearer ${token}`,
    },
    body: formData,
  });
  if(!response.ok) {
    throw new Error('Greška pri ažuriranju materijala.')
  }
  return response.json();
}

// Ocjenjivanje materijala 
export async function rateMaterial(materialId, rating) {
  const token = localStorage.getItem('token')
  const response = await fetch(`${BASE_URL}/materials/${materialId}/rate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ rating, material_id: materialId })
  })
  return response
}

export async function updateRating(materialId, rating) {
  const token = localStorage.getItem('token')
  const response = await fetch(`${BASE_URL}/materials/${materialId}/rate`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ rating, material_id: materialId })
  })
  return response
}

// Download materijala - Marinela
export async function downloadMaterial(materialId) {
  const response = await fetch(`${BASE_URL}/materials/${materialId}/download`)
  return response
}
