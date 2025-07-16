
let responseJson = JSON.parse('{"example":"bruh"}');
let terminalStr="ready";
let execBool=false;
let cancelled=false;
let heartID=0;
let pulse_period=2;

var xhrForm = new XMLHttpRequest();

xhrForm.onload = () => {
  // Request finished. Do processing here.
  try {
    responseJson = JSON.parse(xhrForm.response);
    if(responseJson.length > 2){
      let done = responseJson[0];
      let exec = responseJson[1];
      console.log(responseJson.join(" - "));
      displayToTerminal(responseJson[2]);
      if (done && exec && execBool){ // Heartbeat soll nur stoppen ,wenn Code executiert wurde und die Antwort von exec True ist
	clearInterval(heartID);
	cancelled=false;
	execBool=false;
      }
    }else{
      displayToTerminal(responseJson)
    }
  } catch (error) {
    responseJson = [error]
    displayToTerminal(responseJson)
  }
};

function heartbeat(){
    let form = new FormData();
    console.log("heartbeat sent");
    form.append("cancelled",cancelled);
    xhrForm.open("POST", "../code/exec");
    xhrForm.send(form);
}

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
    if(!execBool){
    xhrForm.open("GET", "../code/exec");
    xhrForm.send(null);  
    execBool=true
    cancelled=false
    heartID=setInterval(heartbeat,1000*pulse_period)}else{
    displayToTerminal(["Code läuft schon","drücke auf Cancel um ihn abzubrechen"])}

};
export function cancExec(){
      if(execBool){
          cancelled=true}else{
      displayToTerminal(["Lade den Code zuerst hoch","und führe ihn aus"])}

};
