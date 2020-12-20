const BACKEND_API = 'https://a8e4e5122cb1.ngrok.io/backend'
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

///define globally cause i use multi function at first///
var WINDOWWIDTH = window.innerWidth,
  WINDOWHEIGHT = window.innerHeight
// let canvas = createHiDPICanvas(WINDOWWIDTH, WINDOWHEIGHT)
// let canvas = createHiDPICanvas(1632, 722)

function getMatrix() {
  let url = BACKEND_API + '/getAdjMatrix'
  return fetch(url)
    .then((response) => response.json())
    .then((matrix) => {
      console.log(matrix)
      matrixToGraph(matrix)
    })
    .catch((err) => {
      throw err
    })
}

function matrixToGraph(matrix) {
  let canvas = createHiDPICanvas(800, 600, 'total-graph')
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
  let url = BACKEND_API + '/getJsonLink/' + json_file
  return fetch(url)
    .then((response) => response.json())
    .then((linkAndPath) => {
      // console.log(linkAndPath.path)
      for (var i = 0; i < linkAndPath.path.length; i++)
        generatePathedGraph(i, linkAndPath.link, linkAndPath.path[i])
    })
    .catch((err) => {
      throw err
    })
}

function generatePathedGraph(number, link, path) {
  console.log(path)
  let pathedGraphCanvas = createHiDPICanvas(800, 600, 'graph')
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

// $('#show-method').click(async () => {
//   try {
//     await getMatrix() // initial graph
//     getPathedGraph() // path added
//   } catch (err) {
//     alert(err.message)
//   }
// })

// $('#close-method').click(function () {
//   for (var i = 0; i < $('#graph').children().length; i++)
//     $('#graph').children().detach()
//   NODES = new Array()
// })

reset = () => {
  $('#total-graph').html('')
  $('#method-text').html('')
  $('#graph').html('').addClass('d-none')
}

$(document).on('keypress', function (e) {
  // press enter
  if (e.which == 13) {
    doCalPath()
  }
})

$('#cal-path').click(() => doCalPath())

doCalPath = async () => {
  reset()

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

  // data = {
  //   iter_times: $('#iter-times')[0].value,
  //   startID: $('#start-node')[0].value,
  //   destID: $('#dest-node')[0].value,
  //   config_loc: $('#config-loc')[0].value,
  // }

  try {
    await calPath()
    await showPath()
  } catch (err) {
    alert(err)
  }

  $.unblockUI()
}

calPath = async () => {
  const data = {
    iter_times: parseInt($('#iter-times').val()),
    startID: parseInt($('#start-node').val()),
    destID: parseInt($('#dest-node').val()),
    userCount: parseInt($('#int-N').val()),
    nodeR: parseInt($('#NodeR').val()),
    nodeO: parseInt($('#NodeO').val()),
    nodeP: parseInt($('#NodeP').val()),
    nodeQ: parseInt($('#NodeQ').val()),
    nodeS: parseInt($('#NodeS').val()),
  }

  try {
    data['traffic'] = await getListInputVal(1)
    data['pathCount'] = await getListInputVal(2)
  } catch (err) {
    throw err
  }

  return fetch(BACKEND_API + '/CalPath', {
    method: 'POST',
    mode: 'cors',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  })
    .then((res) => {
      if (res.status !== 200) throw new Error('Call CalPath error')
      else return res.json()
    })
    .then((res) => {
      console.log(res)
      handleCalPath(res)
    })
    .catch((err) => {
      throw err
    })
}

getListInputVal = async (id) => {
  let data = []
  await $(`.N-ints-${id}`).each(function () {
    data.push(parseInt($(this).val()) || 0)
  })
  return data
}

showPath = () => {
  return Promise.all([getMatrix(), getPathedGraph()])
    .then((res) => {
      console.log(res)
    })
    .catch((err) => {
      throw err
    })
}

handleCalPath = (res) => {
  for (const x of res.data) {
    $('#path-text').append(
      `<p class="path-item btn btn-outline-dark mr-3">${x.name}</p>`,
    )

    let txt = ''
    for (const y of x.paths) {
      txt += y.capacity === '' ? y.link : `${y.link} =(${y.capacity})> `
    }
    $('#path-info-block').append(`<p class="m-0 path-info">${txt}</p>`)
    $('#path-info-block p').hide()
  }

  $('.path-item').click(function () {
    const id = $('.path-item').index(this)
    $('#path-info-block p').hide()
    $($('#path-info-block p')[id]).show()
    showGraphById(id)
    location.hash = '#'
    location.hash = '#path-info-block'
  })
}

showGraphById = (id) => {
  $('#graph').removeClass('d-none')
  $('#graph canvas').hide()
  $($('#graph canvas')[id]).fadeIn()
}

$(document).ready(() => {
  $('#int-N').on('input', function () {
    const num = $(this).val()
    $($('.N-ints-block')[0]).html(add_str(1, num))
    $($('.N-ints-block')[1]).html(add_str(2, num))
  })
})

add_str = (id, num) => {
  let str = `<label for="N-ints-1" class="col-sm-2 col-form-label">${
    id === 1 ? 'Traffic' : 'Path Count'
  }</label><div class="col-sm-10"><div class="row">`
  for (let i = 0; i < num; i++) {
    str += `<div class="col-sm"><input type="number" class="form-control N-ints N-ints-${id} mb-2" /></div>`
  }
  str += '</div></div>'
  return str
}
