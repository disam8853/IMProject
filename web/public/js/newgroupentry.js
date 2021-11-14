$('#submit').click(async (el) => {
  $('.loading').fadeIn()
  console.log(el)
  await postFloeentry()
})

function postFloeentry() {
  let buckets = []
  if ($('#OUTPUT').val() !== '')
    buckets.push({ actions: [{ type: 'OUTPUT', port: $('#OUTPUT').val() }] })

  const data = [
    {
      group_id: $('#gid').val(),
      sw: $('#switch').val(),
      groups: 1,
      type: $('#type').val(),
      buckets,
    },
  ]

  console.log(data)

  return fetch('/api/groupentry', {
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
      $('.alert').hide()
      if (res.status !== 200) throw new Error('Create group entry error')
      else return res.json()
    })
    .then((res) => {
      console.log(res)
      $('.alert-success').show()
      $('.alert-success').html('Create group entry success.')
    })
    .catch((err) => {
      $('.alert-danger').show()
      $('.alert-danger').html(err)
    })
}
