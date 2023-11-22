import gitlab

'''
If you encounter library compatibilty problems when installing python-gitlab, try running
pip3 uninstall urllib3
pip3 install 'urllib3<2.0'
'''

gl = gitlab.Gitlab(url = 'https://gitlab-cw1.centralesupelec.fr', private_token='glpat-fULiHV8-x78CbwdNsz6w')
project = gl.projects.get('amin.belfkira/game2048')

def list_users(url, token):
    users = gitlab.Gitlab(url = url, private_token=token).users.list(get_all=True)
    return [(user.name, user.email) for user in users]

def list_projects(url, token):
    gl = gitlab.Gitlab(url = url, private_token=token)
    return gl.projects.list(get_all=True)

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

def rate_commits(project):
    malus = 0
    for commit in project.commits.list(get_all=False):
        size = 0
        for diff in commit.diff(get_all=False):
            lines = diff['diff'].split('\n')
            for line in lines:
                if line != '' and (line[0] == '-' or line[0] == '+'):
                    size += 1
        if size > 40:
            print(commit.message)
            malus += min((size - 30)/30, 1)
    return 20 - malus
