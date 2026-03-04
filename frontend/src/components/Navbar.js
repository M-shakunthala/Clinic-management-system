import React from 'react';
import { Link, useNavigate } from 'react-router-dom';

const Navbar = ({ user, onLogout }) => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('token');
    onLogout();
    navigate('/login');
  };

  return (
    <nav className="navbar">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="flex items-center space-x-2">
              <svg 
                width="32" 
                height="32" 
                viewBox="0 0 24 24" 
                fill="none" 
                xmlns="http://www.w3.org/2000/svg"
                className="text-medical-500"
              >
                <path 
                  d="M3 12h2l2-5 4 10 4-10 2 5h4" 
                  stroke="currentColor" 
                  strokeWidth="2.5" 
                  strokeLinecap="round" 
                  strokeLinejoin="round"
                  fill="none"
                />
                <circle cx="12" cy="12" r="1" fill="currentColor"/>
              </svg>
              <span className="text-xl font-bold text-gray-900">ClinicCare</span>
            </Link>
          </div>

          {user && (
            <div className="flex items-center space-x-4">
              <div className="hidden md:flex space-x-4">
                <Link
                  to="/dashboard"
                  className="text-gray-700 hover:text-medical-500 px-3 py-2 rounded-md text-sm font-medium transition-colors"
                >
                  Dashboard
                </Link>
                
                {(user.role === 'admin' || user.role === 'doctor') && (
                  <Link
                    to="/doctors"
                    className="text-gray-700 hover:text-medical-500 px-3 py-2 rounded-md text-sm font-medium transition-colors flex items-center space-x-1"
                  >
                    <i className="fas fa-user-md"></i>
                    <span>Doctors</span>
                  </Link>
                )}
                
                <Link
                  to="/appointments"
                  className="text-gray-700 hover:text-medical-500 px-3 py-2 rounded-md text-sm font-medium transition-colors flex items-center space-x-1"
                >
                  <i className="fas fa-calendar-alt"></i>
                  <span>Appointments</span>
                </Link>
                
                {user.role === 'admin' && (
                  <Link
                    to="/patients"
                    className="text-gray-700 hover:text-medical-500 px-3 py-2 rounded-md text-sm font-medium transition-colors flex items-center space-x-1"
                  >
                    <i className="fas fa-users"></i>
                    <span>Patients</span>
                  </Link>
                )}
                
                {(user.role === 'doctor' || user.role === 'patient') && (
                  <Link
                    to="/medical-records"
                    className="text-gray-700 hover:text-medical-500 px-3 py-2 rounded-md text-sm font-medium transition-colors flex items-center space-x-1"
                  >
                    <i className="fas fa-file-medical"></i>
                    <span>Records</span>
                  </Link>
                )}
              </div>

              <div className="flex items-center space-x-3">
                <div className="flex items-center space-x-2 text-sm text-gray-700">
                  <i className="fas fa-user"></i>
                  <span>{user.email}</span>
                  <span className="bg-medical-100 text-medical-700 px-2 py-1 rounded-full text-xs font-medium capitalize">
                    {user.role}
                  </span>
                </div>
                <button
                  onClick={handleLogout}
                  className="text-gray-400 hover:text-gray-600 transition-colors"
                  title="Logout"
                >
                  <i className="fas fa-sign-out-alt"></i>
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
