const loginForm = document.getElementById('login-form')
const productList = document.getElementById('product-list')
const baseEndpoint = "http://localhost:8000/api"
if (loginForm) {
    // handle this login form
    loginForm.addEventListener('submit', handleLogin)
}

function handleLogin(event) {
    event.preventDefault()
    const loginEndpoint = `${baseEndpoint}/token/`
    let loginFormData = new FormData(loginForm)
    let loginObjectData = Object.fromEntries(loginFormData)
    let bodyStr = JSON.stringify(loginObjectData)
    const options = {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: bodyStr
    }
    fetch(loginEndpoint, options) //  Promise
    .then(response=>{
        return response.json()
    })
    .then(authData => {
        handleAuthData(authData)
    })
    .catch(err=> {
        console.log('err', err)
    })
}

const handleAuthData = (data) => {
    localStorage.setItem('access',data.access)
    localStorage.setItem('refresh',data.refresh)
    getProductList()
}

const getProductList = ()=>{
    const product_endpoint = `${baseEndpoint}/products/`
    const access_token = localStorage.getItem('access')
    if(access_token) {
        const options = {
            method:"GET",
            headers:{
                'Content-Type': "application/json",
                Authorization:"Bearer " + access_token
            }
        }
        fetch(product_endpoint, options)
        .then(res=>res.json())
        .then(data=>{
            renderProduct(data.results)
        })
        .catch(err=>console.log(err))

    }
}


const renderProduct = (data)=>{
    if(productList){
        function generateListItemsHTML(data) {
            return data.map(product => `<li>${product.title}</li>`).join('');
          }
          
          // Set the innerHTML of the <ul> element with the generated HTML content
          productList.innerHTML = generateListItemsHTML(data);
    }
}