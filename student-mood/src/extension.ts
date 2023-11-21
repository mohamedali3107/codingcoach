// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';
import { askStudentMood } from "./tools/notification";
import { executeGitCommandAndGetOutput } from "./tools/execute-command";
import { makePostRequest } from "./tools/request"
import { ConsoleReporter } from '@vscode/test-electron';

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
    const openTerminalListener = vscode.window.onDidOpenTerminal(async (terminal) => {

        // Get the mood of the student
        const mood = await askStudentMood()

        console.log(mood)
        const mood_integer = mood[0]
        const message = mood[1]

        // Get the email of the user
        const email: string = await executeGitCommandAndGetOutput("git config user.email", terminal, 5000)
        
        console.log("Mood Integer:", mood_integer);

        // POST request: send the mood of the student
        const response = makePostRequest( {
            "moodLevel": mood_integer,
            "message": message,
            "email": email
        });

        console.log(response)

        terminals.push(terminal);

    });

    context.subscriptions.push(openTerminalListener);
}

// This method is called when your extension is deactivated
export function deactivate() {}


