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
