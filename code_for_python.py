# %% [markdown]
# # Lesson Notes: Advanced Pandas

# %%
import pandas as pd
import numpy as np

# %% [markdown]
# ### Combining Series and DataFrames
# -   `pd.concat()` - Alows us to add together DF of similar shape
# -   `pd.append()`
# -   `pd.merge()` - similar to `JOIN` in SQL
# -   `pd.join()`

# %% [markdown]
# #### pd.concat()

# %%
# .concat()
df1 = pd.DataFrame(
    {
        "A": ["A0", "A1", "A2", "A3"],
        "B": ["B0", "B1", "B2", "B3"],
        "C": ["C0", "C1", "C2", "C3"],
        "D": ["D0", "D1", "D2", "D3"],
    },

)


df2 = pd.DataFrame(
    {
        "A": ["A4", "A5", "A6", "A7"],
        "B": ["B4", "B5", "B6", "B7"],
        "C": ["C4", "C5", "C6", "C7"],
        "D": ["D4", "D5", "D6", "D7"],
    },

)


df3 = pd.DataFrame(
    {
        "A": ["A8", "A9", "A10", "A11"],
        "B": ["B8", "B9", "B10", "B11"],
        "C": ["C8", "C9", "C10", "C11"],
        "D": ["D8", "D9", "D10", "D11"],
    },

)

frames = [ df1, df2, df3 ]

# ignore_index to create a new index starting from 0 - n
result = pd.concat(frames, ignore_index=True)

result

# %%
# use keys to delineate the difference concatenated df
# allows tracking of original DF
result = pd.concat(frames, keys=['x', 'y', 'z'])
result

# %%
# Allows extraction of the original df objects
result_y = result.loc[('y')]
result_y

# %%
df4 = pd.DataFrame(
    {
        "B": ["B2", "B3", "B6", "B7"],
        "D": ["D2", "D3", "D6", "D7"],
        "F": ["F2", "F3", "F6", "F7"],
    },
    index=[12, 13, 14, 15],
)

df4

# %%
# if our df have mismatched columns. Nan is filled in where they dont overlap
result = pd.concat([df1, df4], ignore_index=True, sort=False)
result

# %%
result = pd.concat([df1, df4], ignore_index=True, axis=1, sort=False)
result

# %% [markdown]
# #### pd.merge() - similar to JOIN SQL. Combining on index or column

# %%
left_df = pd.DataFrame({'Courses': ["Spark","PySpark","Python","pandas","Java"],
                    'Fee' : [20000,25000,30000,24000,40000],
                    'Duration':['30day','40days','60days','55days','50days']})

right_df = pd.DataFrame({'Courses': ["Java","PySpark","Python","pandas","Hyperion","html"],
                    'Fee': [20000,25000,30000,24000,40000,4000],
                    'Percentage':['10%','20%','25%','20%','10%','50%']})

# %%
left_df

# %%
right_df

# %%
# without any arguments, inner join
merged_df = pd.merge(left_df, right_df)
merged_df

# %%
# merged all matching values in courses table
merged_df = pd.merge(left_df, right_df, on='Courses')
merged_df

# %%
merged_df = pd.merge(left_df, right_df, on=['Courses', 'Fee'])
merged_df

# %%
# almost a left join
merged_df = pd.merge(left_df, right_df, how='left', left_on=['Courses', 'Fee'], right_on=['Courses', 'Fee'])
merged_df

# %%
left = pd.DataFrame({"A": [1, 2], "B": [1, 2]})

right = pd.DataFrame({"A": [4, 5, 6], "B": [2, 2, 2]})

# %%
result = pd.merge(left, right, on='B', how='inner')
result

# %%
result = pd.merge(left, right, on='B', how='inner', validate='one_to_many')
result

# %%
sales_data = {
    'TransactionID': [1, 2, 3, 4, 5],
    'ProductID': [101, 102, 103, 101, 105],
    'StoreID': [1, 2, 1, 3, 2],
    'Quantity': [5, 3, 2, 4, 1],
    'Amount': [500.00, 300.00, 200.00, 400.00, 150.00]
}

products_data = {
    'ProductID': [101, 102, 103, 104, 105],
    'ProductName': ['Laptop', 'Headphones', 'Smartphone', 'Tablet', 'Monitor'],
    'Category': ['Electronics', 'Electronics', 'Electronics', 'Electronics', 'Electronics']
}

# %%
sale_df = pd.DataFrame(sales_data)
prod_df = pd.DataFrame(products_data)

merged_df = pd.merge(sale_df, prod_df, on='ProductID', how='left')

merged_df = merged_df.drop('ProductID', axis=1)

merged_df

# %% [markdown]
# #### pd.join()

# %%
technologies = {
    'Courses':["Spark","PySpark","Python","pandas"],
    'Fee' :[20000,25000,22000,30000],
    'Duration':['30days','40days','35days','50days'],
              }
index_labels=['r1','r2','r3','r4']

technologies2 = {
    'Courses':["Spark","Java","Python","Go"],
    'Discount':[2000,2300,1200,2000]
              }
index_labels2=['r1','r6','r3','r5']

# %%
df1 = pd.DataFrame(technologies, index=index_labels)
df2 = pd.DataFrame(technologies2, index=index_labels2)

# %%
# left join
df3 = df1.join(df2, lsuffix='_left', rsuffix='_right')
df3

# %%
# inner join
df3 = df1.join(df2, lsuffix='_left', rsuffix='_right', how='inner')
df3

# %%
# right join
df3 = df1.join(df2, lsuffix='_left', rsuffix='_right', how='right')
df3

# %%
#joining df and setting new indexes
df3 = df1.set_index('Courses').join(df2.set_index('Courses'), how='inner')
df3

# %% [markdown]
# # Grouping and Aggregation
# -   `df(series).aggregate(func)`

# %%
zoo = pd.read_csv('data/zoo.csv')
print(zoo)

# %%
zoo.count()

# %%
print(zoo[['animal']].count())
print(zoo.animal.count())

# %%
print(zoo['water_need'].sum())
print(zoo.water_need.sum())

# %%
print(zoo.sum())

# %%
# Min, Max, Mean, Median water needed
min_water = zoo['water_need'].min()
max_water = zoo['water_need'].max()
mean_water = zoo['water_need'].mean()
median_water = zoo['water_need'].median()

print(f'Min Water: {min_water}')
print(f'Max Water: {max_water}')
print(f'Mean Water: {mean_water}')
print(f'Median water: {median_water}')

# %%
# mean / median of each type of animal
zoo.groupby('animal').mean()

# %%
zoo.groupby('animal').mean()[['water_need']]

# %%
zoo.groupby('animal').mean().water_need

# %%
zoo.groupby('animal')['animal'].count()

# %% [markdown]
# ## Group by with student scores

# %%
df = pd.read_csv('data/student_scores.csv', parse_dates=['birth'])

# shape
rows, cols = df.shape
print(f'Rows: {rows}')
print(f'Cols: {cols}')

#descriptive stats
df.describe()

# %%
df.info()

# %%
df

# %%
item_group = df.groupby('first_name')
item_group.groups

# %%
# group by multiple columns
multi_group = df.groupby(['first_name', 'last_name'])
multi_group.groups

# %%
# looping/iterating through groups
for name, group in item_group:
    print(f'{name}')
    print(group)

# %%
subject_group = df.groupby('Subject')
subject_group.groups

# .get_group() to then grab a specific group
subject_group.get_group('Calculus')

# %%
agg_group_mean = df.groupby('Subject')['score'].mean()
agg_group_mean

# %%
student_means = df.groupby(['first_name', 'last_name'])['score'].mean()
print(student_means)

# %%
agg_group = df.groupby(['first_name', 'last_name'])['score'].agg([np.mean, np.sum, np.median, np.min, np.max])
print(agg_group)

# %%
student_count = df.groupby(['first_name', 'last_name'])['id'].count()
student_count

# %% [markdown]
# ### Tranforming Data, CUMSUM, Diff()

# %%
df = pd.read_csv('data/sales_transactions.csv')
df

# %%
order_total = df.groupby('order')['ext price'].sum()
order_total

# %%
# tranform takes the place of agg() and allows us to add those values to then end of the og dataframe (if we wanted)
order_total = df.groupby('order')['ext price'].transform('sum')
order_total

# %%
# take the return value of the broupby transform and make it a new column in our df
df['Order Total'] = df.groupby('order')['ext price'].transform('sum')
df

# %%
df['Percent of Order'] = df['ext price'] / df['Order Total']
df

# %% [markdown]
# #### .diff() - difference invalue from one cell of a sereies to the next

# %%
np.random.seed(seed=13)

df = pd.DataFrame(data=np.random.normal(loc=70, scale=10, size=(7,3)),
           columns=('San Francisco', 'San Diego', 'Los Angeles'),
            index=['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun']
)

df = df.round()

df

# %%
df.diff()

# %%
df.diff(periods=2)

# %%
# Diff of the horizontal Axis
df.diff(axis=1)

# %%
df = pd.DataFrame({'period': [1, 2, 3, 4, 5, 6, 7, 8],
                   'sales': [12, 14, 15, 15, 18, 20, 19, 24],
                   'returns': [2, 2, 3, 3, 5, 4, 4, 6]})

df

# %%
# claculate the diff from a row 3 down from current
df['sales_diff'] =  df['sales'].diff()
df

# %%
# grab records conditionally

df[ df['sales_diff'] < 2 ]

# %%



