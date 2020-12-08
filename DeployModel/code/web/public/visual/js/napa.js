fetch('http://localhost:3000/api/node/')
  .then((res) => res.json())
  .then((res) => {
    console.log(res)
  })
  .catch((err) => {
    console.log(err)
  })
