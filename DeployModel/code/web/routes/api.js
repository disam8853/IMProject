const express = require('express')
const fetch = require('node-fetch')
const router = express.Router()

require('dotenv').config()
const NAPA_API = process.env.NAPA_API

function callNode() {
  return fetch(NAPA_API + '/api/serve/topology/node/', {
    headers: {
      Authorization: 'Basic c2Rib3g6c2Rib3g=',
    },
  })
    .then((res) => res.json())
    .catch((err) => {
      console.log(err)
      throw err
    })
}

function callLink() {
  return fetch(NAPA_API + '/api/serve/topology/link/', {
    headers: {
      Authorization: 'Basic c2Rib3g6c2Rib3g=',
    },
  })
    .then((res) => res.json())
    .catch((err) => {
      console.log(err)
      throw err
    })
}

function callPortUsg(port_id) {
  body = {
    data_volume: 5,
    groups: 1,
    type: 'rate',
    port_id,
  }
  return fetch(NAPA_API + '/api/monitor/Port_USG/', {
    method: 'post',
    body: JSON.stringify(body),
    headers: {
      Authorization: 'Basic c2Rib3g6c2Rib3g=',
      'Content-Type': 'application/json',
    },
  })
    .then((res) => res.json())
    .catch((err) => {
      console.log(err)
      throw err
    })
}

router.get('/all-data', async (req, res, next) => {
  let node, link, port_usg
  try {
    node = await callNode()
    link = await callLink()
    port_id = []
    for (const l of link) {
      port_id.push(l.port[0].id)
    }
    console.log(port_id)
    port_usg = await Promise.all(port_id.map(callPortUsg))
  } catch (error) {
    return next(error)
  }

  port_usg = port_usg.filter((x) => !x.ERROR)

  res.json({ node, link, port_usg })
})

router.get('/switch', (req, res, next) => {
  fetch(NAPA_API + '/api/openflow/switch/', {
    headers: {
      Authorization: 'Basic c2Rib3g6c2Rib3g=',
      'Content-Type': 'application/json',
    },
  })
    .then((response) => response.json())
    .then((response) => {
      res.json(response)
    })
    .catch((err) => {
      console.log(err)
      res.sendStatus(500)
    })
})

router.get('/flowentry', (req, res, next) => {
  fetch(NAPA_API + '/api/openflow/flowentry/', {
    headers: {
      Authorization: 'Basic c2Rib3g6c2Rib3g=',
      'Content-Type': 'application/json',
    },
  })
    .then((response) => response.json())
    .then((response) => {
      res.json(response)
    })
    .catch((err) => {
      console.log(err)
      res.sendStatus(500)
    })
})

router.get('/groupentry', (req, res, next) => {
  fetch(NAPA_API + '/api/openflow/groupentry/', {
    headers: {
      Authorization: 'Basic c2Rib3g6c2Rib3g=',
      'Content-Type': 'application/json',
    },
  })
    .then((response) => response.json())
    .then((response) => {
      res.json(response)
    })
    .catch((err) => {
      console.log(err)
      res.sendStatus(500)
    })
})

router.post('/flowentry', (req, res) => {
  return fetch(NAPA_API + '/api/openflow/flowentry/', {
    method: 'post',
    body: JSON.stringify(req.body),
    headers: {
      Authorization: 'Basic c2Rib3g6c2Rib3g=',
      'Content-Type': 'application/json',
    },
  })
    .then((response) => {
      console.log(response)
      if (response.status >= 200 && response.status < 300)
        return response.json()
      else throw new Error('call post flowentry error')
    })
    .then((response) => {
      res.json(response)
    })
    .catch((err) => {
      console.log(err)
      res.sendStatus(500)
    })
})

router.put('/flowentry/:id', (req, res) => {
  return fetch(NAPA_API + '/api/openflow/flowentry/' + req.params.id, {
    method: 'put',
    body: JSON.stringify(req.body),
    headers: {
      Authorization: 'Basic c2Rib3g6c2Rib3g=',
      'Content-Type': 'application/json',
    },
  })
    .then((response) => response.json())
    .then((response) => {
      res.json(response)
    })
    .catch((err) => {
      console.log(err)
      res.sendStatus(500)
    })
})

router.delete('/flowentry/:id', (req, res) => {
  return fetch(NAPA_API + '/api/openflow/flowentry/' + req.params.id, {
    method: 'delete',
    headers: {
      Authorization: 'Basic c2Rib3g6c2Rib3g=',
      'Content-Type': 'application/json',
    },
  })
    .then((response) => {
      if (response.status >= 200 && response.status < 300) res.json(response)
      else throw new Error('delete error')
    })
    .catch((err) => {
      console.log(err)
      res.sendStatus(500)
    })
})

router.delete('/groupentry/:id', (req, res) => {
  return fetch(NAPA_API + '/api/openflow/groupentry/' + req.params.id, {
    method: 'delete',
    headers: {
      Authorization: 'Basic c2Rib3g6c2Rib3g=',
      'Content-Type': 'application/json',
    },
  })
    .then((response) => {
      if (response.status >= 200 && response.status < 300) res.json(response)
      else throw new Error('delete error')
    })
    .catch((err) => {
      console.log(err)
      res.sendStatus(500)
    })
})

router.get('/rulerecord', (req, res) => {
  fetch(NAPA_API + '/api/openflow/rulerecord/', {
    headers: {
      Authorization: 'Basic c2Rib3g6c2Rib3g=',
      'Content-Type': 'application/json',
    },
  })
    .then((response) => response.json())
    .then((response) => {
      res.json(response)
    })
    .catch((err) => {
      console.log(err)
      res.sendStatus(500)
    })
})

module.exports = router
