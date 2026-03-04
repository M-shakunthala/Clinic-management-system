import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Heart, User, LogOut, Calendar, Users, Stethoscope, FileText } from 'lucide-react';

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
              <Heart className="h-8 w-8 text-medical-500" />
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
                    <Stethoscope className="h-4 w-4" />
                    <span>Doctors</span>
                  </Link>
                )}
                
                <Link
                  to="/appointments"
                  className="text-gray-700 hover:text-medical-500 px-3 py-2 rounded-md text-sm font-medium transition-colors flex items-center space-x-1"
                >
                  <Calendar className="h-4 w-4" />
                  <span>Appointments</span>
                </Link>
                
                {user.role === 'admin' && (
                  <Link
                    to="/patients"
                    className="text-gray-700 hover:text-medical-500 px-3 py-2 rounded-md text-sm font-medium transition-colors flex items-center space-x-1"
                  >
                    <Users className="h-4 w-4" />
                    <span>Patients</span>
                  </Link>
                )}
                
                {(user.role === 'doctor' || user.role === 'patient') && (
                  <Link
                    to="/medical-records"
                    className="text-gray-700 hover:text-medical-500 px-3 py-2 rounded-md text-sm font-medium transition-colors flex items-center space-x-1"
                  >
                    <FileText className="h-4 w-4" />
                    <span>Records</span>
                  </Link>
                )}
              </div>

              <div className="flex items-center space-x-3">
                <div className="flex items-center space-x-2 text-sm text-gray-700">
                  <User className="h-4 w-4" />
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
                  <LogOut className="h-5 w-5" />
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
