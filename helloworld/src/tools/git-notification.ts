import * as vscode from 'vscode';
import * as fs from 'fs';


export function showNotification(message: string): void {
    vscode.window.showInformationMessage(message);
}

export async function executeGitCommandAndGetOutput(command: string, terminal: vscode.Terminal, duration: number): Promise<string> {
    
    // Check if there's an active workspace folder
    const activeWorkspace = vscode.workspace.workspaceFolders?.[0];

    if (!activeWorkspace) {
        throw new Error('No active workspace found.');
    }

    // Generate a temporary file path within the workspace folder to store the command output
    const tempFilePath = vscode.Uri.joinPath(activeWorkspace.uri, 'git_output_temp.txt').fsPath;

    // Run the Git command in the terminal
    terminal.sendText(`${command} > ${tempFilePath}`);

    // Wait for some time to collect the output (adjust this time according to your command's execution time)
    await new Promise(resolve => setTimeout(resolve, duration)); // Wait for 2 seconds (adjust as needed)

   // Read the contents of the temporary file (command output)
   const output = fs.readFileSync(tempFilePath, 'utf-8');

   // Remove the temporary file
   fs.unlinkSync(tempFilePath);

   // Return the captured output
   return output;
}

export function gitStatusCommand(output: String): Array<any> {

    let lines = output.split("\n")
    const lines_number = lines.length

    let branch = ""
    let relationship_with_remote = ""
    let changes_to_be_committed = []
    let changes_not_staged = []
    let untracked_files = []
    let commit_ahead = {}
    let commit_behind = {}



    for (let i = 0; i < lines_number; i++) {
        let line = lines[i];

        if (line.includes("On branch")) {
            branch += line.substring(10,line.length);
            relationship_with_remote += lines[i+1];

        } else if (line.includes("Changes to be committed:")){
            let j = 1;
            let file = lines[i+j];
            while (file !== "" && i+j < lines_number) {
                if (!file.includes("(use")) {
                    let file_split = file.split("\t")
                    file_split = file_split[file_split.length - 1].split(" ")
                    changes_to_be_committed.push(file_split[file_split.length - 1]);
                }
                j += 1;
                file = lines[i+j];
            }

        } else if (line.includes("Changes not staged for commit:")){
            let j = 1;
            let file = lines[i+j];
            while (file !== "" && i+j < lines_number) {
                if (!file.includes("(use")) {
                    let file_split = file.split("\t")
                    file_split = file_split[file_split.length - 1].split(" ")
                    changes_not_staged.push(file_split[file_split.length - 1]);
                }
                j += 1;
                file = lines[i+j];
            }

        } else if (line.includes("Untracked files:")){
            let j = 1;
            let file = lines[i+j];
            while (file !== "" && i+j < lines_number) {
                if (file !== '\tgit_output_temp.txt' && !file.includes("(use")) {
                    let file_split = (file[0] !== "\t" ? file.split(" ") : file.split("\t"));
                    untracked_files.push(file_split[file_split.length - 1]);
                }
                j += 1;
                file = lines[i+j];
            }
        } else if (line.includes("Your branch is ahead of")) {
            // Your branch is ahead of 'origin/extension' by 1 commit.
            let file_split = line.split(" ");
            (commit_ahead as any).file_line[5] = parseInt(file_split[7]);

        } else if (line.includes("Your branch is behind")) {
            // Your branch is behind 'origin/extension' by 1 commit, and can be fast-forwarded.
            // (use "git pull" to update your local branch)
            let file_split = line.split(" ");
            (commit_behind  as any).file_line[4] = parseInt(file_split[6]);
        }

    }

    return ["Current branch:", branch, 
    "Relationship with remote repository:", relationship_with_remote, 
    "Changes to be commited:", changes_to_be_committed, 
    "Changes not staged for commit:", changes_not_staged, 
    "Untracked files:", untracked_files,
    "Commit ahead:", commit_ahead,
    "Commit behind:", commit_behind
    ]

}

//test