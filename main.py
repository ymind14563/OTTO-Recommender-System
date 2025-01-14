import matplotlib.pyplot as plt
from matplotlib import rc
import os
import time
from src import (
    load_data,
    preprocess_data,
    plot_event_distribution,
    plot_timestamp_distribution,
    plot_session_event_distribution,
    plot_aid_distribution,
    plot_aid_event_relationship,
    plot_conversion_rate,
)

# 한글 폰트 설정 (맑은 고딕체)
rc('font', family='Malgun Gothic')

# 한글 깨짐 방지를 위한 유니코드 설정 (한글에서 마이너스(-) 기호가 깨지는 현상 방지)
plt.rcParams['axes.unicode_minus'] = False

# 전체 작업 시작 시간 기록
script_start_time = time.time()

# 경로 설정
RAW_DATA_PATH = "data/raw/test.jsonl"
PROCESSED_DATA_PATH = "data/processed/processed_data.csv"
FIGURES_DIR = "outputs/figures/"

# 디렉토리 생성 (없을 경우)
os.makedirs("data/processed", exist_ok=True)
os.makedirs(FIGURES_DIR, exist_ok=True)

# 1. 데이터 로드
start_time = time.time()
print("데이터 로드 중...")
data = load_data(RAW_DATA_PATH)
print(f"데이터 로드 완료: {time.time() - start_time:.2f}초 소요\n")

# 2. 데이터 전처리
start_time = time.time()
print("데이터 전처리 중...")
df = preprocess_data(data)
print(f"데이터 전처리 완료: {time.time() - start_time:.2f}초 소요\n")

# 3. 전처리된 데이터 저장
start_time = time.time()
print("전처리된 데이터 저장 중...")
df.to_csv(PROCESSED_DATA_PATH, index=False)
print(f"데이터 저장 완료: {time.time() - start_time:.2f}초 소요\n")

# 4. 시각화
print("시각화 생성 중...")
start_time = time.time()

# (1) 이벤트 유형 분포
plot_event_distribution(df, os.path.join(FIGURES_DIR, "(1) event_distribution.png"))
print("(1) 이벤트 유형 분포 저장 완료")

# (2) 타임스탬프 분포
plot_timestamp_distribution(df, os.path.join(FIGURES_DIR, "(2) timestamp_distribution.png"))
print("(2) 타임스탬프 분포 저장 완료")

# (3) 세션당 이벤트 수 분포
plot_session_event_distribution(df, os.path.join(FIGURES_DIR, "(3) session_event_distribution.png"))
print("(3) 세션당 이벤트 수 분포 저장 완료")

# (4) 고유 상품(AID) 분포
plot_aid_distribution(df, os.path.join(FIGURES_DIR, "(4) aid_distribution.png"))
print("(4) 고유 상품(AID) 분포 저장 완료")

# (5) 상위 10개 상품(AID)와 이벤트 유형 관계
aid_event_df = df[["aid", "type"]]
aid_event_counts = aid_event_df.groupby(["aid", "type"]).size().unstack(fill_value=0)
plot_aid_event_relationship(aid_event_counts, os.path.join(FIGURES_DIR, "(5) aid_event_relationship.png"))
print("(5) AID와 이벤트 유형 관계 저장 완료")

# (6) 구매 전환율 높은 상품(AID)
plot_conversion_rate(aid_event_counts, os.path.join(FIGURES_DIR, "(6) conversion_rate_top10.png"))
print("(6) 구매 전환율 높은 상품 저장 완료")

print(f"시각화 완료: {time.time() - start_time:.2f}초 소요\n")

# 전체 작업 완료 시간 계산
total_time = time.time() - script_start_time
print(f"작업 완료. 총 소요 시간: {total_time:.2f}초")
