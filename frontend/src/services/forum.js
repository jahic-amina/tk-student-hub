import axios from "axios";


const forumApi = axios.create({
  baseURL: "http://127.0.0.1:8000",
  headers: {
    "Content-Type": "application/json",
  },
});


forumApi.interceptors.request.use((config) => {
  const token = localStorage.getItem("token") || localStorage.getItem("access_token");

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});


export const getTopics = async () => {
  const response = await forumApi.get("/forum/topics");
  return response.data;
};

export const getTopicById = async (id) => {
  const response = await forumApi.get(`/forum/topics/${id}`);
  return response.data;
};

export const incrementTopicView = async (id) => {
  const response = await forumApi.patch(`/forum/topics/${id}/view`);
  return response.data;
};

export const createTopic = async (topicData) => {
  const response = await forumApi.post("/forum/topics", topicData);
  return response.data;
};

export const createComment = async (commentData) => {
  const response = await forumApi.post("/forum/comments", commentData);
  return response.data;
};

export const deleteTopic = async (id) => {
  const response = await forumApi.delete(`/forum/topics/${id}`);
  return response.data;
};

export const deleteComment = async (id) => {
  const response = await forumApi.delete(`/forum/comments/${id}`);
  return response.data;
};


export default {
  getTopics,
  getTopicById,
  incrementTopicView,
  createTopic,
  createComment,
  deleteTopic,
  deleteComment,
};