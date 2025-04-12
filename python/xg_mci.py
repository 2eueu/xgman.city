import json
import matplotlib.pyplot as plt
import os
import re

# 파일 경로
base_dir = "/Users/2eueu_/coding/xG_mancity"
shots_path = os.path.join(base_dir, "shots_raw.txt")
match_info_path = os.path.join(base_dir, "match_info_raw.txt")

# shots_raw.txt에서 var shotsData = JSON.parse('...') 추출
with open(shots_path, "r", encoding="utf-8") as f:
    raw = f.read()
    match = re.search(r"JSON\.parse\('(.+)'\)", raw)
    if match:
        json_escaped = match.group(1).encode('utf-8').decode('unicode_escape')
        shots_data = json.loads(json_escaped)
    else:
        raise ValueError("shots_raw.txt에서 JSON.parse(...) 패턴을 찾을 수 없습니다.")

# match_info_raw.txt에서 JSON.parse('...') 추출
with open(match_info_path, "r", encoding="utf-8") as f:
    raw = f.read()
    match = re.search(r"JSON\.parse\('(.+)'\)", raw)
    if match:
        json_escaped = match.group(1).encode('utf-8').decode('unicode_escape')
        match_info = json.loads(json_escaped)
    else:
        raise ValueError("match_info_raw.txt에서 JSON.parse(...) 패턴을 찾을 수 없습니다.")

# 홈팀/원정팀 이름
home_team = match_info["team_h"]
away_team = match_info["team_a"]

# 누적 xG 계산용 함수
def cumulative_xg(events):
    x = []
    y = []
    total = 0
    for i, event in enumerate(events):
        total += float(event['xG'])
        x.append(event['minute'])
        y.append(total)
    return x, y

home_shots = shots_data['h']
away_shots = shots_data['a']

home_x, home_y = cumulative_xg(home_shots)
away_x, away_y = cumulative_xg(away_shots)

# 시각화
plt.figure(figsize=(10, 6))
plt.step(home_x, home_y, label=f"{home_team} (xG {match_info['h_xg']})", where='post')
plt.step(away_x, away_y, label=f"{away_team} (xG {match_info['a_xg']})", where='post')
plt.xlabel("Minute")
plt.ylabel("Cumulative xG")
plt.title(f"{home_team} vs {away_team} - xG Timeline")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
