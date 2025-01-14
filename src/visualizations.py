import matplotlib.pyplot as plt
import datetime
import numpy as np

### 시각화

# (1) 이벤트 유형 분포
def plot_event_distribution(df, save_path):
    plt.figure()
    event_types = df["type"]
    event_counts = event_types.value_counts()
    event_counts.plot(kind="bar", title="이벤트 유형 분포", ylabel="개수(백만)", xlabel="이벤트 유형")
    
    plt.savefig(save_path)
    plt.close()


# (2) 타임스탬프 분포
def plot_timestamp_distribution(df, save_path):
    plt.figure()
    timestamps = df["ts"]
    ax = timestamps.plot(kind="hist", bins=50, title="타임스탬프 분포", ylabel="이벤트 발생 빈도수", xlabel="타임스탬프")
    plt.xlim(timestamps.min(), timestamps.max())

    # X축 레이블 재설정 (날짜와 시간으로 표시)
    xticks = np.linspace(timestamps.min(), timestamps.max(), num=10)
    xtick_labels = [datetime.datetime.utcfromtimestamp(ts / 1000).strftime('%Y-%m-%d\n%H:%M:%S') for ts in xticks]
    ax.set_xticks(xticks)
    ax.set_xticklabels(xtick_labels, rotation=45)

    plt.savefig(save_path)
    plt.close()



# (3) 세션당 이벤트 수 분포
def plot_session_event_distribution(df, save_path):
    plt.figure()
    session_event_counts = df.groupby("session").size()
    session_event_counts.plot(kind="hist", bins=50, title="세션당 이벤트 수 분포", ylabel="빈도수", xlabel="이벤트 수")
    
    plt.savefig(save_path)
    plt.close()


# (4) 상품(AID) 분포
def plot_aid_distribution(df, save_path):
    plt.figure()
    aids = df["aid"]
    aid_counts = aids.value_counts().head(20)    
    aid_counts.plot(kind="bar", title="상위 20개의 상품(AID) 분포", ylabel="개수", xlabel="상품 ID")
    plt.xticks(rotation=45)
    
    plt.savefig(save_path)
    plt.close()


# (5) 상위 10개 상품(AID)와 이벤트 유형 관계
def plot_aid_event_relationship(aid_event_counts, save_path):
    plt.figure()
    aid_event_counts["total"] = aid_event_counts.sum(axis=1)
    aid_event_counts = aid_event_counts.sort_values(by="total", ascending=False)

    aid_event_counts.head(10).drop(columns=["total"]).plot(kind="bar", stacked=True, title="상위 10개 상품(AID)과 이벤트 유형의 관계", ylabel="개수", xlabel="상품 ID")
    plt.xticks(ticks=range(len(aid_event_counts.head(10).index)), labels=aid_event_counts.head(10).index, rotation=45)
    
    plt.savefig(save_path)
    plt.close()


# (6) 구매 전환율 높은 상품(AID)
def plot_conversion_rate(aid_event_counts, save_path):
    plt.figure()
    # 구매 전환율 계산 및 데이터 정리
    aid_event_counts["conversion_rate"] = aid_event_counts["orders"] / (aid_event_counts["clicks"] + 1e-10)
    aid_event_counts_sorted = aid_event_counts.sort_values(by="conversion_rate", ascending=False)

    # 클릭 > 카트 > 주문 조건 필터링 (단기간 데이터이므로 과거 담아놓은 상품을 주문하는 경우의 집계를 최소화하기 위함)
    aid_event_counts_filtered = aid_event_counts_sorted[
        (aid_event_counts_sorted["clicks"] > aid_event_counts_sorted["carts"]) &
        (aid_event_counts_sorted["carts"] > aid_event_counts_sorted["orders"])
    ]

    top_10_aid_events = aid_event_counts_filtered.head(10)[["clicks", "carts", "orders"]]
    top_10_aid_events.plot(kind="bar", stacked=True, figsize=(10, 6), title="구매전환율이 높은 상위 10개 상품(AID)와 비율", ylabel="개수", xlabel="상품 ID")
    plt.xticks(ticks=range(len(top_10_aid_events.index)), labels=top_10_aid_events.index, rotation=45)
    plt.legend(["Clicks", "Carts", "Orders"])

    plt.savefig(save_path)
    plt.close()
