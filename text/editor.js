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
import { sendCode,getCode,execCode } from "../xmlhttpcom.js";

let editorView = CodeMirror.fromTextArea(
    document.getElementById("editor"),
    {
        mode:"python",
        lineNumbers:true
    }
);

let postBtn=document.getElementById("postButton");
let getBtn=document.getElementById("getButton");
let execBtn=document.getElementById("execButton");

postBtn.onclick = function(){
    sendCode(editorView.getValue());
};
getBtn.onclick = function(){
    getCode();
};
execBtn.onclick = function(){
    execCode();
};

