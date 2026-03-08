import json, os, urllib.request

username = os.environ['USERNAME']
token = os.environ['GH_TOKEN']

req = urllib.request.Request(
    f'https://api.github.com/users/{username}',
    headers={'Authorization': f'token {token}', 'Accept': 'application/vnd.github.v3+json'}
)
with urllib.request.urlopen(req) as r:
    user = json.loads(r.read())

repos_req = urllib.request.Request(
    f'https://api.github.com/users/{username}/repos?per_page=100&type=owner',
    headers={'Authorization': f'token {token}', 'Accept': 'application/vnd.github.v3+json'}
)
with urllib.request.urlopen(repos_req) as r:
    repos = json.loads(r.read())

total_stars = sum(repo.get('stargazers_count', 0) for repo in repos)
followers = user.get('followers', 0)
public_repos = user.get('public_repos', 0)

def get_level(value, thresholds):
    labels = ['C', 'B', 'A', 'S', 'SS', 'SSS']
    for i, t in enumerate(thresholds):
        if value < t:
            return labels[i]
    return 'SSS'

trophies = [
    ('Stars', str(total_stars), get_level(total_stars, [10,50,100,500,1000,5000]), '#FFD700'),
    ('Followers', str(followers), get_level(followers, [10,50,100,500,1000,5000]), '#C0C0C0'),
    ('Commits', '109+', 'A', '#CD7F32'),
    ('Repos', str(public_repos), get_level(public_repos, [5,10,20,50,100,200]), '#00CED1'),
    ('PRs', '2', 'B', '#9370DB'),
    ('Issues', '1', 'B', '#FF6347'),
]

W, H, cols = 800, 110, 6
cell_w = W // cols

parts = []
parts.append(f'<svg width="{W}" height="{H}" xmlns="http://www.w3.org/2000/svg">')
parts.append(f'<rect width="{W}" height="{H}" fill="#1a1b27" rx="10"/>')

for i, (name, count, rank, color) in enumerate(trophies):
    x = i * cell_w
    cx = x + cell_w // 2
    tx = cx - 8
    ty = 36
    cup = (f'M{tx+8},{ty} L{tx+3},{ty+8} Q{tx+1},{ty+13} {tx+4},{ty+15}'
           f' L{tx+6},{ty+15} L{tx+6},{ty+19} L{tx+2},{ty+21}'
           f' L{tx+14},{ty+21} L{tx+10},{ty+19} L{tx+10},{ty+15}'
           f' L{tx+12},{ty+15} Q{tx+15},{ty+13} {tx+13},{ty+8} Z')
    parts.append('<g>')
    parts.append(f'<rect x="{x+4}" y="4" width="{cell_w-8}" height="{H-8}" fill="#1f2335" rx="8" stroke="{color}" stroke-width="1.5"/>')
    parts.append(f'<text x="{cx}" y="20" text-anchor="middle" fill="{color}" font-size="10" font-family="monospace" font-weight="bold">{name}</text>')
    parts.append(f'<path d="{cup}" fill="{color}"/>')
    parts.append(f'<text x="{cx}" y="76" text-anchor="middle" fill="#a9b1d6" font-size="9" font-family="monospace">{count}</text>')
    parts.append(f'<text x="{cx}" y="94" text-anchor="middle" fill="{color}" font-size="11" font-family="monospace" font-weight="bold">{rank}</text>')
    parts.append('</g>')

parts.append('</svg>')

svg = '\n'.join(parts)
os.makedirs('profile', exist_ok=True)
with open('profile/trophy.svg', 'w') as f:
    f.write(svg)
print(f'Trophy SVG generated: {len(svg)} bytes')
