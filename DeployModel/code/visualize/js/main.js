var NODES = new Array()

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
createHiDPICanvas = function (w, h, ratio) {
  if (!ratio) {
    ratio = PIXEL_RATIO
  }
  var can = document.createElement('canvas')
  can.width = w * ratio
  can.height = h * ratio
  can.style.width = w + 'px'
  can.style.height = h + 'px'
  can.getContext('2d').setTransform(ratio, 0, 0, ratio, 0, 0)
  var parent = document.getElementById('graph')
  parent.appendChild(can)
  return can
}
///////////////////////////////

///define globally cause i use multi function at first///
var WINDOWWIDTH = window.innerWidth,
  WINDOWHEIGHT = window.innerHeight
// let canvas = createHiDPICanvas(WINDOWWIDTH, WINDOWHEIGHT)
// let canvas = createHiDPICanvas(1632, 722)

function getMatrix() {
  let url = 'http://127.0.0.1:5000/getAdjMatrix'
  return fetch(url)
    .then((response) => response.json())
    .then((matrix) => {
      console.log(matrix)
      matrixToGraph(matrix)
    })
    .catch((err) => {
      console.log(err)
      throw err
    })
}

function matrixToGraph(matrix) {
  let canvas = createHiDPICanvas(800, 600)
  var CANVASWIDTH = parseInt(canvas.style.width, 10),
    CANVASHEIGHT = parseInt(canvas.style.height, 10)
  let ctx = canvas.getContext('2d')
  ctx.font = '20px Georgia'
  ctx.fillText('Linked Graph', 10, 20)
  createNodes(matrix, CANVASWIDTH, CANVASHEIGHT, ctx)
  createLines(matrix, CANVASWIDTH, CANVASHEIGHT, ctx)
}

function createNodes(matrix, CANVASWIDTH, CANVASHEIGHT, ctx) {
  // console.log(CANVASWIDTH, CANVASHEIGHT)
  for (var i = 0; i < matrix[0].length; i++) {
    var nodeName = '(' + matrix[0][i].toString() + ')'
    var nodeX = CANVASWIDTH * ((9 / 11) * (Math.random() + 0.1))
    var nodeY = CANVASHEIGHT * ((9 / 11) * (Math.random() + 0.1))
    ctx.fillText(nodeName, nodeX, nodeY)
    // console.log(nodeName, nodeX, nodeY)
    NODES.push({ nodeX: nodeX, nodeY: nodeY })
  }
}

function createLines(matrix, CANVASWIDTH, CANVASHEIGHT, ctx) {
  for (var i = 1; i < matrix.length; i++) {
    for (var j = 0; j < matrix.length; j++) {
      if (matrix[i][j] == 1) {
        ctx.beginPath()
        ctx.moveTo(NODES[i - 1].nodeX + 17, NODES[i - 1].nodeY - 5)
        ctx.lineTo(NODES[j].nodeX + 17, NODES[j].nodeY - 5)
        ctx.stroke()
      }
    }
  }
}
///initial graph///

///linked graph///
function getPathedGraph() {
  let json_file = 'result.json' // can change later
  let url = 'http://127.0.0.1:5000/getJsonLink/' + json_file
  return fetch(url)
    .then((response) => response.json())
    .then((linkAndPath) => {
      // console.log(linkAndPath.path)
      for (var i = 0; i < linkAndPath.path.length; i++)
        generatePathedGraph(i, linkAndPath.link, linkAndPath.path[i])
    })
    .catch((err) => {
      console.log(err)
      throw err
    })
}

function generatePathedGraph(number, link, path) {
  console.log(path)
  let pathedGraphCanvas = createHiDPICanvas(1632, 722)
  var CANVASWIDTH = parseInt(pathedGraphCanvas.style.width, 10),
    CANVASHEIGHT = parseInt(pathedGraphCanvas.style.height, 10)
  let ctx = pathedGraphCanvas.getContext('2d')
  ctx.font = '20px Georgia'
  ctx.fillText('Path ' + number.toString(), 10, 20)

  /// draw remained link ///
  // console.log(link)
  ctx.strokeStyle = '#D0D0D0'
  ctx.lineWidth = 1
  for (var i = 0; i < link.length; i++) {
    var targetLink = link[i]
    var startNode = targetLink[0],
      destinationNode = targetLink[1]
    ctx.beginPath()
    ctx.moveTo(NODES[startNode].nodeX + 17, NODES[startNode].nodeY - 5)
    ctx.lineTo(
      NODES[destinationNode].nodeX + 17,
      NODES[destinationNode].nodeY - 5,
    )
    ctx.stroke()
  }

  /// draw path ///
  ctx.strokeStyle = '#FF0000'
  ctx.fillStyle = '#0000C6'
  ctx.font = '20px Georgia bold'
  ctx.lineWidth = 3
  for (var i = 0; i < path.link.length - 1; i++) {
    // console.log(targetLink)
    var startNode = path.link[i],
      destinationNode = path.link[i + 1]
    ctx.beginPath()
    ctx.moveTo(NODES[startNode].nodeX + 17, NODES[startNode].nodeY - 5)
    ctx.lineTo(
      NODES[destinationNode].nodeX + 17,
      NODES[destinationNode].nodeY - 5,
    )
    ctx.stroke()
    ctx.fillText(
      path.capacity[i],
      (NODES[startNode].nodeX + NODES[destinationNode].nodeX) / 2,
      (NODES[startNode].nodeY + NODES[destinationNode].nodeY) / 2,
    )
  }

  /// draw nodes ///
  ctx.fillStyle = '#000000'
  ctx.font = '20px Georgia'
  for (var i = 0; i < NODES.length; i++) {
    ctx.fillText('(' + i + ')', NODES[i].nodeX, NODES[i].nodeY)
  }
}

$('#show-method').click(async () => {
  try {
    await getMatrix() // initial graph
    getPathedGraph() // path added
  } catch (err) {
    alert(err.message)
  }
})

$('#close-method').click(function () {
  for (var i = 0; i < $('#graph').children().length; i++)
    $('#graph').children().detach()
  NODES = new Array()
})

$('#cal-path').click(() => {
  $.blockUI({
    message: '<i class="fas fa-spinner"></i>',
    css: {
      borderWidth: '0px',
      backgroundColor: 'transparent',
      top: '50%',
      left: '50%',
      transform: 'translate(-50%, -50%)',
    },
  })

  data = {
    iter_times: $('#iter-times')[0].value,
    startID: $('#start-node')[0].value,
    destID: $('#dest-node')[0].value,
    config_loc: $('#config-loc')[0].value,
  }

  fetch('http://127.0.0.1:5000/CalPath', {
    method: 'POST',
    mode: 'cors',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  })
    .then((res) => res.text())
    .then((res) => {
      $.unblockUI()
      if (res == 'Something Wrong' || res == 'failed') {
        throw new Error(res)
      }
      handleCalPath(res)
    })
    .catch((err) => alert(err))
})

handleCalPath = (res) => {
  $('#method-text')[0].innerHTML = res
}
