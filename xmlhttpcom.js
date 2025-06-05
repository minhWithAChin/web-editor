
let responseJson = JSON.parse('{"example":"bruh"}');
let terminalStr="ready";

var xhrForm = new XMLHttpRequest();

xhrForm.onload = () => {
  // Request finished. Do processing here.
  try {
    responseJson = JSON.parse(xhrForm.response);
  } catch (error) {
    responseJson = [error]
  }
  terminalStr=responseJson.join("<br />")
  document.getElementById("terminal").innerHTML = terminalStr;
};

export function sendCode(content){
    let form = new FormData();
    console.log(content);
    form.append("code",content);
    xhrForm.open("POST", "code/");
    xhrForm.send(form);
};
export function reloadCode(){
    xhrForm.open("GET", "code/");
    xhrForm.send(null);  

};
