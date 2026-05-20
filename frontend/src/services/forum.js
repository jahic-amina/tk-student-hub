<<<<<<< HEAD
const BASE_URL = 'http://127.0.0.1:8000'
=======
import axios from "axios";

const forumApi = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

forumApi.interceptors.request.use((config) => {
  const token = localStorage.getItem("token") || localStorage.getItem("access_token");
>>>>>>> origin/tim3/forum/detaljna-tema

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

<<<<<<< HEAD
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
=======
function handleForumError(error, fallbackMessage) {
  console.error("Forum API greška:", {
    message: error.message,
    status: error.response?.status,
    data: error.response?.data,
    url: error.config?.url,
  });

  throw new Error(
    error.response?.data?.detail ||
      error.message ||
      fallbackMessage
  );
}

export const getTopics = async ({ search = "" } = {}) => {
  try {
    const params = {};

    if (search && search.trim()) {
      params.search = search.trim();
    }

    const response = await forumApi.get("/forum/topics", { params });

    if (!Array.isArray(response.data)) {
      console.error("Neočekivan odgovor za /forum/topics:", response.data);
      return [];
    }

    return response.data;
  } catch (error) {
    handleForumError(error, "Teme se ne mogu učitati.");
  }
};

export const getTopicById = async (id) => {
  try {
    const response = await forumApi.get(`/forum/topics/${id}`);
    return response.data;
  } catch (error) {
    handleForumError(error, "Detalji teme se ne mogu učitati.");
  }
};

export const incrementTopicView = async (id) => {
  try {
    const response = await forumApi.patch(`/forum/topics/${id}/view`);
    return response.data;
  } catch (error) {
    handleForumError(error, "Broj pregleda se ne može ažurirati.");
  }
};

export default {
  getTopics,
  getTopicById,
  incrementTopicView,
};
>>>>>>> origin/tim3/forum/detaljna-tema
