import * as vscode from 'vscode';
import * as fs from 'fs';

import { showNotification, showBigNotification } from './git-notification';
import { privateEncrypt } from 'crypto';

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

interface GitStatusInfo {
    current_branch: string;
    changes_to_be_commited: string[]; 
    changes_not_staged_for_commit: string[]; 
    untracked_files: string[];
    commit_ahead: {branch: string, commit_ahead: number};
    commit_behind: {branch: string, commit_behind: number};
}


export function gitStatusCommand(output: String): GitStatusInfo {

    let lines = output.split("\n");
    const lines_number = lines.length;

    let branch = "";
    let changes_to_be_committed = [];
    let changes_not_staged = [];
    let untracked_files = [];
    let commit_ahead = {branch: "", commit_ahead: 0};
    let commit_behind = {branch: "", commit_behind: 0};


    for (let i = 0; i < lines_number; i++) {
        let line = lines[i];

        if (line.includes("On branch")) {
            branch += line.substring(10,line.length);

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
            let file_split = (line[0] !== "\t" ? line.split(" ") : line.split("\t"));
            const ahead_branch = file_split[5];
            const n = ahead_branch.length;
            commit_ahead.branch = ahead_branch.substring(1,n-1);
            commit_ahead.commit_ahead = parseInt(file_split[7]);

        } else if (line.includes("Your branch is behind")) {
            // Your branch is behind 'origin/extension' by 1 commit, and can be fast-forwarded.
            // (use "git pull" to update your local branch)
            let file_split = (line[0] !== "\t" ? line.split(" ") : line.split("\t"));
            const behind_branch = file_split[5];
            const n = behind_branch.length;
            commit_behind.branch = behind_branch.substring(1,n-1);
            commit_behind.commit_behind = parseInt(file_split[6]);
        }

    }

    const res = { current_branch: branch, 
        changes_to_be_commited : changes_to_be_committed, 
        changes_not_staged_for_commit: changes_not_staged, 
        untracked_files: untracked_files,
        commit_ahead: commit_ahead,
        commit_behind: commit_behind
    }

    return res
}

export async function compareBranchWithMain(branchName: string, terminal: vscode.Terminal) {
    const command = `git rev-list --left-right --count ${branchName}...main`;
    const duration = 5000;
    let out = ""

    await executeGitCommandAndGetOutput(command, terminal, duration, 'git_output_temp_commits.txt')
        .then((value) => out = value)
        .catch((e) => console.log("Error in compareBranchWithMain:", e))

    const commits = out.split("\t");
    const commit_ahead = commits[0];
    const commit_behind = commits[1];
    return [Number(commit_ahead), Number(commit_behind)]

}

export function warning_message_status(branchName: string, ahead_by: number, behind_by: number, comparisonBranch: string) {
    let message = '';
    if (ahead_by >= 1 && behind_by ===0) {
        message += `${branchName} is ahead of ${comparisonBranch} by ${ahead_by} commits, consider merging: 
        git checkout ${comparisonBranch}, git pull, git merge ${branchName}, git push origin ${comparisonBranch}`
    } else if (behind_by >= 1 && ahead_by ===0) {
        message += `${branchName} is behind ${comparisonBranch} by ${behind_by} commits, consider rebasing: 
        git checkout ${comparisonBranch}, git pull, git checkout ${branchName}, git rebase ${comparisonBranch}, 
        git push origin ${branchName}`
    } else if (behind_by >= 1 && ahead_by >= 1) {
        message += `${branchName} is ahead of ${comparisonBranch} by ${ahead_by} commits and behind ${comparisonBranch} 
        by ${behind_by} commits, 
        consider rebasing and merging. Execute this to rebase: 
        git checkout ${comparisonBranch}, git pull, git checkout ${branchName}, git rebase ${comparisonBranch}, git push origin ${branchName}; 
        Execute this to merge: 
        git checkout ${comparisonBranch}, git pull, git merge ${branchName}, git push origin ${comparisonBranch}`
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
    let branch: string = "";
    let changes_to_be_commited: string[] = [];
    let changes_not_staged_for_commit: string[] = [];
    let untracked_files: string[] = [];
    let commit_ahead_remote = {branch: "", commit_ahead: 0};
    let commit_behind_remote = {branch: "", commit_behind: 0};


    executeGitCommandAndGetOutput("git status", terminal, 5000, 'git_output_temp.txt')
        .then((value) =>
            {
                const out = gitStatusCommand(value);
                branch = out.current_branch;
                changes_to_be_commited = out.changes_to_be_commited;
                changes_not_staged_for_commit = out.changes_not_staged_for_commit;
                untracked_files = out.untracked_files;
                commit_ahead_remote = out.commit_ahead;
                commit_behind_remote = out.commit_behind;
                }
        )
        .catch((e) => {
            console.log('Error in branchesStatus:', e)
    })

    const [commit_ahead_main, commit_behind_main] = await compareBranchWithMain(branch, terminal);
    const message_local = warning_message_status(branch, commit_ahead_main, commit_behind_main, "main")
    if (message_local != "") {
        showBigNotification(message_local)
    }

    // Show a second notification after 5 minutes
    const delay1 = 5*60000;
    setTimeout(() => {
        const message_remote = warning_message_status(branch, commit_ahead_remote.commit_ahead, commit_behind_remote.commit_behind, commit_ahead_remote.branch)
        if (message_remote != "") {
            showBigNotification(message_remote)
        }
    }, delay1);

    // Show a third notification after 10 minutes
    const delay2 = 10*60000;
    setTimeout(() => {
        let changes_to_be_commited_length = changes_to_be_commited.length;
        let changes_not_staged_for_commit_length = changes_not_staged_for_commit.length;
        let untracked_files_length = untracked_files.length;
        if (changes_not_staged_for_commit_length !== 0) {
            let changes = ""
            for (const change of changes_not_staged_for_commit) {
                changes += (change) + ", "
            }
            const message = `You have not staged changes. Don't forget to add the files ${changes}.`
            showBigNotification(message)
        }
        if (changes_to_be_commited_length !== 0) {
            const message = `You have not committed changes. Don't forget to commit and push.`
            showBigNotification(message)
        }
        if (untracked_files_length !== 0) {
            let changes = ""
            for (const change of untracked_files) {
                changes += (change) + ", "
            }
            const message = `The following files are untracked: ${changes}. Don't forget to add, commit and push them.`
            showBigNotification(message)
        }
    }, delay2);

}

export async function workInMain(terminal: vscode.Terminal) {
    let branchName = ""
    await executeGitCommandAndGetOutput("git branch --show-current", terminal, 3000, 'git_output_temp_current_branch.txt')
    .then((value) => branchName = value.replace(/[^a-zA-Z]/g, ''))
    .catch((e) => console.log('Error in workInMain:',e))

    console.log("Branch name:", branchName=="main")

    if (branchName =="main") {

        let branch: string = "";
        let changes_to_be_commited: string[] = [];
        let changes_not_staged_for_commit: string[] = [];
        let untracked_files: string[] = [];

        setInterval(async () => {

            await executeGitCommandAndGetOutput("git status", terminal, 5000, 'git_output_temp_work_in_main.txt')
            .then((value) =>
                {
                    const out = gitStatusCommand(value);
                    branch = out.current_branch;
                    changes_to_be_commited = out.changes_to_be_commited;
                    changes_not_staged_for_commit = out.changes_not_staged_for_commit;
                    untracked_files = out.untracked_files;
                    }
            )
            .catch((e) => {
                console.log('Error in workInMain:', e)
        })

        branch.replace(/[^a-zA-Z]/g, '');

        console.log("Branch:", branch=="main");

        const branch_modified = changes_to_be_commited.length + changes_not_staged_for_commit.length + untracked_files.length

        console.log(branch_modified)

        if (branch == "main" && branch_modified > 0) {
            showNotification("Warning: you are working in the main branch.")
        }
            }, 5*60000);  // Check every 5 minutes
    }
}