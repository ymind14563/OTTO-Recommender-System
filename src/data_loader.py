import json
import pandas as pd
import numpy as np

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

    initial_count = len(df)
    print(f"데이터 이상치, 결측치 처리 전: {initial_count:,}행")

    # (1) 결측치 처리(빈 경우 제거)
    required_columns = ["aid", "ts", "type", "session"]
    df = df.dropna(subset=required_columns)
    print(f"(1) 결측치 제거: {initial_count - len(df):,}행 제거")

    # (2) 이벤트 타입 결측치 처리(clicks, carts, orders 이외의 값이 존재하는 행 제거)
    valid_event_types = ["clicks", "carts", "orders"]
    count_before = len(df)
    df = df[df["type"].isin(valid_event_types)]
    print(f"(2) 이벤트 타입 필터링: {count_before - len(df):,}행 제거")

    # (3) AID의 이상치 처리 (음수는 제거)
    count_before = len(df)
    df = df[df["aid"] > 0]
    print(f"(3) AID 이상치 제거: {count_before - len(df):,}행 제거")

    # # (4) IQR 기반 이상치 처리 (aid 이벤트 수 기준, 상하위 15% 제거)
    # event_counts = df.groupby("aid").size()
    # Q1 = event_counts.quantile(0.15)
    # Q3 = event_counts.quantile(0.85)
    # IQR = Q3 - Q1

    # # 정상 범위: Q1 - 1.5 * IQR ~ Q3 + 1.5 * IQR 
    # lower_bound = Q1 - 1.5 * IQR
    # upper_bound = Q3 + 1.5 * IQR
    # valid_aids = event_counts[(event_counts >= lower_bound) & (event_counts <= upper_bound)].index

    # count_before = len(df)
    # df = df[df["aid"].isin(valid_aids)]
    
    print(f"(4) AID IQR 이상치 제거: {count_before - len(df):,}행 제거")

    # (5) 타임스탬프 이상치 처리
    # 10자리(초 단위) -> 13자리(밀리초 단위) 변환
    count_before = len(df)
    df["ts"] = np.where(df["ts"].astype(str).str.len() == 10, df["ts"] * 1000, df["ts"])
    print(f"(5.1) 타임스탬프 변환 완료")

    # 13자리 타임스탬프가 아닌 경우 제거
    count_before = len(df)
    df = df[df["ts"].astype(str).str.len() == 13]
    print(f"(5.2) 비정상 타임스탬프 제거: {count_before - len(df):,}행 제거")

    # IQR 기반 타임스탬프 이상치 제거
    Q1 = df["ts"].quantile(0.25)
    Q3 = df["ts"].quantile(0.75)
    IQR = Q3 - Q1

    # 정상 범위: Q1 - 1.5 * IQR ~ Q3 + 1.5 * IQR
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    count_before = len(df)
    df = df[(df["ts"] >= lower_bound) & (df["ts"] <= upper_bound)]
    print(f"(5.3) 타임스탬프 IQR 이상치 제거: {count_before - len(df):,}행 제거")


    # 최종 데이터 확인 로그
    print(f"최종 데이터 개수: {len(df):,}")

    return df
