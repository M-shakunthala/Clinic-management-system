import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import Navbar from './components/Navbar';
import Login from './pages/Login';
import SignUp from './pages/SignUp';
import Dashboard from './pages/Dashboard';
import Appointments from './pages/Appointments';
import Patients from './pages/Patients';
import { authService } from './services/api';
import './index.css';

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    const token = localStorage.getItem('token');
    if (token) {
      try {
        const response = await authService.getCurrentUser();
        setUser(response.data);
      } catch (error) {
        localStorage.removeItem('token');
      }
    }
    setLoading(false);
  };

  const handleLogin = (userData) => {
    setUser(userData);
  };

  const handleLogout = () => {
    setUser(null);
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-medical-500"></div>
      </div>
    );
  }

  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Toaster position="top-right" />
        
        {user && <Navbar user={user} onLogout={handleLogout} />}
        
        <main className={user ? 'pt-16' : ''}>
          <Routes>
            <Route
              path="/login"
              element={
                user ? <Navigate to="/dashboard" /> : <Login onLogin={handleLogin} />
              }
            />
            
            <Route
              path="/signup"
              element={
                user ? <Navigate to="/dashboard" /> : <SignUp />
              }
            />
            
            <Route
              path="/dashboard"
              element={
                user ? <Dashboard user={user} /> : <Navigate to="/login" />
              }
            />

            <Route
              path="/appointments"
              element={
                user ? <Appointments user={user} /> : <Navigate to="/login" />
              }
            />

            <Route
              path="/patients"
              element={
                user ? <Patients user={user} /> : <Navigate to="/login" />
              }
            />
            
            <Route
              path="/"
              element={<Navigate to={user ? "/dashboard" : "/login"} />}
            />
            
            <Route
              path="*"
              element={<Navigate to={user ? "/dashboard" : "/login"} />}
            />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
