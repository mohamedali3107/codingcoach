import gitlab

gl = gitlab.Gitlab(url = 'https://gitlab.paris-digital-lab.com', private_token='glpat-qsH-B46AAzU8vCDw1yV3')

project = gl.projects.get('centralesupelec-fall2023-p2/codingcoach')
items = project.repository_tree()
branches = project.branches.list()

for branch in branches:
    if branch.name != 'main':
        behind_by = len(project.repository_compare(branch.name, 'main')['commits'])
        ahead_by = len(project.repository_compare('main', branch.name)['commits'])
        print(f"Branch '{branch.name}' is ahead by {ahead_by} commits and behind by {behind_by} commits compared to 'main'.")