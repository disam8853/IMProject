var NODES = new Array()
var FLOWS = new Array()
/////for canvas quality/////
var PIXEL_RATIO = (function () {
  var ctx = document.createElement('canvas').getContext('2d'),
    dpr = window.devicePixelRatio || 1,
    bsr =
      ctx.webkitBackingStorePixelRatio ||
      ctx.mozBackingStorePixelRatio ||
      ctx.msBackingStorePixelRatio ||
      ctx.oBackingStorePixelRatio ||
      ctx.backingStorePixelRatio ||
      1

  return dpr / bsr
})()

createHiDPICanvas = function (w, h, el_id, ratio) {
  if (!ratio) {
    ratio = PIXEL_RATIO
  }
  var can = document.createElement('canvas')
  can.width = w * ratio
  can.height = h * ratio
  can.style.width = w + 'px'
  can.style.height = h + 'px'
  can.getContext('2d').setTransform(ratio, 0, 0, ratio, 0, 0)
  var parent = document.getElementById(el_id)
  parent.appendChild(can)
  return can
}
///////////////////////////////

function formatBytes(bytes, decimals = 2) {
  if (bytes === 0) return '0 Bytes'

  const k = 1024
  const dm = decimals < 0 ? 0 : decimals
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']

  const i = Math.floor(Math.log(bytes) / Math.log(k))

  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i]
}

function canvasArrow(context, fromx, fromy, tox, toy, color) {
  var headlen = 20 // length of head in pixels
  var dx = tox - fromx
  var dy = toy - fromy
  var midx = (fromx + tox) / 2
  var midy = (fromy + toy) / 2
  var angle = Math.atan2(dy, dx)
  context.strokeStyle = color
  context.lineWidth = 3
  context.moveTo(fromx, fromy)
  context.lineTo(tox, toy)
  context.moveTo(midx, midy)
  context.lineTo(
    midx - headlen * Math.cos(angle - Math.PI / 6),
    midy - headlen * Math.sin(angle - Math.PI / 6),
  )
  context.moveTo(midx, midy)
  context.lineTo(
    midx - headlen * Math.cos(angle + Math.PI / 6),
    midy - headlen * Math.sin(angle + Math.PI / 6),
  )
}

function getRealtimeTopo(container, nodes, flows, values) {
  let canvas = createHiDPICanvas(2400, 1800, container)
  let ctx = canvas.getContext('2d')
  var CANVASWIDTH = parseInt(canvas.style.width, 10),
    CANVASHEIGHT = parseInt(canvas.style.height, 10)
  ////////////////dealing nodes//////////////////
  for (var i = 0; i < nodes.length; i++) {
    var nodeX = CANVASWIDTH * ((9 / 11) * (Math.random() + 0.1))
    var nodeY = CANVASHEIGHT * ((9 / 11) * (Math.random() + 0.1))
    NODES.push({
      name: nodes[i].name,
      id: nodes[i].id,
      nodeX: nodeX,
      nodeY: nodeY,
    })
  }
  // console.log(NODES)
  ///////////////dealing flows///////////////////
  for (var i = 0; i < flows.length; i++) {
    var oriNode, destNode
    for (var j = 0; j < NODES.length; j++) {
      if (flows[i].port[0].switch == NODES[j].id) oriNode = NODES[j]
      else if (flows[i].port[1].switch == NODES[j].id) destNode = NODES[j]
    }
    FLOWS.push({
      id: flows[i].id,
      bandwidth: flows[i].bandwidth,
      oriPort: flows[i].port[0].id,
      oriNode: oriNode,
      destNode: destNode,
      flowValue: 0,
    })
  }
  // console.log(FLOWS)
  ///////////////dealing value////////////////////
  // console.log(values)
  for (var i = 0; i < values.length; i++) {
    for (var j = 0; j < FLOWS.length; j++) {
      if (values[i].id == FLOWS[j].oriPort) {
        // for(var k = 0; k < values[i].usage.tx.length; k++) {
        //   if (values[i].usage.tx[k].value > 0)
        //     FLOWS[j].flowValue = values[i].usage.tx[k].value
        // }
        if (values[i].usage.tx[values[i].usage.tx.length - 1].value > 0)
          FLOWS[j].flowValue =
            values[i].usage.tx[values[i].usage.tx.length - 1].value
      }
    }
  }

  plotTopo(ctx)
}

function updateRealtimeTopo(container, nodes, flows, values) {
  let canvas = createHiDPICanvas(2400, 1800, container)
  let ctx = canvas.getContext('2d')
  var CANVASWIDTH = parseInt(canvas.style.width, 10),
    CANVASHEIGHT = parseInt(canvas.style.height, 10)
  ////////////////dealing nodes//////////////////
  var updateNodes = new Array()
  for (var i = 0; i < nodes.length; i++) {
    for (var j = 0; j < NODES.length; j++) {
      /////////node still exists//////////
      if (nodes[i].id == NODES[j].id) 
        updateNodes.push(NODES[j])
      /////////new nodes//////////////////
      else {
        var nodeX = CANVASWIDTH * ((9 / 11) * (Math.random() + 0.1))
        var nodeY = CANVASHEIGHT * ((9 / 11) * (Math.random() + 0.1))
        updateNodes.push({
          name: nodes[i].name,
          id: nodes[i].id,
          nodeX: nodeX,
          nodeY: nodeY,
        })
      }
    }
  }
  NODES = updateNodes
  // console.log(NODES)

  ///////////////dealing flows///////////////////
  var updateFlows = new Array()
  for (var i = 0; i < flows.length; i++) {
    for (var j = 0; j < FLOWS.length; j++) {
      /////////flow still exists//////////
      if (flows[i].id == FLOWS[j].id) {
        FLOWS[j].flowValue = 0
        updateFlows.push(FLOWS[j])
      }
      /////////new flows//////////////////
      else {
        var oriNode, destNode
        for (var j = 0; j < NODES.length; j++) {
          if (flows[i].port[0].switch == NODES[j].id) oriNode = NODES[j]
          else if (flows[i].port[1].switch == NODES[j].id) destNode = NODES[j]
        }
        updateFlows.push({
          id: flows[i].id,
          bandwidth: flows[i].bandwidth,
          oriPort: flows[i].port[0].id,
          oriNode: oriNode,
          destNode: destNode,
          flowValue: 0,
        })
      }
    }
  }
  FLOWS = updateFlows
  // console.log(FLOWS)

  ///////////////dealing value////////////////////
  // console.log(values)
  for (var i = 0; i < values.length; i++) {
    for (var j = 0; j < FLOWS.length; j++) {
      if (values[i].id == FLOWS[j].oriPort) {
        // for(var k = 0; k < values[i].usage.tx.length; k++) {
        //   if (values[i].usage.tx[k].value > 0)
        //     FLOWS[j].flowValue = values[i].usage.tx[k].value
        // }
        if (values[i].usage.tx[values[i].usage.tx.length - 1].value > 0)
          FLOWS[j].flowValue =
            values[i].usage.tx[values[i].usage.tx.length - 1].value
      }
    }
  }
  plotTopo(ctx)
}

function plotTopo(ctx) {
  let low = '#00EC00',
    overHundred = '#2894FF',
    mediumLow = '#F9F900',
    mediumHigh = '#FF0000',
    high = '#921AFF',
    none = '#E0E0E0'
  ctx.font = '20px bold Georgia'
  ////////////////plot flows///////////////
  for (var i = 0; i < FLOWS.length; i++) {
    ctx.beginPath()
    canvasArrow(
      ctx,
      FLOWS[i].oriNode.nodeX,
      FLOWS[i].oriNode.nodeY,
      FLOWS[i].destNode.nodeX,
      FLOWS[i].destNode.nodeY,
      none,
    )
    ctx.stroke()
  }
  for (var i = 0; i < FLOWS.length; i++) {
    if (FLOWS[i].flowValue != 0) {
      if (FLOWS[i].flowValue >= 100 && FLOWS[i].flowValue / FLOWS[i].bandwidth <= 0.25) {
        ctx.beginPath()
        canvasArrow(
          ctx,
          FLOWS[i].oriNode.nodeX,
          FLOWS[i].oriNode.nodeY,
          FLOWS[i].destNode.nodeX,
          FLOWS[i].destNode.nodeY,
          overHundred,
        )
        ctx.stroke()
      } else if (FLOWS[i].flowValue / FLOWS[i].bandwidth <= 0.25) {
        ctx.beginPath()
        canvasArrow(
          ctx,
          FLOWS[i].oriNode.nodeX,
          FLOWS[i].oriNode.nodeY,
          FLOWS[i].destNode.nodeX,
          FLOWS[i].destNode.nodeY,
          low,
        )
        ctx.stroke()
      } else if (FLOWS[i].flowValue / FLOWS[i].bandwidth <= 0.5) {
        ctx.beginPath()
        canvasArrow(
          ctx,
          FLOWS[i].oriNode.nodeX,
          FLOWS[i].oriNode.nodeY,
          FLOWS[i].destNode.nodeX,
          FLOWS[i].destNode.nodeY,
          mediumLow,
        )
        ctx.stroke()
      } else if (FLOWS[i].flowValue / FLOWS[i].bandwidth <= 0.75) {
        ctx.beginPath()
        canvasArrow(
          ctx,
          FLOWS[i].oriNode.nodeX,
          FLOWS[i].oriNode.nodeY,
          FLOWS[i].destNode.nodeX,
          FLOWS[i].destNode.nodeY,
          mediumHigh,
        )
        ctx.stroke()
      } else {
        ctx.beginPath()
        canvasArrow(
          ctx,
          FLOWS[i].oriNode.nodeX,
          FLOWS[i].oriNode.nodeY,
          FLOWS[i].destNode.nodeX,
          FLOWS[i].destNode.nodeY,
          high,
        )
        ctx.stroke()
      }
    }
  }
  ///////////////plot values///////////////
  for (var i = 0; i < FLOWS.length; i++) {
    if (FLOWS[i].flowValue != 0) {
      var textX = (FLOWS[i].oriNode.nodeX + FLOWS[i].destNode.nodeX) / 2,
        textY = (FLOWS[i].oriNode.nodeY + FLOWS[i].destNode.nodeY) / 2
      ctx.fillText(formatBytes(FLOWS[i].flowValue), textX, textY)
    }
  }
  ///////////////plot nodes////////////////
  for (var i = 0; i < NODES.length; i++) {
    ctx.fillText(NODES[i].name, NODES[i].nodeX - 50, NODES[i].nodeY + 10)
  }
}

$(document).ready(async () => {
  let nodes, flows, values
  try {
    const res = await getDate()
    nodes = res.nodes
    flows = res.flows
    values = res.values
  } catch (err) {
    alert('error! Please refresh!')
    console.log(err)
  }
  getRealtimeTopo('realtimeGraph', nodes, flows, values)
  $('.loding').hide()

  setInterval(async function() {
    try {
      const res = await getDate()
      nodes = res.nodes
      flows = res.flows
      values = res.values
    } catch (err) {
      alert('error! Please refresh!')
      console.log(err)
    }
    updateRealtimeTopo('realtimeGraph', nodes, flows, values)
  }, 30000)
})

function getDate() {
  return fetch('/api/all-data')
    .then((res) => res.json())
    .then((res) => {
      console.log(res)
      return { nodes: res.node, flows: res.link, values: res.port_usg }
    })
    .catch((err) => {
      console.log(err)
      throw err
    })
}
