var updateBtns = document.getElementsByClassName('Vfx-cart')
for (var i=0; i<updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        var productName = this.dataset.product
        var publisherId=this.dataset.pubid 
        var poid=this.dataset.poid         
        var action = this.dataset.action
        
     if(user == 'AnonymousUser'){  
         addCookieItem(productName, action)
     }
     else{
         updatePaidVfxProduct(productName,publisherId,poid, action);
     }
  })
}

function addCookieItem(productId, action){
    console.log('Customer Not logged in...')
}

function updatePaidVfxProduct(productName,publisherId,poid, action){  
    data = {
        "productName": productName,
        "publisherId":publisherId,
        "poid":poid,
        "action": action
    }
     var url = '/updatevfxproducts/' 
     fetch(url,{
        method:'POST',
        headers:{
           'Content-Type': 'application/json',
           'X-CSRFToken': csrftoken,
 
        },
        body:data
     })                                                                  //stringify is used for that
     .then((response) =>{
          return response.json()   //then we wanna send back the jsonresponse that we defined in updateItem function
     })
     .then((data) =>{
          console.log('data:',data)  //then we need to console to be able to see the JSONresponse (i.e data,Item was added.)

     })
 }
 