import { useState, useEffect, useCallback } from 'react';
import { login as apiLogin, logout as apiLogout, register as apiRegister } from '../services/api';

const useAuth = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const checkAuth = useCallback(() => {
    const token = localStorage.getItem('token');
    const username = localStorage.getItem('username');
    if (token && username) {
      // In a real app, you might want to validate the token with the server here
      setUser({ token, username });
    } else {
      setUser(null);
    }
    setLoading(false);
  }, []);

  useEffect(() => {
    checkAuth();
  }, [checkAuth]);

  const login = async (username, password) => {
    try {
      const response = await apiLogin(username, password);  // Assume apiLogin is the function that makes the API call
     
  
      // Extracting the data from the response
      const { token, user_id, email } = response.data;
  
      // Storing the token and additional user information in local storage
      localStorage.setItem('token', token);
      localStorage.setItem('username', username);  // Username might still be useful to store
      localStorage.setItem('user_id', user_id);
      localStorage.setItem('email', email);
  
      // Setting user state
      setUser({ token, username, user_id, email });
  
      return true;
    } catch (error) {
      console.error('Login failed:', error);
      return false;
    }
  };
  

  const logout = async () => {
    try {
      await apiLogout();
    } catch (error) {
      console.error('Logout failed:', error);
    } finally {
      localStorage.removeItem('token');
      localStorage.removeItem('username');
      setUser(null);
    }
  };

  const register = async (username, email, password, firstName, lastName, bio, dateOfBirth) => {
    try {
      const data = await apiRegister({
        username,
        email,
        password,
        first_name: firstName,
        last_name: lastName,
        bio,
        date_of_birth: dateOfBirth,
      });
      
      return true;
    } catch (error) {
      console.error('Registration failed:', error);
      return false;
    }
  };


  return { user, loading, login, logout, register };
};

export default useAuth;
