import axios from 'axios';

const API_URL = 'http://localhost:8000/posts/';

export const getPosts = async () => {
  const response = await axios.get(API_URL);
  return response.data;
};

export const getPost = async (id) => {
  try {
    const response = await axios.get(`${API_URL}${id}/`);
    return response.data;
  } catch (error) {
    console.error(error);
    return null;
  }
};

export const createPost = async (newPost) => {
  const response = await axios.post(API_URL, newPost);
  return response.data;
};

export const updatePost = async (id, updatedPost) => {
  const response = await axios.put(`${API_URL}${id}/`, updatedPost);
  return response.data;
};

export const deletePost = async (id) => {
  const response = await axios.delete(`${API_URL}${id}/`);
  return response.data;
};