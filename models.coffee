mongoose = require 'mongoose'

NotificationSchema = new mongoose.Schema
  userId: Number
  phone: Number
  givenName: String
  surName: String

module.exports.notification = mongoose.model 'Notification', NotificationSchema
