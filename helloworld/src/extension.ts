// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';

function showNotification(message: string): void {
    vscode.window.showInformationMessage(message);
}

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed
export function activate(context: vscode.ExtensionContext) {

	// Use the console to output diagnostic information (console.log) and errors (console.error)
	// This line of code will only be executed once when your extension is activated
	console.log('Congratulations, your extension "helloworld" is now active!');

	// The command has been defined in the package.json file
	// Now provide the implementation of the command with registerCommand
	// The commandId parameter must match the command field in package.json
	const terminalListener = vscode.window.onDidOpenTerminal((terminal) => {
        const message = `New terminal created: ${terminal.name}`;
        showNotification(message);
	});
	
	// Make sure to dispose of the event listener when the extension is deactivated
    context.subscriptions.push(terminalListener);
}

// This method is called when your extension is deactivated
export function deactivate() {}
