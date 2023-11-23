import gitlab

'''
If you encounter library compatibilty problems when installing python-gitlab, try running
pip3 uninstall urllib3
pip3 install 'urllib3<2.0'
'''

gl = gitlab.Gitlab(url = 'https://gitlab-cw1.centralesupelec.fr', private_token='glpat-fULiHV8-x78CbwdNsz6w')
project = gl.projects.get('amin.belfkira/game2048')

def get_project(server, token, project):
    gl = gitlab.Gitlab(url=server, private_token=token)
    return gl.projects.get(project)

def list_projects_users(server, token):
    projects = gitlab.Gitlab(url = server, private_token=token).projects.list(get_all=True)
    L = []
    for p in projects:
        path = p.path_with_namespace
        users = [user.username for user in p.users.list()]
        L.append([path] + users)
    return L


def most_ahead_branch(server, token, project):
    project = get_project(server, token, project)
    branches = project.branches.list()
    max_ahead = 0
    for branch in branches:
        if branch.name != 'main':
            ahead_by = len(project.repository_compare('main', branch.name)['commits'])
            if ahead_by > max_ahead:
                max_ahead = ahead_by
                most_ahead = branch.name
    return most_ahead

def most_behind_branch(server, token, project):
    project = get_project(server, token, project)
    branches = project.branches.list()
    max_behind = 0
    for branch in branches:
        if branch.name != 'main':
            behind_by = len(project.repository_compare(branch.name, 'main')['commits'])
            if behind_by > max_behind:
                max_behind = behind_by
                most_behind = branch.name
    return most_behind

def get_branch_number(server, token, project):
    project = get_project(server, token, project)
    return len(project.branches.list())

def last_PR_time(server, token, project): # untested because nobody does PRs
    project = get_project(server, token, project)
    merge_requests = project.mergerequests.list()
    if len(merge_requests) == 0:
        return None
    merge_requests.sort(key=lambda x: x.created_at, reverse=True)
    return merge_requests[0].created_at

def compare_branches(server, token, project):
    '''
    Takes a project and returns a list of branch names and numbers of commits ahead and behind.
    '''
    project = get_project(server, token, project)
    branches = project.branches.list()
    L = []
    for branch in branches:
        if branch.name != 'main':
            behind_by = len(project.repository_compare(branch.name, 'main')['commits'])
            ahead_by = len(project.repository_compare('main', branch.name)['commits'])
            L.append((branch.name, ahead_by, behind_by))
    return L

def rate_commits(server, token, project):
    project = get_project(server, token, project)
    malus = 0
    for commit in project.commits.list(get_all=False):
        size = 0
        for diff in commit.diff(get_all=False):
            lines = diff['diff'].split('\n')
            for line in lines:
                if line != '' and (line[0] == '-' or line[0] == '+'):
                    size += 1
        if size > 40:
            malus += min((size - 30)/30, 1)
    return 20 - malus
