import { sendCode,getCode,execCode } from "../xmlhttpcom.js";

const myBlockDefinitions = Blockly.common.defineBlocksWithJsonArray([
  {
    "type": "print_block",
    "message0": "print %1",
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
  }
]);

// 3. Python-Codegenerator
      python.pythonGenerator.forBlock['print_block'] = function(block) {
        const value_text = Blockly.Python.valueToCode(block, 'TEXT', Blockly.Python.ORDER_NONE) || "''";
        return 'print(' + value_text + ')\n';
      };

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

postBtn.onclick = function(){
    const pythonCode = python.pythonGenerator.workspaceToCode(workspace);
    console.log(pythonCode)
    sendCode(pythonCode);
};
getBtn.onclick = function(){
    getCode();
};

execBtn.onclick = function(){
    execCode();
};