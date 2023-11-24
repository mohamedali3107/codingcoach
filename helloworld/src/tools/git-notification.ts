import * as vscode from 'vscode';

export function showNotification(message: string): void {
    vscode.window.showInformationMessage(message);
}

export function showBigNotification(message: string): void {
    //const options: vscode.MessageOptions = { detail: "", modal: true};
    vscode.window.showInformationMessage(message, ...[" "," "]);
}