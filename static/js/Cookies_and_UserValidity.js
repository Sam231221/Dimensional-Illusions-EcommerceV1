var user= '{{request.user}}'  //<!--defining user and assiginig in cart part-->
// <!--creating csrftoken-->
  function getToken(name){
  var cookieValue = null;
  if(document.cookie && document.cookie !==''){
      var cookies = document.cookie.split(';');
      for(var i=0; i< cookies.length; i++){
          var cookie = cookies[i].trim();
          //Does this cookie string begin with the name we want?
          if(cookie.substring(0,name.length + 1)===(name+'='))
            {
            cookieValue = decodeURIComponent(cookie.substring(
              name.length +=1));
             break;
            }
          }
      }
     return cookieValue;
  }

  var csrftoken =getToken('csrftoken'); //acessing csrf token from functioni upadteuserorder in cart.jss this way item added is stored in backend
  
  function getCookie(name){
      //Split cookie string and get all indiviudal name=value pairs in an array
      var cookieArr = document.cookie.split(";");

      //Loop through the array elements
      for(var i=0; i< cookieArr.length; i++){
          var cookiePair = cookieArr[i].split("=");

      /* Removing whitespace at the begining of the cookije name
      and compare it with the given string */
          if(name == cookiePair[0].trim()){
         //Decode the cookie value and return
             return decodeURIComponent(cookiePair[1]);
          } 
      }
  // Return null if not found
  return null;
  }

  var cart = JSON.parse(getCookie('cart'))
  if(cart == undefined){
     cart = {}  //cart as empty dicitonary
     console.log('YourShoppingCart was created')  //not goona display this becoz we have a cart for it
    //document.cookie is a Javascript method to create a cookie.Cart is aobject we need to convert it into string and we wanna assign it ot our all pages.So for that domain=;path=/''.
     document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"  
  }
  //console.log('Cart:',cart)
  