import gitlab

gl = gitlab.Gitlab(url = 'https://gitlab.paris-digital-lab.com', private_token='glpat-qsH-B46AAzU8vCDw1yV3')

project = gl.projects.get('centralesupelec-fall2023-p2/codingcoach')
items = project.repository_tree()

print(items)