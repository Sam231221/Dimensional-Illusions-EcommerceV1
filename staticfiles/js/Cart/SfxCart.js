var updateBtns = document.getElementsByClassName('Sfx-cart')
for (var i=0; i<updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
    var productName = this.dataset.product
    var publisherId=this.dataset.pubid     
     var action = this.dataset.action


     if(user == 'AnonymousUser'){  
         addCookieItem(productName, action)
     }
     else{
         updatePaidSfxProduct(productName, publisherId,action);
     }
  })
}

function addCookieItem(productId, action){
    console.log('Customer Not logged in...')
}

function updatePaidSfxProduct(productName, publisherId,action){  
 
     var url = '/updatesfxproducts/' 
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
