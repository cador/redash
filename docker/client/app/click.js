
find = function(){
  let ok = false
  if(window.location.href.indexOf('token=') > 0){
    for(let i=0;i<document.getElementsByTagName('button').length;i++){
      if(document.getElementsByTagName('button')[i].getAttribute("data-test") === "SaveButton"){
        ok = true
        document.getElementsByTagName('button')[i].click()
      }
    }
  }
  if(!ok){
    setTimeout(find, 1000)
  }
}

setTimeout(find, 1000)
