// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';
import { executeGitCommandAndGetOutput, gitStatusCommand, branchesStatus } from "./tools/git-command";

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed
export function activate(context: vscode.ExtensionContext) {

    // Use the console to output diagnostic information (console.log) and errors (console.error)
    // This line of code will only be executed once when your extension is activated
    console.log('Congratulations, your extension "helloworld" is active!');

    let terminals: vscode.Terminal[] = [];

    // Register the terminal open event listener
    const openTerminalListener = vscode.window.onDidOpenTerminal((terminal) => {
        
        terminals.push(terminal);

        // Execute a Git command in the terminal and retrieve the output
        executeGitCommandAndGetOutput("git status", terminal, 5000, 'git_output_temp.txt')
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

        branchesStatus(terminal)

    });

    context.subscriptions.push(openTerminalListener);
}

// This method is called when your extension is deactivated
export function deactivate() {}


//test

