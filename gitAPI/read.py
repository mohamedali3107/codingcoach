import gitlab

gl = gitlab.Gitlab(url = 'https://gitlab.paris-digital-lab.com', private_token='glpat-qsH-B46AAzU8vCDw1yV3')
project = gl.projects.get('centralesupelec-fall2023-p2/codingcoach')

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

def warning_message(L):
    s = ''
    for branch, ahead_by, behind_by in L:
        if ahead_by >= 10:
            s += f'''{branch} is ahead of main by {ahead_by} commits, consider merging:'''
        if behind_by >= 10:
            s += f'''{branch} is behind main by {behind_by} commits, consider rebasing:
    git checkout main
    git pull
    git checkout {branch}
    git rebase main
    '''
    return s

print(warning_message(compare_branches(project)))

#for name, ahead_by, behind_by in compare_branches(project):
#    print(f"{name} is ahead by {ahead_by} commits and behind by {behind_by} commits compared to main.")