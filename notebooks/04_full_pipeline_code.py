import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 한글 지원 폰트 설치
plt.rc('font', family = 'Malgun Gothic')

# 데이터 불러오기
customer_df = pd.read_csv(r'C:\Users\TRUEBON\Downloads\customer_data.csv', sep='\t')
 
# 컬럼 정보 확인
customer_df.info()

# 데이터 샘플(상위 5개) 확인
customer_df.head()

# str 타입의 컬럼의 데이터 종류 확인
for i in customer_df.columns:
    if customer_df[i].dtype == 'str':
        print(customer_df[i].unique())

# 결측값 있는 컬럼 확인
customer_df.isna().sum()

# 데이터의 양이 충분히 많으므로 결측값 있는 로우 제거
customer_df = customer_df.dropna()

# 결측값 제거 확인
customer_df.isna().sum()

# 중복되는 로우 확인, 삭제
customer_df[customer_df.duplicated()]
customer_df.drop_duplicates()

# 컬럼 별 수학적 정보 확인
customer_df.describe(include = 'all')

# 고객 특성 분류에 불필요한 'ID'와 컬럼 내 모든 데이터의 값이 같은 'revenue' 컬럼 삭제
customer_df = customer_df.drop(columns = ['ID', 'revenue'])

# 총 구매 금액 컬럼 생성
amount_total = customer_df[['amount_alcohol', 'amount_fruit', 'amount_meat', 'amount_fish', 'amount_snack', 'amount_general']].sum(axis = 1)
amount_loc = customer_df.columns.get_loc('amount_general') + 1
customer_df.insert(loc = amount_loc, column = 'amount_total', value = amount_total)

# 총 구매 횟수 컬럼 생성
num_purchase_total = customer_df[['num_purchase_web', 'num_purchase_store', 'num_purchase_discount']].sum(axis = 1)
num_purchase_loc = customer_df.columns.get_loc('num_purchase_discount') + 1
customer_df.insert(loc = num_purchase_loc, column = 'num_purchase_total', value = num_purchase_total)

# 컬럼 생성, 데이터 타입 확인
customer_df.info()

# birth_year -> age 값 수정, 컬럼 이름 변경
customer_df['birth_year'] = 2026 - customer_df['birth_year']
customer_df = customer_df.rename(columns = {'birth_year' : 'age'})

# 고객 연령 분포 확인
sns.histplot(data = customer_df['age'])
plt.show()

# 고객 연령 이상치 확인
customer_df['age'].plot(kind = 'box')
plt.show()

# 고객 연령 이상치 제거, 확인
customer_df = customer_df[customer_df['age'] < 100]
customer_df['age'].plot(kind = 'box')
plt.show()

# 고객 연령 분포 재확인
sns.histplot(data = customer_df['age'])
plt.show()

# 고객 연령 구간화 (10대 ~ 70대), 컬럼 생성
age_bins = list(range(10, 81, 10))
age_labels = [f'{x}대' for x in age_bins[:-1]]

age_group = pd.cut(customer_df['age'], bins = age_bins, labels = age_labels, right = False)
age_group_loc = customer_df.columns.get_loc('age') + 1

customer_df.insert(loc = age_group_loc, column = 'age_group', value = age_group)

# 컬럼 생성 확인
customer_df.head()

# 연령대별 고객 수 확인
customer_df['age_group'].value_counts()

# 데이터 수가 적은 10대, 20대 컬럼과 60대, 70대 컬럼을 합치기
age_group_replace = {'10대' : '20대 이하', '20대' : '20대 이하', '60대' : '60대 이상', '70대' : '60대 이상'}
customer_df['age_group'] = customer_df['age_group'].astype(str).replace(age_group_replace)

# 연령대별 고객 수 재확인
customer_df['age_group'].value_counts()

# 고객 소득 분포 확인
sns.histplot(data = customer_df['annual_income'])
plt.show()

# 소득 이상치 확인
customer_df['annual_income'].plot(kind = 'box')
plt.show()

# 소득 이상치 삭제
q1 = customer_df['annual_income'].quantile(0.25)
q3 = customer_df['annual_income'].quantile(0.75)

iqr = q3 - q1

lower_limit = q1 - 1.5 * iqr
upper_limit = q3 + 1.5 * iqr

condition1 = customer_df['annual_income'] >= lower_limit
condition2 = customer_df['annual_income'] <= upper_limit

customer_df = customer_df[condition1 & condition2]

# 소득 이상치 삭제 확인
customer_df['annual_income'].plot(kind = 'box')
plt.show()

# recency 컬럼 데이터 분포 확인
sns.histplot(data = customer_df['recency'])
plt.show()

# 데이터 분포가 고르므로 3등급으로 나눠 새 컬럼 생성 (등급 값이 클수록 우수 고객)
recency_level = pd.cut(customer_df['recency'], bins = 3, labels = [3, 2, 1])
customer_df['recency_level'] = recency_level
customer_df['recency_level'] = customer_df['recency_level'].astype('int')

# recency 등급 별 고객 수 확인
customer_df['recency_level'].value_counts()

# recency 등급 별 데이터 확인
groupby_recency_level = customer_df.groupby('recency_level').sum(numeric_only = True).reset_index()
groupby_recency_level

# recency 등급 별 매출 기여도 확인
groupby_recency_level['amount_total'].plot(kind = 'pie', autopct = '%.1f%%', labels = ['3등급', '2등급', '1등급'], title = 'Recency 등급 별 매출 기여도')
plt.show()

# frequency 등급 나누고 새 컬럼 생성 (등급 값이 클수록 우수 고객)
frequency_level = pd.cut(customer_df['num_purchase_total'], bins = 3, labels = [1, 2, 3])
customer_df['frequency_level'] = frequency_level
customer_df['frequency_level'] = customer_df['frequency_level'].astype('int')

# frequency 등급 별 고객 수 확인
customer_df['frequency_level'].value_counts()

# 등급 별 고객 수가 균등할 수 있도록 조정
frequency_level = pd.qcut(customer_df['num_purchase_total'], q = 3, labels = [1, 2, 3])
customer_df['frequency_level'] = frequency_level
customer_df['frequency_level'] = customer_df['frequency_level'].astype('int')

# frequency 등급 별 고객 수 재확인
customer_df['frequency_level'].value_counts()

# frequency 등급 별 데이터 확인
groupby_frequency_level = customer_df.groupby('frequency_level').sum(numeric_only = True).reset_index()
groupby_frequency_level

# frequency 그룹 별 매출 기여도 확인
groupby_frequency_level['amount_total'].plot(kind = 'pie', autopct = '%.1f%%', labels = ['1등급', '2등급', '3등급'], title = 'Frequency 등급 별 매출 기여도')
plt.show()

# monetary 등급 나누고 새 컬럼 생성
monetary_level = pd.qcut(customer_df['amount_total'], q = 3, labels = [1, 2, 3])
customer_df['monetary_level'] = monetary_level
customer_df['monetary_level'] = customer_df['monetary_level'].astype('int')

# monetary 등급 별 고객 수 확인
customer_df['monetary_level'].value_counts()

# monetary 그룹 별 데이터 확인
groupby_monetary_level = customer_df.groupby('monetary_level').sum(numeric_only = True).reset_index()
groupby_monetary_level

# monetary 그룹 별 매출 기여도 확인
groupby_monetary_level['amount_total'].plot(kind = 'pie', autopct = '%.1f%%', labels = ['1등급', '2등급', '3등급'], title = 'Monetary 등급 별 매출 기여도')
plt.show()

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