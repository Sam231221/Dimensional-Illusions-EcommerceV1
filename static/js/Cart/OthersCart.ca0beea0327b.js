var updateBtns = document.getElementsByClassName('spectrum-cart')
for (var i=0; i<updateBtns.length; i++){
     updateBtns[i].addEventListener('click', function(){
     var productName = this.dataset.product
     var publisherId=this.dataset.pubid  
     var action = this.dataset.action

     if(user == 'AnonymousUser'){  
         addCookieItem(productName, action)
     }
     else{
         updateSpectrum(productName, publisherId,action);
     }
  })
}


//FOR GUEST USERS
function addCookieItem(productId, action){
    console.log('Customer Not logged in...')
}

function updateSpectrum(productName,publisherId, action){  

     var url = '/updateSpectrum/'  
     fetch(url,{
        method:'POST',
        headers:{
           'Content-Type': 'application/json',
           'X-CSRFToken': csrftoken,
 
        },
        body:JSON.stringify({'productName': productName, 'publisherId':publisherId,action: action}) 
     })                                                            
     .then((response) =>{
          return response.json()  
     })
     .then((data) =>{
          console.log('data:',data)  
          location.reload()
     })
 }
 
 var updateBtns = document.getElementsByClassName('lyricstemplate-cart')
for (var i=0; i<updateBtns.length; i++){
     updateBtns[i].addEventListener('click', function(){
     var productName = this.dataset.product
     var publisherId=this.dataset.pubid  
     var action = this.dataset.action

     if(user == 'AnonymousUser'){  
         addCookieItem(productName, action)
     }
     else{
         updatelyricstemplate(productName,publisherId, action);
     }
  })
}

function addCookieItem(productId, action){
    console.log('Customer Not logged in...')
}

function updatelyricstemplate(productName, publisherId,action){  
 
     var url = '/updateLyricsTemplate/'  
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
 