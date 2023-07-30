const loginForm = document.getElementById('login-form')
const productList = document.getElementById('product-list')
const searchForm = document.getElementById('search-form')
const baseEndpoint = "http://localhost:8000/api"
if (loginForm) {
    loginForm.addEventListener('submit', handleLogin)
}

if (searchForm) {
    searchForm.addEventListener('submit', handleSearch)
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

function handleSearch(event) {
    event.preventDefault()

    let forData = new FormData(searchForm)
    let data = Object.fromEntries(forData)
    let params = new URLSearchParams(data)

    const SearchEndpoint = `${baseEndpoint}/search/?${params}`

    const headers = {
        "Content-Type": "application/json",
    }

    const authToken = localStorage.getItem('access')

    if(authToken){
        headers['Authorization'] = `Bearer ${authToken}`
    }

    const options = {
        method: "GET",
        headers: headers,
    }
    fetch(SearchEndpoint, options) //  Promise
    .then(response=>{
        return response.json()
    })
    .then(data => {
        console.log(data);
        const tokenIsValid = isTokenValid(data.code)
        console.log(tokenIsValid);
        if(tokenIsValid && productList){
            if(data&&data.hits){
                renderProduct(data.hits)
            }else{
                productList.innerHTML = "<li>No product found</li>"
            }
        }
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
    const token  = localStorage.getItem('access')
    if(token){
        const bodyVerify = JSON.stringify({token : token})
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
    }else{
        alert("You have to login to see product list")
    }
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

const searchClient = algoliasearch('BNO1XNMAW1', '74a0bb4147c05d63c60f07e330d265e9');

const search = instantsearch({
  indexName: 'sippy_Product',
  searchClient,
});

search.addWidgets([
  instantsearch.widgets.searchBox({
    container: '#searchbox',
  }),

    instantsearch.widgets.refinementList({
        container:"#user-list",
        attribute:"user"
    }),
    instantsearch.widgets.clearRefinements({
        container:"#clear-refinements",
    }),

  instantsearch.widgets.hits({
    container: '#hits',
    templates:{
        item:`
        <div>
            <div>{{#helpers.highlight}}{"attribute":"title"}{{/helpers.highlight}}</div>
            <div>{{#helpers.highlight}}{"attribute":"body"}{{/helpers.highlight}}</div>
            <p>{{user}</p><p>\${{price}}
        </div>`
    }
  })
]);

search.start();
