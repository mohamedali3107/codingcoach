import * as vscode from 'vscode';

export async function showNotification(message: string, moods: string[]) {
    const value = await vscode.window.showInformationMessage(message,...moods);
    return value
}

export async function showInputPrompt() {
    const userInput = await vscode.window.showInputBox({
        prompt: 'Enter your mood:',
        placeHolder: 'e.g., everything is fine',
    });
    return userInput
}



