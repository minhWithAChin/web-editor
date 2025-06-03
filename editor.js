// import {EditorState} from "@codemirror/state"
// import {EditorView, keymap} from "@codemirror/view"
// import {defaultKeymap} from "@codemirror/commands"

// let startState = EditorState.create({
//   doc: "Hello World",
//   extensions: [keymap.of(defaultKeymap)]
// })

// let view = new EditorView({
//   state: startState,
//   parent: document.body
// })

let editorView = CodeMirror.fromTextArea(
    document.getElementById("editor"),
    {
        mode:"python",
        lineNumbers:true
    }
);

let postBtn=document.getElementById("postButton")
let getBtn=document.getElementById("getButton")
var xhrForm = new XMLHttpRequest();

xhrForm.onload = () => {
  // Request finished. Do processing here.
  document.getElementById("terminal").innerHTML = "whatever";
};

postBtn.onclick = function(){
    let form = new FormData();
    let codeStr=editorView.getValue();
    console.log(codeStr);
    form.append("code",codeStr);
    xhrForm.open("POST", "code/");
    xhrForm.send(form);

};
getBtn.onclick = function(){
    xhrForm.open("GET", "code/");
    xhrForm.send(null);
    

};
