// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';
import { executeGitCommandAndGetOutput, gitStatusCommand, branchesStatus, workInMain, workOnSameBranch } from "./tools/git-command";
import { showNotification} from "./tools/git-notification";
import { privateEncrypt } from 'crypto';

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed
export function activate(context: vscode.ExtensionContext) {

    // Use the console to output diagnostic information (console.log) and errors (console.error)
    // This line of code will only be executed once when your extension is activated
    console.log('Congratulations, your extension "helloworld" is active!');

    let terminals: vscode.Terminal[] = [];

    // Register the terminal open event listener
    const openTerminalListener = vscode.window.onDidOpenTerminal(async (terminal) => {
        const userName = await executeGitCommandAndGetOutput("git config user.name", terminal, 5000, 'git_output_temp_user_name.txt')
        userName.replace(/[^a-zA-Z]/g, '');

        setInterval(() => {
            workInMain(terminal)

        }, 10*60000); // Check every 10 minutes

        setInterval(() => {
                branchesStatus(terminal)
                workOnSameBranch(terminal, userName.split('\n')[0])

        }, 30*60000); // Check every 30 minutes

        terminals.push(terminal);

    });

    context.subscriptions.push(openTerminalListener);
}

// This method is called when your extension is deactivated
export function deactivate() {}
