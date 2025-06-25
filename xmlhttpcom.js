
let responseJson = JSON.parse('{"example":"bruh"}');
let terminalStr="ready";

var xhrForm = new XMLHttpRequest();

xhrForm.onload = () => {
  // Request finished. Do processing here.
  try {
    responseJson = JSON.parse(xhrForm.response);
    if(responseJson.length > 1){
      console.log(responseJson[1])
      displayToTerminal(responseJson[1])
    }else{
      displayToTerminal(responseJson)
    }
  } catch (error) {
    responseJson = [error]
    displayToTerminal(responseJson)
  }
};

function displayToTerminal(responseJson){
  terminalStr=responseJson.join("<br />")
  document.getElementById("terminal").innerHTML = terminalStr;
}

export function sendCode(content){
    let form = new FormData();
    console.log(content);
    form.append("code",content);
    xhrForm.open("POST", "../code/");
    xhrForm.send(form);
};
export function getCode(){
    xhrForm.open("GET", "../code/");
    xhrForm.send(null);  

};
export function execCode(){
    xhrForm.open("GET", "../code/exec");
    xhrForm.send(null);  

};
