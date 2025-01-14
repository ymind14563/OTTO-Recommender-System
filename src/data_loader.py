import json
import pandas as pd

# JSONL 파일 경로
data_file = "../data/raw/test.jsonl"

### 데이터 로드
def load_data(file_path):
    data = []
    with open(file_path, "r") as file:
        for line in file:
            session_data = json.loads(line.strip())
            data.append(session_data)
    return data

### 데이터 전처리
def preprocess_data(data):
    # 세션과 이벤트 데이터를 분리
    sessions = []
    for session in data:
        session_id = session["session"]
        for event in session["events"]:
            event["session"] = session_id
            sessions.append(event)

    # DataFrame 생성
    df = pd.DataFrame(sessions)
    return df
