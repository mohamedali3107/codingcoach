### Logging Commands and Outputs in VSCode Terminal

#### Windows (Using `Get-Transcript`)

1. Open VSCode and go to the integrated terminal.

2. Ensure that you have the transcription feature enabled. Run the following command in PowerShell:

    ```powershell
    Start-Transcript -Path C:\Users\<Your user>\Documents\git.log
    ```
	This will start recording your terminal session and save it to a file named `git.log`.

3. Execute your git commands as usual. All input and output will be logged.

4. To stop recording, run:

    ```powershell
    Stop-Transcript
    ```

5. Send us `git.log` at `codingcoachgit@gmail.com`

#### Linux (Using `script`)

1. Open VSCode and navigate to the integrated terminal.

2. To start logging, use the `script` command followed by the filename. 

    ```bash
    script git.log
    ```

    This will start recording your terminal session and save it to a file named `git.log`.

3. Execute your git commands as usual. All input and output will be logged.

4. To stop recording, type `exit` or `Ctrl+D`.

5. Send us `git.log` at `codingcoachgit@gmail.com`

### /!\

Remember to stop the logging session to save the output.