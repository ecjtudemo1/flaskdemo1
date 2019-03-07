import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.formula.api import ols, glm
wine = pd.read_csv(open('D:/tensorflow学习资料/111.csv'), sep=',', header=0)
wine.columns = wine.columns.str.replace(' ', '_')
# 检查标题行和前5条数据
print(wine.head())
# 显示所有变量的描述性统计量m
print(wine.describe())
# 找出唯一值
print(sorted(wine.quality.unique()))
# 计算值的频率
print(wine.quality.value_counts())
# 按照葡萄酒类型显示质量的描述性统计量
print(wine.groupby('type')[['quality']].describe().unstack('type'))
# 按照葡萄酒类型显示质量的特定分位数值
print(wine.groupby('type')[['quality']].quantile([0.25, 0.75]).unstack('type'))
# 按照葡萄酒类型查看质量分布
red_wine = wine.loc[wine['type']=='red', 'quality']
white_wine = wine.loc[wine['type']=='white', 'quality']
sns.set_style("dark")
print(sns.distplot(red_wine, \
 norm_hist=True, kde=False, color="red", label="Red wine"))
print(sns.distplot(white_wine, \
 norm_hist=True, kde=False, color="white", label="White wine"))
#sns.axlabel("data", "data1")
plt.title("Distribution of Quality by Wine Type")
plt.legend()
plt.show()
# 检验红葡萄酒和白葡萄酒的平均质量是否有所不同
print(wine.groupby(['type'])[['quality']].agg(['std']))
tstat, pvalue, df = sm.stats.ttest_ind(red_wine, white_wine)
print('tstat: %.3f pvalue: %.4f' % (tstat, pvalue))
my_formula = 'quality ~ data + data1'
# 创建一个名为dependent_variable的序列来保存质量数据
dependent_variable = wine['quality']
# 创建一个名为independent variables的数据框
# 来保存初始的葡萄酒数据集中除quality、type和in_sample之外的所有变量
independent_variables = wine[wine.columns.difference(['quality', 'type',\
'in_sample'])]
# 对自变量进行标准化
# 对每个变量，在每个观测中减去变量的均值
# 并且使用结果除以变量的标准差
independent_variables_standardized = (independent_variables -\
independent_variables.mean()) / independent_variables.std()
# 将因变量quality作为一列添加到自变量数据框中
# 创建一个带有标准化自变量的
# 新数据集
wine_standardized = pd.concat([dependent_variable, independent_variables_standardized], axis=1)
lm_standardized = ols(my_formula, data=wine_standardized).fit()
## 或者，也可以使用广义线性模型（glm）语法进行线性回归
## lm = glm(my_formula, data=wine, family=sm.families.Gaussian()).fit()
print(lm_standardized.summary())
print("\nQuantities you can extract from the result:\n%s" % dir(lm_standardized))
print("\nCoefficients:\n%s" % lm_standardized.params)
print("\nCoefficient Std Errors:\n%s" %lm_standardized.bse)
print("\nAdj. R-squared:\n%.2f" % lm_standardized.rsquared_adj)
print("\nF-statistic: %.1f P-value: %.2f" % (lm_standardized.fvalue,lm_standardized.f_pvalue))
print("\nNumber of obs: %d Number of fitted values: %d" % (lm_standardized.nobs,\
len(lm_standardized.fittedvalues)))
new_observations = wine.ix[wine.index.isin(range(3)), \
independent_variables.columns]
# 基于新观测中的葡萄酒特性预测质量评分
y_predicted = lm_standardized.predict(new_observations)
# 将预测值保留两位小数并打印到屏幕上
y_predicted_rounded = [round(score, 2) for score in y_predicted]
print(y_predicted_rounded)