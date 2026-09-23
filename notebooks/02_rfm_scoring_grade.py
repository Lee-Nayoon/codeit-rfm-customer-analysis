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