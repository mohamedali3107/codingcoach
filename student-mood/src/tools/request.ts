import * as vscode from 'vscode';
import axios from 'axios';

export async function makePostRequest(values: any) {
    const url = 'http://localhost:8000/send_mood/'; // Server's URL

    try {
        const response = await axios.post(url, values);

        // Handle the response
        console.log('Response:', response.data);
        console.log(response.request)
        console.log(response.config.url)

        // Show a notification with the response data
        vscode.window.showInformationMessage('POST request successful!');
    } catch (error) {
        // Handle errors
        console.error('Error:', error);

        // Show an error notification
        vscode.window.showErrorMessage('Error: POST request failed!');
    }
}
