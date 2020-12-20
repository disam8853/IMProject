const express = require('express')
const fetch = require('node-fetch')
const router = express.Router()

require('dotenv').config()
const NAPA_API = process.env.NAPA_API

router.get('/', function (req, res, next) {
  res.render('index')
})

router.get('/flow', (req, res) => {
  res.render('realtime')
})

router.get('/flowtable', (req, res) => {
  res.render('table')
})

router.get('/newentry', (req, res, next) => {
  fetch(NAPA_API + '/api/openflow/switch/', {
    headers: {
      Authorization: 'Basic c2Rib3g6c2Rib3g=',
      'Content-Type': 'application/json',
    },
  })
    .then((response) => response.json())
    .then((response) => {
      let switch_name = []
      for (const e of response) {
        switch_name.push({
          id: e.id,
          name: e.name,
        })
      }

      res.render('newentry', { switch_name })
    })
    .catch((err) => {
      next(err)
    })
})

module.exports = router
