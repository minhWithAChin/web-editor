import { sendCode,getCode,execCode,cancExec } from "../xmlhttpcom.js";

const myBlockDefinitions = Blockly.common.defineBlocksWithJsonArray([
  {
    "type": "print_block",
    "message0": "Ausgabe %1",
    "args0": [
      {
        "type": "input_value",
        "name": "TEXT"
      }
    ],
    "previousStatement": null,
    "nextStatement": null,
    "colour": 160,
    "tooltip": "Gibt den Text in der Konsole aus",
    "helpUrl": ""
  },
<
 {
    "type": "forw_step",
    "message0": "%1 Schritte Vorwärts",
    "args0": [
      {
        "type": "input_value",
        "name": "NUM"
      }
    ],
    "previousStatement": null,
    "nextStatement": null,
    "colour": 160,
    "tooltip": "geht um so viele Sekunden vorwärts",
    "helpUrl": ""
 }
]);

// 3. Python-Codegenerator
      python.pythonGenerator.forBlock['print_block'] = function(block) {
        const value_text = Blockly.Python.valueToCode(block, 'TEXT', Blockly.Python.ORDER_NONE) || "''";
        return 'print(f"[{t.strftime(\'%H:%M:%S\')}]: "+' + value_text + ')\n';
      };
      python.pythonGenerator.forBlock['forw_step'] = function(block) {
        const value_num = Blockly.Python.valueToCode(block, 'NUM', Blockly.Python.ORDER_NONE) || "''";
        return 'm.forward(+' + value_num + ')\n';
      };

// Add a preamble and a postscript to the code.
const preamble = 'import motor_test as m\nimport time as t\n'

const toolbox = {
  // There are two kinds of toolboxes. The simpler one is a flyout toolbox.
  kind: 'flyoutToolbox',
  // The contents is the blocks and other items that exist in your toolbox.
  contents: [
    {
      kind: 'block',
      type: 'controls_if'
    },
    {
      kind: 'block',
      type: 'controls_whileUntil'
    },
    // You can add more blocks to this array.
    {
      "kind": "block",
      "type": "math_number",
      "fields": {
        "NUM": 42
      }
    },
    {
      "kind": "block",
      "type": "logic_boolean",
    },
    {
      "kind": "block",
      "type": "text",
      
    },
    {
      kind: 'block',
      type: 'print_block'
    }, 
    {
      kind: 'block',
      type: 'forw_step'
    }, 
  ]
};

// The toolbox gets passed to the configuration struct during injection.
// Passes the ID.

const workspace = Blockly.inject('editor', {
                    toolbox: toolbox,
                    scrollbars: false,
                    horizontalLayout: true,
                    toolboxPosition: "end",
});


//___Generierung des Codes wenn Post gedrückt wird___
let postBtn=document.getElementById("postButton");
let getBtn=document.getElementById("getButton");
let execBtn=document.getElementById("execButton");
let cancBtn=document.getElementById("cancButton");
//cancBtn.disabled = true;

postBtn.onclick = function(){
    const pythonCode = python.pythonGenerator.workspaceToCode(workspace);
    const outCode=preamble+pythonCode
    console.log(outCode)
    sendCode(outCode);
};
getBtn.onclick = function(){
    getCode();
};

execBtn.onclick = function(){
    execCode();
    //execBtn.disabled = true;
    //cancBtn.disabled = false;
};

cancBtn.onclick = function(){
    cancExec();
    //execBtn.disabled = false;
    //cancBtn.disabled = true;
};
