//services/index.js
import authController from './auth'
import userController from './user'
import { createWithVisitApiService, createBaseApiService } from './util'

const vitalController = createWithVisitApiService('vitals')
const labtestController = createWithVisitApiService('labtests')
const appointmentController = createBaseApiService('appointments')
const visitController = createBaseApiService('visits')

export const API = {
  auth: authController,
  user: userController,
  visit: visitController,
  labtest: labtestController,
  appointment: appointmentController,
  vital: vitalController
}
