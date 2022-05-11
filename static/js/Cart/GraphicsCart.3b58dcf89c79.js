var updateBtns = document.getElementsByClassName('Graphics-cart')
for (var i=0; i<updateBtns.length; i++){
     updateBtns[i].addEventListener('click', function(){
     var productName = this.dataset.product
     var publisherId=this.dataset.pubid  
     var action = this.dataset.action

     if(user == 'AnonymousUser'){  
         addCookieItem(productName, action)
     }
     else{
         updateGraphicsProduct(productName,publisherId, action);
     }
  })
}

function addCookieItem(productName, action){
    console.log('Customer Not logged in...')
}

function updateGraphicsProduct(productName,publisherId, action){  
 
     var url = '/updategraphicsproducts/' 
     fetch(url,{
        method:'POST',
        headers:{
           'Content-Type': 'application/json',
           'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({'productName': productName,'publisherId':publisherId, action: action}) 
     })                                                              
     .then((response) =>{
          return response.json()   
     })
     .then((data) =>{
          console.log('data:',data)  
          location.reload()
     })
 }
 
