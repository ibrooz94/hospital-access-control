//services/index.js
import authController from './auth'
import userController from './user'
import { createWithVisitApiService } from './util'

const vitalController = createWithVisitApiService('vital')

export const API = {
  auth: authController,
  user: userController,
  vital: vitalController
}
