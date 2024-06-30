import http from './api'

const createBaseApiService = (resource) => {
  return {
    // Get a list of resources
    list: (config = null) => http.get(`${resource}`, config),
    // Get a single resource by its id
    get: (id, config = null) => http.get(`/${resource}/${id}`, config),
    // Create a new resource
    create: (payload) => http.post(`/${resource}`, payload),
    // Replace an existing resource with payload
    update: (id, payload) => http.put(`/${resource}/${id}`, payload),
    // Merge new payload into a resource
    patch: (id, payload) => http.patch(`/${resource}/${id}`, payload),
    // Remove a resource by its id
    remove: (id) => http.delete(`/${resource}/${id}`)
  }
}
const createWithVisitApiService = (resource) => {
  return {
    // Get a list of resources for a specific visit
    listByVisit: (visitId, config = null) => http.get(`/visits/${visitId}/${resource}`, config),
    // Get a single resource by its id within a visit
    get: (visitId, id, config = null) => http.get(`/visits/${visitId}/${resource}/${id}`, config),
    // Create a new resource within a visit
    createByVisit: (visitId, payload) => http.post(`/visits/${visitId}/${resource}`, payload),
    // Replace an existing resource with payload within a visit
    update: (visitId, id, payload) => http.put(`/visits/${visitId}/${resource}/${id}`, payload),
    // Merge new payload into a resource within a visit
    patch: (visitId, id, payload) => http.patch(`/visits/${visitId}/${resource}/${id}`, payload),
    // Remove a resource by its id within a visit
    removeByVisit: (visitId, id) => http.delete(`/visits/${visitId}/${resource}/${id}`)
  }
}

export { createBaseApiService, createWithVisitApiService }
