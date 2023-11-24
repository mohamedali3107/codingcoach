import * as vscode from 'vscode';
import * as fs from 'fs';

import { showNotification, showBigNotification } from './git-notification';
import { Context } from 'mocha';

export async function executeGitCommandAndGetOutput(command: string, terminal: vscode.Terminal, duration: number, path: string): Promise<string> {
    
    // Check if there's an active workspace folder
    const activeWorkspace = vscode.workspace.workspaceFolders?.[0];

    if (!activeWorkspace) {
        throw new Error('No active workspace found.');
    }

    // Generate a temporary file path within the workspace folder to store the command output
    const tempFilePath = vscode.Uri.joinPath(activeWorkspace.uri, path).fsPath;

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
            console.log(line);
            // Your branch is ahead of 'origin/extension' by 1 commit.
            let file_split = (line[0] !== "\t" ? line.split(" ") : line.split("\t"));
            const ahead_branch = file_split[5];
            const n = ahead_branch.length;
            (commit_ahead as any)[ahead_branch.substring(1,n-1)] = parseInt(file_split[7]);

        } else if (line.includes("Your branch is behind")) {
            // Your branch is behind 'origin/extension' by 1 commit, and can be fast-forwarded.
            // (use "git pull" to update your local branch)
            let file_split = (line[0] !== "\t" ? line.split(" ") : line.split("\t"));
            const behind_branch = file_split[5];
            const n = behind_branch.length;
            (commit_behind  as any)[behind_branch.substring(1,n-1)] = parseInt(file_split[6]);
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

export async function compareBranchWithMain(branchName: string, terminal: vscode.Terminal) {
    const command = `git rev-list --left-right --count ${branchName}...main`;
    const duration = 5000;
    let out = ""

    await executeGitCommandAndGetOutput(command, terminal, duration, 'git_output_temp_commits.txt')
        .then((value) => out = value)
        .catch((e) => console.log(e))

    const commits = out.split("\t");
    const commit_ahead = commits[0];
    const commit_behind = commits[1];
    return [Number(commit_ahead), Number(commit_behind)]

}

export function warning_message(branchName: string, ahead_by: number, behind_by: number) {
    let message = '';
    if (ahead_by >= 1 && behind_by ===0) {
        message += `${branchName} is ahead of main by ${ahead_by} commits, consider merging: 
        git checkout main, git pull, git merge ${branchName}, git push origin main`
    } else if (behind_by >= 1 && ahead_by ===0) {
        message += `${branchName} is behind main by ${behind_by} commits, consider rebasing: 
        git checkout main, git pull, git checkout ${branchName}, git rebase main, git push origin ${branchName}`
    } else if (behind_by >= 1 && ahead_by >= 1) {
        message += `${branchName} is ahead of main by ${ahead_by} commits and behind main by ${behind_by} commits, 
        consider rebasing and merging. Execute this to rebase: 
        git checkout main, git pull, git checkout ${branchName}, git rebase main, git push origin ${branchName}; 
        Execute this to merge: 
        git checkout main, git pull, git merge ${branchName}, git push origin main`
    }
    
    return message
}

export async function getBranches(terminal: vscode.Terminal) {
    const duration = 5000
    const command = "git branch"
    let out = ""

    await executeGitCommandAndGetOutput(command, terminal, duration, 'git_output_temp_branch.txt')
        .then((value) => out = value)
        .catch((e) => console.log(e))

    let lines = out.split("\n")
    let names = []

    console.log(lines)

    for (const line of lines) {
        const name = (line[0] !== "\t" ? line.split(" ") : line.split("\t"));
        names.push(name[name.length-1])
    }
    return names
}

export async function branchesStatus(terminal: vscode.Terminal) {
    let branches: string[] = [];
    await getBranches(terminal)
        .then((value) => branches = value)
        .catch((e) => console.log(e))

    console.log("Branches:", branches)
    for (const branch of branches) {
        const [commit_ahead, commit_behind] = await compareBranchWithMain(branch, terminal);
        console.log("branchName:", branch)
        const message = warning_message(branch, commit_ahead, commit_behind)
        console.log("Message:", message)
        if (message != "") {
            showBigNotification(message)
        }
    }
}

