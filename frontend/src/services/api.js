const BASE_URL = "http://127.0.0.1:8000";

export async function registerUser(email, fullName, password) {
  const response = await fetch(`${BASE_URL}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, full_name: fullName, password }),
  });
  return response.json();
}

export async function loginUser(email, password) {
  const formData = new FormData();
  formData.append("username", email);
  formData.append("password", password);

  const response = await fetch(`${BASE_URL}/auth/login`, {
    method: "POST",
    body: formData,
  });
  return response.json();
}

export async function getMe(token) {
  const response = await fetch(`${BASE_URL}/me`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.json();
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

  try {
    const response = await fetch(url, {
      method: "GET",
      headers: { 
        "Authorization": `Bearer ${token}` // POŠALJI TOKEN
      },
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