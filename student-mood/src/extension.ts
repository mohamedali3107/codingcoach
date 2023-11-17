// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';
import { showNotification } from "./tools/notification";

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed
export function activate(context: vscode.ExtensionContext) {

    // Use the console to output diagnostic information (console.log) and errors (console.error)
    // This line of code will only be executed once when your extension is activated
    console.log('Congratulations, your extension "studentmood" is now active!');

    // The command has been defined in the package.json file
    // Now provide the implementation of the command with registerCommand
    // The commandId parameter must match the command field in package.json
    
    let terminals: vscode.Terminal[] = [];
    
    // Register the terminal open event listener
    const openTerminalListener = vscode.window.onDidOpenTerminal((terminal) => {
        const message = `What is your mood today?`;

        showNotification(message, ['\u{1F603}','\u{1F610}','\u{1F641}', '\u{1F62D}'])
            .then(mood => console.log("Mood:",mood))
            .catch((e) => console.log(e));

        terminals.push(terminal);
    });

    context.subscriptions.push(openTerminalListener);
}

// This method is called when your extension is deactivated
export function deactivate() {}


