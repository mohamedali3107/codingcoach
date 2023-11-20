import gitlab

gl = gitlab.Gitlab(url = 'https://gitlab-cw1.centralesupelec.fr', private_token='glpat-fULiHV8-x78CbwdNsz6w')
project = gl.projects.get('amin.belfkira/game2048')

def get_most_ahead(project):
    branches = project.branches.list()
    max_ahead = 0
    for branch in branches:
        if branch.name != 'main':
            ahead_by = len(project.repository_compare('main', branch.name)['commits'])
            if ahead_by > max_ahead:
                max_ahead = ahead_by
                most_ahead = branch.name
    return most_ahead

def get_most_behind(project):
    branches = project.branches.list()
    max_behind = 0
    for branch in branches:
        if branch.name != 'main':
            behind_by = len(project.repository_compare(branch.name, 'main')['commits'])
            if behind_by > max_behind:
                max_behind = behind_by
                most_behind = branch.name
    return most_behind

def get_branch_number(project):
    return len(project.branches.list())

def get_last_PR(project): # untested because nobody does PRs
    merge_requests = project.mergerequests.list()
    if len(merge_requests) == 0:
        return None
    merge_requests.sort(key=lambda x: x.created_at, reverse=True)
    return merge_requests[0]

def compare_branches(project):
    '''
    Takes a project and returns a list of branch names and numbers of commits ahead and behind.
    '''
    branches = project.branches.list()
    L = []
    for branch in branches:
        if branch.name != 'main':
            behind_by = len(project.repository_compare(branch.name, 'main')['commits'])
            ahead_by = len(project.repository_compare('main', branch.name)['commits'])
            L.append((branch.name, ahead_by, behind_by))
    return L

def count_big_commits(project):
    big_commits = 0
    for commit in project.commits.list(get_all=False):
        size = 0
        for diff in commit.diff(get_all=False):
            lines = diff['diff'].split('\n')
            for line in lines:
                if line != '' and (line[0] == '-' or line[0] == '+'):
                    size += 1
        if size > 40:
            print(commit.message)
            big_commits += 1
    return big_commits


def warning_message(L):
    s = ''
    for branch, ahead_by, behind_by in L:
        if ahead_by >= 10:
            s += f'''{branch} is ahead of main by {ahead_by} commits, consider merging:
    git checkout main
    git pull
    git merge {branch}

'''
        if behind_by >= 10:
            s += f'''{branch} is behind main by {behind_by} commits, consider rebasing:
    git checkout main
    git pull
    git checkout {branch}
    git rebase main
    
'''
    return s

#print(warning_message(compare_branches(project)))

#for name, ahead_by, behind_by in compare_branches(project):
#    print(f"{name} is ahead by {ahead_by} commits and behind by {behind_by} commits compared to main.")