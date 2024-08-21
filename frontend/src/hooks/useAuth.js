// File: src/hooks/useAuth.js

import { useState, useEffect, useCallback } from 'react';
import { login as apiLogin, logout as apiLogout } from '../services/api';

const useAuth = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const checkAuth = useCallback(() => {
    const token = localStorage.getItem('token');
    if (token) {
      // In a real app, you might want to validate the token with the server here
      setUser({ token });
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
      console.log(username, password)
      const data = await apiLogin(username, password);
      localStorage.setItem('token', data.token);
      setUser({ token: data.token });
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
      setUser(null);
    }
  };

  return { user, loading, login, logout };
};

export default useAuth;