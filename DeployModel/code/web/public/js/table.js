var Switches = new Array()
var FlowEntries = new Array()
var GroupEntries = new Array()

function fillFlowEntry(switches, flowEntries) {
  let targetTable = $('#flowEntryBody')
  for (var i = 0; i < switches.length; i++) {
    for (var j = 0; j < flowEntries.length; j++) {
      if (switches[i].id == flowEntries[j].sw) {
        var appendToTable = '<tr><td>'
        appendToTable += switches[i].name
        appendToTable += '</td><td>'
        appendToTable += flowEntries[j].table_id
        appendToTable += '</td><td>'
        appendToTable += flowEntries[j].priority
        appendToTable += '</td><td>'
        appendToTable += JSON.stringify(flowEntries[j].match)
        appendToTable += '</td><td>'
        for (var k = 0; k < flowEntries[j].actions.length; k++)
          appendToTable += JSON.stringify(flowEntries[j].actions[k])
        appendToTable += '</td><td>'
        appendToTable += flowEntries[j].flags
        appendToTable += '</td><td>'
        appendToTable += flowEntries[j].hard_timeout
        appendToTable += '</td><td>'
        appendToTable += flowEntries[j].idle_timeout
        appendToTable += '</td><td>'
        appendToTable += flowEntries[j].cookie
        appendToTable += `</td><td><button type="button" class="btn btn-light delete-btn">DELETE<input type="hidden" value="${flowEntries[j].id}"></button></td></tr>`

        targetTable.append(appendToTable)
      }
    }
  }
}

function fillGroupEntry(switches, groupEntries) {
  let targetTable = $('#groupEntryBody')
  for (var i = 0; i < switches.length; i++) {
    for (var j = 0; j < groupEntries.length; j++) {
      if (switches[i].id == groupEntries[j].sw) {
        var appendToTable = '<tr><td>'
        appendToTable += switches[i].name
        appendToTable += '</td><td>'
        appendToTable += groupEntries[j].group_id
        appendToTable += '</td><td>'
        appendToTable += groupEntries[j].type
        appendToTable += '</td><td>'
        for (var k = 0; k < groupEntries[j].buckets.length; k++)
          appendToTable += JSON.stringify(groupEntries[j].buckets[k]) + '<br>'
        appendToTable += '</td><td>'
        appendToTable += groupEntries[j].status
        appendToTable += `</td><td><button type="button" class="btn btn-light delete-btn">DELETE<input type="hidden" value="${groupEntries[j].id}"></button></td></tr>`

        targetTable.append(appendToTable)
      }
    }
  }
}

function getSwitches() {
  return fetch('/api/switch/')
    .then((res) => {
      return res.json()
    })
    .then((switchData) => {
      return switchData
    })
}

function getFlowEntries() {
  return fetch('/api/flowentry/')
    .then((res) => {
      return res.json()
    })
    .then((flowEntryData) => {
      return flowEntryData
    })
}

function getGroupEntries() {
  return fetch('/api/groupentry/')
    .then((res) => {
      return res.json()
    })
    .then((groupEntryData) => {
      return groupEntryData
    })
}

$(document).ready(async () => {
  try {
    Switches = await getSwitches()
    FlowEntries = await getFlowEntries()
    GroupEntries = await getGroupEntries()
  } catch (err) {
    alert('Error. Please refresh.')
  }

  console.log(Switches)
  console.log(FlowEntries)
  console.log(GroupEntries)

  fillFlowEntry(Switches, FlowEntries)
  fillGroupEntry(Switches, GroupEntries)

  $('#flowEntryBody .delete-btn').click(function (el) {
    if (confirm('您是否確定要刪除？')) {
      const id = $(this).children()[0].value
      deleteFlowEntry(id)
    }
  })

  $('#groupEntryBody .delete-btn').click(function (el) {
    if (confirm('您是否確定要刪除？')) {
      const id = $(this).children()[0].value
      deleteGroupEntry(id)
    }
  })
})

function deleteFlowEntry(id) {
  return fetch('/api/flowentry/' + id, { method: 'delete' })
    .then((res) => res.json())
    .catch((err) => {
      console.log(err)
    })
}

function deleteGroupEntry(id) {
  return fetch('/api/groupentry/' + id, { method: 'delete' })
    .then((res) => res.json())
    .catch((err) => {
      console.log(err)
    })
}
