// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';
import { askAndSendMood } from './tools/mood';


// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed
export function activate(context: vscode.ExtensionContext) {

    // Use the console to output diagnostic information (console.log) and errors (console.error)
    // This line of code will only be executed once when your extension is activated
    console.log('Congratulations, your extension "studentmood" is now active!');

    // The command has been defined in the package.json file
    // Now provide the implementation of the command with registerCommand
    // The commandId parameter must match the command field in package.json
    
    let terminals: vscode.Terminal[] = []; 

    
    // Register the terminal open event listener
    const openTerminalListener = vscode.window.onDidOpenTerminal(async (terminal) => {

        const time = { hours: 10, minutes: 30 };

        setInterval(() => {
            const now = new Date();
            const scheduledTime = new Date();
            scheduledTime.setHours(time.hours, time.minutes, 0, 0); // Set hours and minutes of scheduled time
            
            // Calculate the delay until the scheduled time (in milliseconds)
            let delay = scheduledTime.getTime() - now.getTime();

            if (delay < -15*60000) {
                // If the scheduled time is in the past, schedule for the next day
                scheduledTime.setDate(scheduledTime.getDate() + 1);
                delay = scheduledTime.getTime() - now.getTime();
                console.log(delay)
            } else if (delay >= -15*60000 && delay < 15*60000) {
            // Execute the command if the delay is within a certain threshold (e.g., 1 minute) 
                askAndSendMood(terminal)
            }
        }, 15*60000); // Check every 15 minute (adjust as needed)

        terminals.push(terminal);

    });

    context.subscriptions.push(openTerminalListener);
}

// This method is called when your extension is deactivated
export function deactivate() {}


