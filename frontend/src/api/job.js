/**
 * Job API
 * API calls for job domain
 */
import apiClient from './index';

export const jobApi = {
  // Projects
  getProjects: () => apiClient.get('/projects'),
  getProject: (id) => apiClient.get(`/projects/${id}`),
  createProject: (data) => apiClient.post('/projects', data),
  updateProject: (id, data) => apiClient.put(`/projects/${id}`, data),
  deleteProject: (id) => apiClient.delete(`/projects/${id}`),
  
  // Jobs
  getJobs: () => apiClient.get('/jobs'),
  getJob: (id) => apiClient.get(`/jobs/${id}`),
  createJob: (data) => apiClient.post('/jobs', data),
  updateJob: (id, data) => apiClient.put(`/jobs/${id}`, data),
  deleteJob: (id) => apiClient.delete(`/jobs/${id}`),
  
  // Quotes
  getQuotes: () => apiClient.get('/quotes'),
  getQuote: (id) => apiClient.get(`/quotes/${id}`),
  createQuote: (data) => apiClient.post('/quotes', data),
  updateQuote: (id, data) => apiClient.put(`/quotes/${id}`, data),
  
  // Items
  getItems: () => apiClient.get('/items'),
  getItem: (id) => apiClient.get(`/items/${id}`),
  createItem: (data) => apiClient.post('/items', data),
  
  // Job Statuses
  getJobStatuses: () => apiClient.get('/job-statuses'),
  createJobStatus: (data) => apiClient.post('/job-statuses', data),
  
  // Test endpoint
  test: () => apiClient.get('/job/test'),
};

