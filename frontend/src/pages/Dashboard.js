import React, { useState, useEffect } from 'react';
import { appointmentService, doctorService, patientService } from '../services/api';

const Dashboard = ({ user }) => {
  const [stats, setStats] = useState({
    appointments: 0,
    doctors: 0,
    patients: 0,
    records: 0,
  });
  const [recentAppointments, setRecentAppointments] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      const [appointmentsRes, doctorsRes, patientsRes] = await Promise.all([
        appointmentService.getAll(0, 10),
        doctorService.getAll(0, 10),
        patientService.getAll(0, 10),
      ]);

      setStats({
        appointments: appointmentsRes.data.length,
        doctors: doctorsRes.data.length,
        patients: patientsRes.data.length,
        records: 0, // Will be updated when we get medical records
      });

      setRecentAppointments(appointmentsRes.data.slice(0, 5));
    } catch (error) {
      console.error('Failed to load dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const StatCard = ({ icon, title, value, color = "medical" }) => (
    <div className="card hover:shadow-lg transition-shadow duration-200">
      <div className="flex items-center">
        <div className={`p-3 rounded-lg bg-${color}-100`}>
          <i className={`${icon} text-xl text-${color}-600`}></i>
        </div>
        <div className="ml-4">
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-2xl font-bold text-gray-900">{loading ? '...' : value}</p>
        </div>
      </div>
    </div>
  );

  return (
    <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div className="px-4 py-6 sm:px-0">
        {/* Welcome Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">
            Welcome back, {user?.email?.split('@')[0]}!
          </h1>
          <p className="mt-2 text-gray-600">
            Here's what's happening in your clinic today.
          </p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatCard
            icon="fas fa-calendar-check"
            title="Total Appointments"
            value={stats.appointments}
            color="medical"
          />
          <StatCard
            icon="fas fa-user-md"
            title="Active Doctors"
            value={stats.doctors}
            color="primary"
          />
          <StatCard
            icon="fas fa-users"
            title="Registered Patients"
            value={stats.patients}
            color="green"
          />
          <StatCard
            icon="fas fa-file-medical"
            title="Medical Records"
            value={stats.records}
            color="purple"
          />
        </div>

        {/* Recent Activity */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Recent Appointments */}
          <div className="lg:col-span-2">
            <div className="card">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-medium text-gray-900">Recent Appointments</h3>
                <i className="fas fa-clock text-gray-400"></i>
              </div>
              
              {loading ? (
                <div className="space-y-3">
                  {[...Array(3)].map((_, i) => (
                    <div key={i} className="animate-pulse">
                      <div className="h-16 bg-gray-200 rounded"></div>
                    </div>
                  ))}
                </div>
              ) : recentAppointments.length > 0 ? (
                <div className="space-y-3">
                  {recentAppointments.map((appointment, index) => (
                    <div
                      key={appointment.id || index}
                      className="flex items-center justify-between p-3 border border-gray-200 rounded-lg hover:bg-gray-50"
                    >
                      <div>
                        <p className="text-sm font-medium text-gray-900">
                          Patient ID: {appointment.patient_id}
                        </p>
                        <p className="text-sm text-gray-500">
                          Doctor ID: {appointment.doctor_id}
                        </p>
                      </div>
                      <div className="text-right">
                        <p className="text-sm text-gray-900">
                          {new Date(appointment.appointment_time).toLocaleDateString()}
                        </p>
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                          appointment.status === 'Scheduled' 
                            ? 'bg-green-100 text-green-800' 
                            : 'bg-yellow-100 text-yellow-800'
                        }`}>
                          {appointment.status}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-6 text-gray-500">
                  No appointments found
                </div>
              )}
            </div>
          </div>

          {/* Quick Actions */}
          <div className="card">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Quick Actions</h3>
            <div className="space-y-3">
              {user?.role === 'admin' && (
                <>
                  <button className="w-full btn-primary text-left">
                    Add New Doctor
                  </button>
                  <button className="w-full btn-secondary text-left">
                    View All Patients
                  </button>
                </>
              )}
              
              <button className="w-full btn-primary text-left">
                Schedule Appointment
              </button>
              
              {user?.role === 'doctor' && (
                <button className="w-full btn-secondary text-left">
                  Create Medical Record
                </button>
              )}
              
              <button className="w-full btn-secondary text-left">
                View Reports
              </button>
            </div>
          </div>
        </div>

        {/* Role-specific sections */}
        {user?.role === 'patient' && (
          <div className="mt-8">
            <div className="card">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Your Next Appointments</h3>
              <p className="text-gray-600">You have no upcoming appointments.</p>
              <button className="mt-4 btn-primary">
                Schedule New Appointment
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
