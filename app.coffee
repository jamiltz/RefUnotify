port = process.env.PORT || 3000
host = process.env.HOST || "0.0.0.0"
request = require 'request'
querystring = require "querystring"

require('zappajs') host, port, ->
  manifest = require './package.json'
  fs = require 'fs'
  mongoose = require 'mongoose'

  models = require('./models')
  Notification = models.notification

  @configure =>
    @use 'cookieParser',
      'bodyParser',
      'methodOverride',
      'session': secret: 'shhhhhhhhhhhhhh!',
      @app.router,
      'static'
    @set 'view engine', 'jade'

  @configure
    development: =>
      mongoose.connect "mongodb://#{host}/#{manifest.name}-dev"
      @use errorHandler: {dumpExceptions: on, showStack: on}
    production: =>
      mongoose.connect process.env.MONGOHQ_URL || "mongodb://#{host}/#{manifest.name}"
      @use 'errorHandler'

  @get '/': ->
    @response.redirect '/home'

  @get '/home': ->
    md = require('node-markdown').Markdown
    fs.readFile 'README.md', 'utf-8', (err, data) =>
      @render 'markdown.jade', {md: md, markdownContent: data, title: manifest.name, id: 'home', brand: manifest.name}

  @get '/source': ->
    @response.redirect manifest.source

  @get '/notifications': ->
    Notification.find {}, (err, notifications) =>
      @response.write "Error retrieving notifications:", err if err?
      @response.header "Access-Control-Allow-Origin", "*"
      @response.json notifications unless err?

  @post '/notification/create': ->
    Notification.create @body, (err, notification) =>
      @response.write "Error saving notification", notification, err if err?
      console.log notification
      request.post
        url: "http://robobo.org:8080/notify"
        body: querystring.stringify
          number: notification.phone
          body: 'You have a new match from Refugees United!'
        , (err, resp, body) =>
          console.log "Error sending message:", err if err?
          @response.header "Access-Control-Allow-Origin", "*"
          @response.json notification

  @get '/notification/list/:uid': ->
    Notification.find {userId: @params.uid}, (err, notifications) =>
      @response.write "Error retrieving notifications", err if err?
      @response.header "Access-Control-Allow-Origin", "*"
      @response.json notifications unless err?
