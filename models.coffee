mongoose = require 'mongoose'

NotificationSchema = new mongoose.Schema
  profileId: Number
  phone: Number
  givenName: String
  surName: String
  genderId: Number

module.exports.notification = mongoose.model 'Notification', NotificationSchema
