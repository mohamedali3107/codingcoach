// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';
import { showNotification, executeGitCommandAndGetOutput, gitStatusCommand } from "./tools/git-notification";

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed
export function activate(context: vscode.ExtensionContext) {

    // Use the console to output diagnostic information (console.log) and errors (console.error)
    // This line of code will only be executed once when your extension is activated
    console.log('Congratulations, your extension "helloworld" is active!');

    let terminals: vscode.Terminal[] = [];

    // Register the terminal open event listener
    const openTerminalListener = vscode.window.onDidOpenTerminal((terminal) => {
        const message = `Remember to run the command "script" in the new terminal`;
        showNotification(message);
        terminals.push(terminal);

        // Execute a Git command in the terminal and retrieve the output
        executeGitCommandAndGetOutput("git status", terminal, 5000)
            .then((value) =>
                {
                    for (const line of gitStatusCommand(value)) {
                        console.log(line)
                    }
                }
            )
            .catch((e) => {
                console.log('Erreur', e)
        })

    });

    // Register the terminal close event listener
    const closeTerminalDisposable = vscode.window.onDidCloseTerminal( (closedTerminal) => {
        // Register a command to handle terminal closure
            const terminal = vscode.window.activeTerminal;
            if (terminal && terminals.includes(terminal)) {
                vscode.window.showInformationMessage(`Did you remember to run the command "exit" in the terminal? `, { modal: true }, 'Yes').then((choice) => {
                    if (choice === 'Yes') {
                        // User confirmed, close the terminal
                        const closeMessage = `Terminal closed`;
                        showNotification(closeMessage);

                        // Remove the closed terminal from the array
                        terminals = terminals.filter((t) => t !== closedTerminal);
                    } else {
                        // User canceled, reopen the terminal
                        vscode.window.createTerminal().show();
                    }
                });
            }   
    });

    context.subscriptions.push(openTerminalListener,closeTerminalDisposable);
}

// This method is called when your extension is deactivated
export function deactivate() {}

