const express = require('express')
const fetch = require('node-fetch')
const router = express.Router()

require('dotenv').config()
const NAPA_API = process.env.NAPA_API

router.get('/', function (req, res, next) {
  res.render('index')
})

module.exports = router
