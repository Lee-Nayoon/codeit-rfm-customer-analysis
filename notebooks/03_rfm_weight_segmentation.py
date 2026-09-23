# 가중치 설정
weight = {}
weight['recency'] = 1/3
weight['frequency'] = 1/3
weight['monetary'] = 1/3
customer_df['rfm_score'] = (weight['recency'] * customer_df['recency_level'] + weight['frequency'] * customer_df['frequency_level'] + weight['monetary'] * customer_df['monetary_level'])

# rfm 등급 분류, 새 컬럼 생성 (등급 값이 클수록 우수 고객)
def rfm_bins(x):
    if x < 5 / 3:
        return 1
    elif x <= 7 / 3:
        return 2
    else:
        return 3

customer_df['rfm_segment'] = customer_df['rfm_score'].apply(rfm_bins)

print(customer_df['rfm_segment'].value_counts().sort_index())


# rfm 세그먼트별 매출 기여도 확인
groupby_monetary_level = customer_df.groupby('rfm_segment').sum(numeric_only = True).reset_index()
groupby_monetary_level['amount_total'].plot(kind = 'pie', autopct = '%.1f%%', labels = ['1등급', '2등급', '3등급'], title = 'RFM 세그먼트별 매출 기여도')

# rfm 세그먼트별 연령대 분포 확인
groupby_rfm_age = pd.DataFrame(customer_df.groupby(['rfm_segment', 'age_group'], observed = True).size().reset_index())
groupby_rfm_age = groupby_rfm_age.rename(columns = {0 : 'customer_total'})
groupby_rfm_age

# 파이 그래프 확인
for i in range(1, 4):
    age_group_dist = groupby_rfm_age[groupby_rfm_age['rfm_segment'] == i]
    age_group_dist['customer_total'].plot(
    kind = 'pie',
    autopct = '%.1f%%',
    labels = age_group_dist['age_group'].unique(),
    title = f'{i}등급 세그먼트별 고객 연령대 분포',
    ylabel = '')
    plt.show()

# rfm 세그먼트별 가족 구성 분포 확인
groupby_rfm_marital = pd.DataFrame(customer_df.groupby(['rfm_segment', 'marital_status'], observed = True).size().reset_index())
groupby_rfm_marital = groupby_rfm_marital.rename(columns = {0 : 'customer_total'})

# 파이 그래프 확인
for i in range(1, 4):
    marital_group_dist = groupby_rfm_marital[groupby_rfm_marital['rfm_segment'] == i]
    marital_group_dist['customer_total'].plot(
    kind = 'pie',
    autopct = '%.1f%%',
    labels = marital_group_dist['marital_status'].unique(),
    title = f'{i}등급 세그먼트별 가족 구성 분포',
    ylabel = '')
    plt.show()

# rfm 세그먼트별 부양 자녀 수 분포 확인
groupby_rfm_children = pd.DataFrame(customer_df.groupby(['rfm_segment', 'children'], observed = True).size().reset_index())
groupby_rfm_children = groupby_rfm_children.rename(columns = {0 : 'customer_total'})

# 파이 그래프 확인
for i in range(1, 4):
    children_group_dist = groupby_rfm_children[groupby_rfm_children['rfm_segment'] == i]
    children_group_dist['customer_total'].plot(
    kind = 'pie',
    autopct = '%.1f%%',
    labels = [f'{x}명' for x in children_group_dist['children'].unique()],
    title = f'{i}등급 세그먼트별 부양 자녀 수 분포',
    ylabel = '')
    plt.show()
