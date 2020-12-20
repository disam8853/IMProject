$('#submit').click(async (el) => {
  $('.loading').fadeIn()
  console.log(el)
  await postFloeentry()
})

function postFloeentry() {
  const match = {}
  let actions = []
  if ($('#in_port').val() !== '') match['in_port'] = $('#in_port').val()
  if ($('#eth_src').val() !== '') match['eth_src'] = $('#eth_src').val()
  if ($('#eth_dst').val() !== '') match['eth_dst'] = $('#eth_dst').val()
  if ($('#eth_type').val() !== '') match['eth_type'] = $('#eth_type').val()
  if ($('#ip_dscp').val() !== '') match['ip_dscp'] = $('#ip_dscp').val()
  if ($('#ip_ecn').val() !== '') match['ip_ecn'] = $('#ip_ecn').val()
  if ($('#ip_proto').val() !== '') match['ip_proto'] = $('#ip_proto').val()
  if ($('#ipv4_src').val() !== '') match['ipv4_src'] = $('#ipv4_src').val()
  if ($('#ipv4_dst').val() !== '') match['ipv4_dst'] = $('#ipv4_dst').val()
  if ($('#GOTO_TABLE').val() !== '')
    actions.push({ type: 'GOTO_TABLE', table_id: $('#GOTO_TABLE').val() })
  if ($('#OUTPUT').val() !== '')
    actions.push({ type: 'OUTPUT', port: $('#OUTPUT').val() })

  const data = [
    {
      sw: $('#switch').val(),
      is_permanent: true,
      groups: 1,
      priority: parseInt($('#priority').val()),
      buffer_id: null,
      cookie_mask: null,
      match,
      actions,
    },
  ]

  console.log(data)

  return fetch('/api/flowentry', {
    method: 'POST',
    mode: 'cors',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  })
    .then((res) => {
      window.scroll(0, 0)
      $('.loading').fadeOut()
      if (res.status !== 200) throw new Error('Create flow entry error')
      else return res.json()
    })
    .then((res) => {
      console.log(res)
      $('.alert-success').show()
      $('.alert-success').html('Create flow entry success.')
    })
    .catch((err) => {
      $('.alert-danger').show()
      $('.alert-danger').html(err)
    })
}
