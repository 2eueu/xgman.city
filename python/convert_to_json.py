import json
import codecs

# 파일 경로
shots_path = "shots_raw.txt"
match_path = "match_info_raw.txt"

# shots_raw 처리
with open(shots_path, "r", encoding="utf-8") as f:
    raw_line = f.read().strip()

start = raw_line.find("JSON.parse('") + len("JSON.parse('")
end = raw_line.rfind("')")
escaped_json = raw_line[start:end]
decoded_json_str = codecs.decode(escaped_json, 'unicode_escape')
shots_data = json.loads(decoded_json_str)

# match_info_raw 처리
with open(match_path, "r", encoding="utf-8") as f:
    match_raw = f.read().strip()

start_m = match_raw.find("JSON.parse('") + len("JSON.parse('")
end_m = match_raw.rfind("')")
escaped_match_json = match_raw[start_m:end_m]
decoded_match_json = codecs.decode(escaped_match_json, 'unicode_escape')
match_info = json.loads(decoded_match_json)

# 병합 구조 생성
xg_data = {
    "match_info": match_info,
    "home_shots": shots_data["h"],
    "away_shots": shots_data["a"]
}

# 저장
with open("xg_data.json", "w", encoding="utf-8") as f:
    json.dump(xg_data, f, indent=2, ensure_ascii=False)

print("✅ xg_data.json 파일이 생성되었습니다.")
