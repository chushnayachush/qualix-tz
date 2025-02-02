const submitButtonElement = document.getElementById('submit-btn');
const requestIdElement = document.getElementById('api-req-id');
const methodElement = document.getElementById('api-method');
const paramsElement = document.getElementById('api-params');
const responseElement = document.getElementById('api-response');
const copyButtonElement = document.getElementById('api-response-copy');

submitButtonElement.addEventListener('click', async e => {
  e.preventDefault()
  try {
    if (paramsElement.value) {
      params = JSON.parse(paramsElement.value)
    } else {
      params = null
    }
    const v = {
      method: methodElement.value,
      id: requestIdElement.value,
      params: params,

    };
    const response = await fetch('send_request/', {
      method: 'post',
      body: JSON.stringify(v)
    }).then(r => r.json());
    responseElement.value = JSON.stringify(response, null, 4);
  } catch (error) {
    if (error instanceof SyntaxError){
      alert("Params should be valid JSON");
    } else {
      alert(error.message)
    }
  }
  });

copyButtonElement.addEventListener('click', async e => {
  e.preventDefault()
  navigator.clipboard.writeText(responseElement.value);
});


