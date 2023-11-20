"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.deactivate = exports.activate = void 0;
// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
const vscode = __importStar(require("vscode"));
const git_notification_1 = require("./tools/git-notification");
// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed
function activate(context) {
    // Use the console to output diagnostic information (console.log) and errors (console.error)
    // This line of code will only be executed once when your extension is activated
    console.log('Congratulations, your extension "helloworld" is active!');
    let terminals = [];
    // Register the terminal open event listener
    const openTerminalListener = vscode.window.onDidOpenTerminal((terminal) => {
        const message = `Remember to run the command "script" in the new terminal`;
        (0, git_notification_1.showNotification)(message);
        terminals.push(terminal);
        // Execute a Git command in the terminal and retrieve the output
        (0, git_notification_1.executeGitCommandAndGetOutput)("git status", terminal, 5000)
            .then((value) => {
            for (const line of (0, git_notification_1.gitStatusCommand)(value)) {
                console.log(line);
            }
        })
            .catch((e) => {
            console.log('Erreur', e);
        });
    });
    // Register the terminal close event listener
    const closeTerminalDisposable = vscode.window.onDidCloseTerminal((closedTerminal) => {
        // Register a command to handle terminal closure
        const terminal = vscode.window.activeTerminal;
        if (terminal && terminals.includes(terminal)) {
            vscode.window.showInformationMessage(`Did you remember to run the command "exit" in the terminal? `, { modal: true }, 'Yes').then((choice) => {
                if (choice === 'Yes') {
                    // User confirmed, close the terminal
                    const closeMessage = `Terminal closed`;
                    (0, git_notification_1.showNotification)(closeMessage);
                    // Remove the closed terminal from the array
                    terminals = terminals.filter((t) => t !== closedTerminal);
                }
                else {
                    // User canceled, reopen the terminal
                    vscode.window.createTerminal().show();
                }
            });
        }
    });
    context.subscriptions.push(openTerminalListener, closeTerminalDisposable);
}
exports.activate = activate;
// This method is called when your extension is deactivated
function deactivate() { }
exports.deactivate = deactivate;
//# sourceMappingURL=extension.js.map