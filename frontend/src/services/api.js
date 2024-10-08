import axios from "axios";

const API_URL = "http://localhost:8000/api"; // Replace with your Django API URL

const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

export const login = async (username, password) => {
  const response = await api.post("/login/", { username, password });
  console.log(response)
  return response.data;
};

export const register = async (recipeData) => {
  const response = await api.post("/users/register/", recipeData.username);
  return response.data;
};

export const logout = async () => {
  const response = await api.post("/users/logout/");
  return response.data;
};

export const getAllRecipes = async (url = null) => {
  try {
    const response = await api.get(url || "/recipes/");
    return response.data;
  } catch (error) {
    console.error("Error fetching recipes:", error);
    throw error;
  }
};

export const getRecipe = async (id) => {
  const response = await api.get(`/recipes/${id}/`);
  return response.data;
};

export const createRecipe = async (recipeData) => {
  
  const token = localStorage.getItem("token");
  const response = await api.post("/recipes/", recipeData, {
    headers: {
      "Content-Type": "multipart/form-data",

      Authorization: `Token ${token}`,
    },
  });
  return response.data;
};

export const updateRecipe = async (id, recipeData) => {
  const token = localStorage.getItem("token");
  const response = await api.put(`/recipes/${id}/`, recipeData,{
    headers: {
      "Content-Type": "multipart/form-data",

      Authorization: `Token ${token}`,
    },
  });
  return response.data;
};

export const deleteRecipe = async (id) => {
  const response = await api.delete(`/recipes/${id}/`);
  return response.data;
};

export const getUserRecipes = async (url = null) => {
  try {
    const response = await api.get(url || "/my-recipes/");
    return response.data;
  } catch (error) {
    console.error("Error fetching user recipes:", error);
    throw error;
  }
};

export default api;
