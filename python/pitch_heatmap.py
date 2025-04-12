import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import json
import codecs

# 파일 경로
shots_path = "shots_raw.txt"
match_path = "match_info_raw.txt"

# shots_raw.txt 처리
with open(shots_path, "r", encoding="utf-8") as f:
    raw_line = f.read().strip()
start = raw_line.find("JSON.parse('") + len("JSON.parse('")
end = raw_line.rfind("')")
escaped_json = raw_line[start:end]
decoded_json_str = codecs.decode(escaped_json, 'unicode_escape')
shots_json = json.loads(decoded_json_str)

# match_info_raw.txt 처리
with open(match_path, "r", encoding="utf-8") as f:
    match_raw = f.read().strip()
start_match = match_raw.find("JSON.parse('") + len("JSON.parse('")
end_match = match_raw.rfind("')")
escaped_match_json = match_raw[start_match:end_match]
decoded_match_json = codecs.decode(escaped_match_json, 'unicode_escape')
match_info = json.loads(decoded_match_json)

# 데이터 준비
home_team = match_info["team_h"]
away_team = match_info["team_a"]
df_home = pd.DataFrame(shots_json["h"])
df_away = pd.DataFrame(shots_json["a"])
df_home["h_a"] = "h"
df_away["h_a"] = "a"
df = pd.concat([df_home, df_away], ignore_index=True)
df["X"] = df["X"].astype(float)
df["Y"] = df["Y"].astype(float)

# ... (이전 코드 생략: shots_json, match_info, df 생성까지 동일)

# 어웨이팀 좌표 반사 (우측 공격 방향)
df.loc[df["h_a"] == "a", "X"] = 1 - df.loc[df["h_a"] == "a", "X"]

# 득점 여부 컬럼
df["isGoal"] = df["result"] == "Goal"

# 축구장 함수
def draw_pitch(ax):
    ax.plot([0, 1], [0, 0], color="black")
    ax.plot([1, 1], [0, 1], color="black")
    ax.plot([1, 0], [1, 1], color="black")
    ax.plot([0, 0], [1, 0], color="black")
    ax.plot([0.5, 0.5], [0, 1], color="black", linestyle="--", alpha=0.3)

    ax.plot([0.12, 0.12], [0.21, 0.79], color="black")
    ax.plot([0, 0.12], [0.21, 0.21], color="black")
    ax.plot([0, 0.12], [0.79, 0.79], color="black")
    ax.plot([0.88, 0.88], [0.21, 0.79], color="black")
    ax.plot([1, 0.88], [0.21, 0.21], color="black")
    ax.plot([1, 0.88], [0.79, 0.79], color="black")

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_axis_off()

# 시각화
fig, ax = plt.subplots(figsize=(12, 8))

# KDE 히트맵
sns.kdeplot(data=df[df["h_a"] == "h"], x="X", y="Y",
            cmap="Reds", fill=True, alpha=0.6, levels=50, thresh=0.02, clip=((0, 1), (0, 1)), ax=ax)
sns.kdeplot(data=df[df["h_a"] == "a"], x="X", y="Y",
            cmap="Blues", fill=True, alpha=0.6, levels=50, thresh=0.02, clip=((0, 1), (0, 1)), ax=ax)

# 마커 표시
for _, shot in df.iterrows():
    if shot["isGoal"]:
        ax.scatter(shot["X"], shot["Y"], color="gold", s=150, edgecolor='black', marker="*", zorder=5)
        # 득점자 이름 표기
        ax.text(shot["X"] + 0.015, shot["Y"], shot["player"], fontsize=9, fontweight="bold",
                verticalalignment='center', color='black')
    else:
        ax.scatter(shot["X"], shot["Y"], color="black", alpha=0.4, s=30, zorder=4)

# 축구장 + 텍스트
draw_pitch(ax)
ax.text(0.08, 1.02, home_team, fontsize=14, ha="center", va="bottom", fontweight="bold")
ax.text(0.92, 1.02, away_team, fontsize=14, ha="center", va="bottom", fontweight="bold")

plt.title(f"Shot Heatmap with Goal Scorers\n{home_team} (Left) vs {away_team} (Right)", fontsize=16, fontweight="bold")
plt.tight_layout()
plt.savefig("shot_heatmap_with_names.png", dpi=300)
plt.show()
