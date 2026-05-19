import axios from "axios";

const forumApi = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

forumApi.interceptors.request.use((config) => {
  const token = localStorage.getItem("token") || localStorage.getItem("access_token");

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

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