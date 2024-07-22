import axios from "axios";

const API_URL = 'http://localhost:8000/users';

export const getUser = async username => {
  const response = await axios.get(`${API_URL}/${username}/`);
  return response.data;
};

export const getProfile = async () => {
  const response = await axios.get(`${API_URL}/profile/`);
  return response.data;
};

export const updateUser = async updatedUser => {
  const response = await axios.put(`${API_URL}/profile/`, updatedUser);
  return response.data;
};

export const deleteUser = async () => {
  const response = await axios.delete(`${API_URL}/profile/`);
  return response.data;
};

export const register = async newUser => {
  const response = await axios.post(`${API_URL}/register/`, newUser);
  return response.data;
};

export const login = async user => {
  try {
    const response = await axios.post(`${API_URL}/login/`, user);
    return response.data;
  } catch (error) {
    console.log(error);
  }
};

export const logout = async () => {
    const response = await axios.post(`${API_URL}/logout/`);
    return response.data;
};

export const changePassword = async (oldPassword, newPassword, confirmPassword) => {
  const passwordData = {
    old_password: oldPassword,
    new_password: newPassword,
    confirm_password: confirmPassword,
  };

  const response = await axios.post(`${API_URL}/password-change/`, passwordData);
  return response.data;
};