//services/index.js
import authController from './auth'
import userController from './user'
import { createWithVisitApiService, createBaseApiService } from './util'

const vitalController = createWithVisitApiService('vitals')
const appointmentController = createBaseApiService('appointments')

export const API = {
  auth: authController,
  user: userController,
  vital: vitalController,
  appointment: appointmentController
}
