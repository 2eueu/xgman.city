import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import json
import codecs

# 📁 파일 경로
shots_path = "shots_raw.txt"
match_path = "match_info_raw.txt"

# 📦 shots_raw.txt 디코딩
with open(shots_path, "r", encoding="utf-8") as f:
    raw_line = f.read().strip()
start = raw_line.find("JSON.parse('") + len("JSON.parse('")
end = raw_line.rfind("')")
escaped_json = raw_line[start:end]
decoded_json_str = codecs.decode(escaped_json, 'unicode_escape')
shots_json = json.loads(decoded_json_str)

# 📦 match_info_raw.txt 디코딩
with open(match_path, "r", encoding="utf-8") as f:
    match_raw = f.read().strip()
start_match = match_raw.find("JSON.parse('") + len("JSON.parse('")
end_match = match_raw.rfind("')")
escaped_match_json = match_raw[start_match:end_match]
decoded_match_json = codecs.decode(escaped_match_json, 'unicode_escape')
match_info = json.loads(decoded_match_json)

# 📊 선수별 xG 집계
home_team = match_info["team_h"]
away_team = match_info["team_a"]
home_df = pd.DataFrame(shots_json["h"])
away_df = pd.DataFrame(shots_json["a"])
home_df["team"] = home_team
away_df["team"] = away_team
df = pd.concat([home_df, away_df], ignore_index=True)
df["xG"] = df["xG"].astype(float)

xg_by_player = df.groupby(["player", "team"])["xG"].sum().reset_index()

# 🎨 시각화
sns.set_style("whitegrid")
fig, axes = plt.subplots(1, 2, figsize=(14, 8), sharex=True)

# 🔴 홈팀 (Brentford)
home_players = xg_by_player[xg_by_player["team"] == home_team].sort_values("xG")
sns.barplot(
    data=home_players, x="xG", y="player", ax=axes[0],
    color="orangered", edgecolor="black"
)
axes[0].set_title(f"{home_team}", fontsize=14, fontweight="bold")
axes[0].set_xlabel("Expected Goals (xG)")
axes[0].set_ylabel("Player")

# 🔵 어웨이팀 (Man City)
away_players = xg_by_player[xg_by_player["team"] == away_team].sort_values("xG")
sns.barplot(
    data=away_players, x="xG", y="player", ax=axes[1],
    color="royalblue", edgecolor="black"
)
axes[1].set_title(f"{away_team}", fontsize=14, fontweight="bold")
axes[1].set_xlabel("Expected Goals (xG)")
axes[1].set_ylabel("")  # 오른쪽 축 라벨 제거

# 🏁 전체 타이틀
plt.suptitle("Total Expected Goals (xG) per Player (Team Split View)", fontsize=16, fontweight="bold")
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig("player_xg_split_bar_chart.png", dpi=300)
plt.show()
