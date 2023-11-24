import * as vscode from 'vscode';
import { executeGitCommandAndGetOutput } from "./execute-command";
import { makePostRequest } from "./request";
import { showNotification, showInputPrompt } from './notification';

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

    let mood_integer = 0

    if (mood_emoji === '\u{1F603}') {
            mood_integer = 1
    } else if (mood_emoji === '\u{1F610}') {
        mood_integer = 2
    } else if (mood_emoji === '\u{1F641}') {
            mood_integer = 3
    } else {
            mood_integer = 4
      }

    return [mood_integer, mood_phrase]

}


export async function askAndSendMood(terminal: vscode.Terminal) {
    // Get the mood of the student
    const mood = await askStudentMood()

    const mood_integer = mood[0]
    const message = mood[1]

    // Get the name of the user's project
    const projectName: string = await executeGitCommandAndGetOutput(`git remote show origin | awk '/Fetch URL:/ { print $3 }' | awk -F/ '{ print $(NF-1) "/" $NF }' | sed 's/\.git$//'`, terminal, 5000)
    
    console.log("Mood Integer:", mood_integer);

    // POST request: send the mood of the student
    const response = makePostRequest( {
        "moodLevel": mood_integer,
        "message": message,
        "email": projectName
    });

    console.log(response)
}