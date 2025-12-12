/**
 * Product API
 * API calls for product domain
 */
import apiClient from './index';

export const productApi = {
  // Categories
  getCategories: () => apiClient.get('/categories'),
  getCategory: (id) => apiClient.get(`/categories/${id}`),
  createCategory: (data) => apiClient.post('/categories', data),
  updateCategory: (id, data) => apiClient.put(`/categories/${id}`, data),
  deleteCategory: (id) => apiClient.delete(`/categories/${id}`),
  
  // Products
  getProducts: (params) => apiClient.get('/products', { params }),
  getProduct: (id) => apiClient.get(`/products/${id}`),
  createProduct: (data) => apiClient.post('/products', data),
  updateProduct: (id, data) => apiClient.put(`/products/${id}`, data),
  deleteProduct: (id) => apiClient.delete(`/products/${id}`),
  
  // Variables
  getVariables: () => apiClient.get('/variables'),
  getVariable: (id) => apiClient.get(`/variables/${id}`),
  createVariable: (data) => apiClient.post('/variables', data),
  updateVariable: (id, data) => apiClient.put(`/variables/${id}`, data),
  deleteVariable: (id) => apiClient.delete(`/variables/${id}`),
  
  // Variable Options
  getOptions: (variableId) => apiClient.get(`/variables/${variableId}/options`),
  getOption: (id) => apiClient.get(`/options/${id}`),
  createOption: (data) => apiClient.post('/options', data),
  updateOption: (id, data) => apiClient.put(`/options/${id}`, data),
  deleteOption: (id) => apiClient.delete(`/options/${id}`),
  
  // Measure Types
  getMeasureTypes: () => apiClient.get('/measure-types'),
  getMeasureType: (id) => apiClient.get(`/measure-types/${id}`),
  createMeasureType: (data) => apiClient.post('/measure-types', data),
  updateMeasureType: (id, data) => apiClient.put(`/measure-types/${id}`, data),
  deleteMeasureType: (id) => apiClient.delete(`/measure-types/${id}`),
  
  // Test endpoint
  test: () => apiClient.get('/product/test'),
};

