// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';
import { executeGitCommandAndGetOutput, branchesStatus, workInMain, workOnSameBranch } from "./tools/git-command";

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed
export async function activate(context: vscode.ExtensionContext) {

    // Use the console to output diagnostic information (console.log) and errors (console.error)
    // This line of code will only be executed once when your extension is activated
    console.log('Congratulations, your extension "helloworld" is active!');

    // Create a new terminal to execute commands
    const git_assistant_terminal = vscode.window.createTerminal("git-assistant");

    const userName = await executeGitCommandAndGetOutput("git config user.name", git_assistant_terminal, 5000, 'git_output_temp_user_name.txt')
    userName.replace(/[^a-zA-Z]/g, '');

    setInterval(() => {
        workInMain(git_assistant_terminal)

    }, 10*60000); // Check every 10 minutes

    setInterval(() => {
            branchesStatus(git_assistant_terminal)
            workOnSameBranch(git_assistant_terminal, userName.split('\n')[0])

    }, 30*60000); // Check every 30 minutes
}

// This method is called when your extension is deactivated
export function deactivate() {}
