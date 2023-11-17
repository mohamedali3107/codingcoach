import * as vscode from 'vscode';

export async function showNotification(message: string, moods: string[]) {
    const value = await vscode.window.showInformationMessage(message,...moods);
    return value
}