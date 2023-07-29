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
        handleAuthData(authData,getProductList)
    })
    .catch(err=> {
        console.log('err', err)
    })
}

const getFetchOptions = (method,body)=>{
    const access_token = localStorage.getItem('access')
    return{
        method: method ? method : "GET",
        headers:{
            'Content-Type': "application/json",
            Authorization:"Bearer " + access_token
        },
        body : body? body : null
    }
}


const handleAuthData = (data,callback) => {
    localStorage.setItem('access',data.access)
    localStorage.setItem('refresh',data.refresh)
    if(callback){
        callback()
    }
}

const isTokenValid = (code)=>{
    if(code && code === "token_not_valid"){
        localStorage.removeItem('access')
        localStorage.removeItem('refresh')
        alert("Please login again. Token is no longer valid")
        return false
    }
    return true
}


const getProductList = ()=>{
    const product_endpoint = `${baseEndpoint}/products/`
    const options = getFetchOptions()
    fetch(product_endpoint, options)
    .then(res=>res.json())
    .then(data=>{
        const validData = isTokenValid(data?.code??'')
        if(validData) {
            renderProduct(data.results)
        }
    })
    .catch(err=>console.log(err))
}


const renderProduct = (data)=>{
    if(productList){
        function generateListItemsHTML(data) {
            return data.map(product => `<li>${product.title}</li>`).join('');
          }
          productList.innerHTML = generateListItemsHTML(data);
    }
}



const validateJWTToken = ()=>{
    const validate_endpoint = `${baseEndpoint}/token/verify/`
    const bodyVerify = JSON.stringify({token : localStorage.getItem('access')})
    const options = getFetchOptions('POST',bodyVerify);
    fetch(validate_endpoint, options)
    .then(res=>res.json())
    .then(data => {
        const token_valid = isTokenValid(data?.code??'')
        if(token_valid) {
            getProductList()
        }else{
            refreshToken()
        }
    })
}

const refreshToken = ()=>{
    const refresh_endpoint = `${baseEndpoint}/token/refresh/`
    const body = JSON.stringify({token : localStorage.getItem('refresh')})
    const options = getFetchOptions('POST',body)
    fetch(refresh_endpoint,options)
    .then(res=>res.json())
    .then(data=>{
        const valid_token =  isTokenValid(data?.code??'')
        if(valid_token){
            localStorage.setItem('access',data.access)
            localStorage.setItem('refresh',data.refresh)
        }else{
            alert("Please login again. Token is no longer valid")
        }
    })
}

validateJWTToken()