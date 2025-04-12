# ⚽ 슛 마커 표시 기능 추가
import json
import matplotlib.pyplot as plt

# shot_raw.txt & match_info_raw.txt 불러오기
with open("shots_raw.txt", "r", encoding="utf-8") as f:
    raw_shots = f.read()
    raw_shots = raw_shots.split("JSON.parse('")[-1].rsplit("')", 1)[0]
    raw_shots = bytes(raw_shots, "utf-8").decode("unicode_escape")
    shots_data = json.loads(raw_shots)

with open("match_info_raw.txt", "r", encoding="utf-8") as f:
    raw_info = f.read()
    raw_info = raw_info.split("JSON.parse('")[-1].rsplit("')", 1)[0]
    raw_info = bytes(raw_info, "utf-8").decode("unicode_escape")
    match_info = json.loads(raw_info)

# 팀 이름과 xG
team_h = match_info["team_h"]
team_a = match_info["team_a"]
xg_h = match_info["h_xg"]
xg_a = match_info["a_xg"]

# 팀별 데이터 분리
home_shots = shots_data["h"]
away_shots = shots_data["a"]

# 누적 xG 계산용 함수
def get_cumulative_xg(shots):
    minutes = []
    xg = []
    total = 0
    for s in shots:
        minutes.append(int(s["minute"]))
        total += float(s["xG"])
        xg.append(total)
    return minutes, xg

# 슛 위치 시각화용 함수
def plot_shot_markers(ax, shots, team_color, is_home=True):
    for s in shots:
        x = float(s["minute"])
        y = float(s["xG"])
        if s["result"] == "Goal":
            ax.scatter(x, y, marker="*", s=100, color=team_color, label=f"Goal: {s['player']}")
        else:
            ax.scatter(x, y, marker="o", s=50, edgecolors=team_color, facecolors='none')

# 그래프 그리기
fig, ax = plt.subplots(figsize=(12, 6))
min_h, xg_h_vals = get_cumulative_xg(home_shots)
min_a, xg_a_vals = get_cumulative_xg(away_shots)

ax.step(min_h, xg_h_vals, label=f"{team_h} (xG {xg_h})", color="dodgerblue")
ax.step(min_a, xg_a_vals, label=f"{team_a} (xG {xg_a})", color="darkorange")

plot_shot_markers(ax, home_shots, "dodgerblue", is_home=True)
plot_shot_markers(ax, away_shots, "darkorange", is_home=False)

ax.set_title(f"{team_h} vs {team_a} - xG Timeline")
ax.set_xlabel("Minute")
ax.set_ylabel("Cumulative xG")
ax.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
