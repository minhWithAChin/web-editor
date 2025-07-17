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

 {
    "type": "move_step",
    "message0": "%1 Schritte %2",
    "args0": [
      {
        "type": "input_value",
        "name": "NUM"
      },
      {
        "type": "field_dropdown",
        "name": "FIELDNAME",
      "options": [
        [ "Vorwärts", "forward" ],
        [ "Rückwärts", "reverse" ]]
      }
    ],
    "previousStatement": null,
    "nextStatement": null,
    "colour": 160,
    "tooltip": "bewegt sich um so viele Sekunden",
    "helpUrl": ""
 },
 {
    "type": "turn_90",
    "message0": "%1-mal nach %2 drehen",
    "args0": [
      {
        "type": "input_value",
        "name": "NUM"
      },
      {
        "type": "field_dropdown",
        "name": "FIELDNAME",
      "options": [
        [ "rechts", "right" ],
        [ "links", "left" ]]
      }
    ],
    "previousStatement": null,
    "nextStatement": null,
    "colour": 160,
    "tooltip": "dreht sich so oft um 90°",
    "helpUrl": ""
 },
 {
    "type": "set_speed",
    "message0": "%1 Geschwindigkeit vom %2",
    "args0": [
      {
        "type": "input_value",
        "name": "NUM"
      },
      {
        "type": "field_dropdown",
        "name": "FIELDNAME",
      "options": [
        [ "rechter Motor", "speed_r" ],
        [ "linker Motor", "speed_l" ]]
      }
    ],
    "previousStatement": null,
    "nextStatement": null,
    "colour": 180,
    "tooltip": "Setzt die Geschwindigkeit des Ausgewählten Motors",
    "helpUrl": ""
 },

{
    "type": "move_cont",
    "message0": "%1",
    "args0": [
      { 
        "type": "field_dropdown",
        "name": "FIELDNAME",
      "options": [
        [ "Vorwärts", "cont_forw" ],
        [ "Rückwärts", "cont_back" ]]
      }
    ],
    "previousStatement": null,
    "nextStatement": null,
    "colour": 180,
    "tooltip": "bewegt sich endlos bis es angehalten wird",
},
{
    "type": "turn_cont",
    "message0": "%1",
    "args0": [
      { 
        "type": "field_dropdown",
        "name": "FIELDNAME",
      "options": [
        [ "Rechts drehen", "cont_right" ],
        [ "Links drehen", "cont_left" ]]
      }
    ],
    "previousStatement": null,
    "nextStatement": null,
    "colour": 180,
    "tooltip": "dreht endlos bis es angehalten wird",
},
{
    "type": "reset_m",
    "message0": "Anhalten",
    "previousStatement": null,
    "nextStatement": null,
    "colour": 180,
    "tooltip": "hält das Fahrzeug an",
},
 {
    "type": "get_dist",
    "message0": "Entfernung vom Sensor %1",
    "args0": [
      {
        "type": "field_dropdown",
        "name": "FIELDNAME",
      "options": [
        [ "links", "0" ],
        [ "mitte", "1" ],
        [ "rechts", "2" ]]
      }
    ],
    "output":"Number",
    "colour": 160,
    "tooltip": "gibt die Entfernung vom Sensor zurück",
    "helpUrl": ""
 },
// Block for variable getter.
{
  "type": "var_get",
  "message0": "%1",
  "args0": [
    {    // Beginning of the field variable dropdown
      "type": "field_variable",
      "name": "VAR",    // Static name of the field
      "variable": "%{BKY_VARIABLES_DEFAULT_NAME}"    // Given at runtime
    }    // End of the field variable dropdown
  ],
  "output": null,    // Null means the return value can be of any type
    "colour": 150,
    "tooltip": "gibt die Variable aus",
  //...
},

// Block for variable setter.
{
  "type": "var_set",
  "message0": "%{BKY_VARIABLES_SET}",
  "args0": [
    {
      "type": "field_variable",
      "name": "VAR",
      "variable": "%{BKY_VARIABLES_DEFAULT_NAME}"
    },
    {
      "type": "input_value",    // This expects an input of any type
      "name": "VALUE"
    }
  ],
    "previousStatement": null,
    "nextStatement": null,
    "colour": 150,
    "tooltip": "erzeigt oder setzt eine Variable",
},

{
  "type": "def_func",
  "message0": "definiere Funktion %1 mit Parametern %2 %3",
  "args0": [
    {
      "type": "field_input",
      "name": "FUNC_NAME",
      "text": "meineFunktion"
    },
    {
      "type": "field_input",
      "name": "PARAMS",
      "text": "arg1"
    },
    {
      "type": "input_statement",
      "name": "BODY"
    }
  ],
  "colour": 195,
  "tooltip": "Erlaubt es dem Nutzer, eine eigene Funktion zu definieren",
  "helpUrl": ""
},
{
  "type": "call_func",
  "message0": "rufe %1 auf mit %2",
  "args0": [
    {
      "type": "field_input",
      "name": "FUNC_NAME",
      "text": "meineFunktion"
    },
    {
      "type": "input_value",
      "name": "ARGS"
    }
  ],
  "inputsInline": true,
  "previousStatement": null,
  "nextStatement": null,
  "colour": 195,
  "tooltip": "Ruft eine benutzerdefinierte Funktion mit Argumenten auf",
  "helpUrl": ""
}


]);


// 3. Python-Codegenerator
      python.pythonGenerator.forBlock['print_block'] = function(block) {
        const value_text = Blockly.Python.valueToCode(block, 'TEXT', Blockly.Python.ORDER_NONE) || "''";
        return 'print(f"[{t.strftime(\'%H:%M:%S\')}]: "+str(' + value_text + '))\n';
      };
      python.pythonGenerator.forBlock['move_step'] = function(block) {
        const value_num = Blockly.Python.valueToCode(block, 'NUM', Blockly.Python.ORDER_NONE) || "''";
	const option = block.getFieldValue('FIELDNAME')
        return 'm.'+ option +'(+' + value_num + ')\n';
      };
      python.pythonGenerator.forBlock['turn_90'] = function(block) {
        const value_num = Blockly.Python.valueToCode(block, 'NUM', Blockly.Python.ORDER_NONE) || "''";
	const option = block.getFieldValue('FIELDNAME')
        return 'm.'+ option +'(+' + value_num + ')\n';
      };python.pythonGenerator.forBlock['move_cont'] = function(block) {
	const option = block.getFieldValue('FIELDNAME')
        return 'm.'+ option +'()\n';
      };python.pythonGenerator.forBlock['turn_cont'] = function(block) {
	const option = block.getFieldValue('FIELDNAME')
        return 'm.'+ option +'()\n';
      };python.pythonGenerator.forBlock['reset_m'] = function(block) {
        return 'm.reset()\n';
      };python.pythonGenerator.forBlock['set_speed'] = function(block) {
        const value_num = Blockly.Python.valueToCode(block, 'NUM', Blockly.Python.ORDER_NONE) || "''";
	const option = block.getFieldValue('FIELDNAME')
        return 'm.'+ option +'(+' + value_num + ')\n';
      };
      python.pythonGenerator.forBlock['get_dist'] = function(block) {
	const option = block.getFieldValue('FIELDNAME')
        return ['m.dist('+ option +')',Blockly.Python.ORDER_NONE];
      };
      python.pythonGenerator.forBlock['var_set'] = function(block) {
      var variable_name = Blockly.Python.nameDB_.getName(block.getFieldValue('VAR'),    Blockly.Variables.NAME_TYPE);
  const value = Blockly.Python.valueToCode(block, "VALUE", Blockly.Python.ORDER_NONE) || "''";
  return variable_name + ' = ' + value + '\n';
};      python.pythonGenerator.forBlock['var_get'] = function(block) {
      var variable_name = Blockly.Python.nameDB_.getName(block.getFieldValue('VAR'),    Blockly.Variables.NAME_TYPE);
  return [variable_name,Blockly.Python.ORDER_ATOMIC];
};
python.pythonGenerator.forBlock['def_func'] = function(block) {
  // Funktionsname und Parameter unverändert übernehmen
  var funcName = block.getFieldValue('FUNC_NAME') || 'meineFunktion';
  var params   = block.getFieldValue('PARAMS').trim();

  // Code aus dem BODY‑Eingang holen und richtig einrücken
  var bodyCode = Blockly.Python.statementToCode(block, 'BODY');
  if (!bodyCode.trim()) {
    bodyCode = Blockly.Python.INDENT + 'pass\n';   // leere Funktionen vermeiden Fehler
  }

  var code  = 'def ' + funcName + '(' + params + '):\n' + bodyCode + '\n';
  return code;
};
      python.pythonGenerator.forBlock['call_func'] = function(block) {
  var funcName = block.getFieldValue('FUNC_NAME');
  var args = Blockly.Python.valueToCode(block, 'ARGS', Blockly.Python.ORDER_NONE) || '';
  var code = funcName + '(' + args + ')\n';
  return code;
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
    {
      kind: 'block',
      type: 'logic_compare'
    },
    {
      kind: 'block',
      type: 'math_arithmetic'
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
      "fields":{"TEXT":"Hello World!"}
      
    },
    {
      kind: 'block',
      type: 'print_block'
    }, 
    {
      kind: 'block',
      type: 'move_step'
    }, {
      kind: 'block',
      type: 'move_cont'
    }, 
    {
      kind: 'block',
      type: 'turn_90'
    }, {
      kind: 'block',
      type: 'turn_cont'
    }, {
      kind: 'block',
      type: 'set_speed'
    }, {
      kind: 'block',
      type: 'reset_m'
    }, 
    {
      kind: 'block',
      type: 'get_dist'
    }, 
    {
      kind: 'block',
      type: 'var_set'
    }, 
    {
      kind: 'block',
      type: 'var_get'
    }, 
    {
      kind: 'block',
      type: 'def_func'
    }, 
    {
      kind: 'block',
      type: 'call_func'
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
