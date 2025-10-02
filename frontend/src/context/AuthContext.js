import React, { createContext, useState, useContext } from "react";
import axiosInstance from "../axiosConfig";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(() => {
    const storedUser = localStorage.getItem("user");
    return storedUser ? JSON.parse(storedUser) : null;
  });

  const [token, setToken] = useState(() => localStorage.getItem("token") || null);

  // Login with backend
  const login = async (email, password) => {
    try {
      const res = await axiosInstance.post("/auth/login", {
        email,
        password,
      });

      const { token, id, name, email: userEmail } = res.data;
      // Compose user object from response
      const user = { id, name, email: userEmail };

      setUser(user);
      setToken(token);

      localStorage.setItem("user", JSON.stringify(user));
      localStorage.setItem("token", token);

      return true;
    } catch (err) {
      console.error("Login failed:", err);
      return false;
    }
  };

  // Logout clears everything
  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem("user");
    localStorage.removeItem("token");
  };

  return (
    <AuthContext.Provider value={{ user, token, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
