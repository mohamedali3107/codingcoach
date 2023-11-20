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

export async function askStudentMood() {

    const message = `What is your mood today?`;
    const instruction = `Please, enter a phrase in the box at the top of the window to describe your mood`;
    let mood_emoji: string | undefined  = ""
    let mood_phrase: string | undefined  = ""

    await showNotification(message, ['\u{1F603}','\u{1F610}','\u{1F641}', '\u{1F62D}'])
        .then(mood => {showNotification(instruction,[]), mood_emoji = mood})
        .then(() => showInputPrompt())
        .then((phrase) => {mood_phrase = phrase})
        .catch((e) => console.log(e));

    return [mood_emoji, mood_phrase]

}


