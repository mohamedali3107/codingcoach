import * as vscode from 'vscode';
import axios from 'axios';

export async function makePostRequest(values: any) {
    const url = 'https://coding-assistant.centralesupelec.fr/send_mood/'; // Server's URL

    try {
        const response = await axios.post(url, values);

    } catch (error) {
        // Handle errors
        console.error('Error:', error);

        // Show an error notification
        vscode.window.showErrorMessage('Error: POST request failed!');
    }
}
