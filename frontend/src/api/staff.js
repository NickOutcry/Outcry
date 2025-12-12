/**
 * Staff API
 * API calls for staff domain
 */
import apiClient from './index';

export const staffApi = {
  // Get all staff
  getAll: () => apiClient.get('/staff'),
  
  // Get single staff member
  getById: (id) => apiClient.get(`/staff/${id}`),
  
  // Create staff member
  create: (data) => apiClient.post('/staff', data),
  
  // Update staff member
  update: (id, data) => apiClient.put(`/staff/${id}`, data),
  
  // Delete staff member
  delete: (id) => apiClient.delete(`/staff/${id}`),
  
  // Test endpoint
  test: () => apiClient.get('/staff/test'),
};

