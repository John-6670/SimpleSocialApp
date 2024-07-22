import axios from 'axios';

const BASE_URL = 'http://localhost:8000/posts/';

export const getComments = async (postId) => {
  const response = await axios.get(`${BASE_URL}${postId}/comments/`);
  return response.data;
};

export const createComment = async (postId, newComment) => {
  const response = await axios.post(`${BASE_URL}${postId}/comments/`, newComment);
  return response.data;
};

export const updateComment = async (postId, commentId, updatedComment) => {
  const response = await axios.put(`${BASE_URL}${postId}/comments/${commentId}/`, updatedComment);
  return response.data;
};

export const deleteComment = async (postId, commentId) => {
  const response = await axios.delete(`${BASE_URL}${postId}/comments/${commentId}/`);
  return response.data;
};