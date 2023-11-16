import gitlab

gl = gitlab.Gitlab(url = 'https://gitlab.paris-digital-lab.com', private_token='glpat-qsH-B46AAzU8vCDw1yV3')
project = gl.projects.get('centralesupelec-fall2023-p2/codingcoach')

def compare_branches(project):
    branches = project.branches.list()
    L = []
    for branch in branches:
        if branch.name != 'main':
            behind_by = len(project.repository_compare(branch.name, 'main')['commits'])
            ahead_by = len(project.repository_compare('main', branch.name)['commits'])
            L.append((branch.name, ahead_by, behind_by))
    return L

for name, ahead_by, behind_by in compare_branches(project):
    print(f"{name} is ahead by {ahead_by} commits and behind by {behind_by} commits compared to main.")