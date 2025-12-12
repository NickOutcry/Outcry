/**
 * Client API
 * API calls for client domain
 */
import apiClient from './index';

export const clientApi = {
  // Get all clients
  getAll: () => apiClient.get('/clients'),
  
  // Get single client
  getById: (id) => apiClient.get(`/clients/${id}`),
  
  // Create client
  create: (data) => apiClient.post('/clients', data),
  
  // Update client
  update: (id, data) => apiClient.put(`/clients/${id}`, data),
  
  // Delete client
  delete: (id) => apiClient.delete(`/clients/${id}`),
  
  // Get client contacts
  getContacts: (clientId) => apiClient.get(`/clients/${clientId}/contacts`),
  
  // Get client billing entities
  getBillingEntities: (clientId) => apiClient.get(`/clients/${clientId}/billing-entities`),
  
  // Test endpoint
  test: () => apiClient.get('/client/test'),
};

