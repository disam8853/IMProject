const express = require('express')
const fetch = require('node-fetch')
const router = express.Router()

require('dotenv').config()
const NAPA_API = process.env.NAPA_API

/* GET home page. */
router.get('/', function (req, res, next) {
  res.render('index', { title: 'Express' })
})

router.get('/node', (req, res, next) => {
  fetch(NAPA_API + '/api/serve/topology/node/', {
    headers: {
      Authorization: 'Basic c2Rib3g6c2Rib3g=',
    },
  })
    .then((response) => response.json())
    .then((response) => {
      console.log(response)
      res.send(response)
    })
    .catch((err) => {
      console.log(err)
      res.send({ err: err }, 500)
    })
})

module.exports = router
