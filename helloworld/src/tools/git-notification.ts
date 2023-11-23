import * as vscode from 'vscode';

export function showNotification(message: string): void {
    vscode.window.showInformationMessage(message);
}