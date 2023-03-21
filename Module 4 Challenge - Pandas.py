#!/usr/bin/env python
# coding: utf-8

# In[59]:


import pandas as pd


# In[60]:


data = pd.read_csv('/Users/anisabraun/Documents/district.csv')
schools = pd.read_csv('/Users/anisabraun/Documents/students_complete.csv')


# In[61]:


pd.options.display.max_columns = None
display(data)
display(schools)


# In[62]:


data_all = pd.merge(data, schools, how="left", on=["school_name", "school_name"])


# In[63]:


data_all.head()


# In[93]:


total_schools = len(data_all.school_name.unique())
total_students = data_all.student_name.count()
total_budget = sum(data_all.budget.unique())
avg_math_score = data_all.math_score.mean()
avg_reading_score = data_all.reading_score.mean()
pass_math = (data_all[data_all['math_score'] >= 70].math_score.count()) / total_students
pass_read = (data_all[data_all['reading_score'] >= 70].reading_score.count()) / total_students
all_pass = (pass_math + pass_read)/2



# In[94]:


district_summary = pd.DataFrame({"Total Schools":[total_schools],
                                 "Total Students":[total_students],
                                 "Total Budget":[total_budget],
                                 "Average Math Score":[avg_math_score],
                                 "Average Reading Score":[avg_reading_score],
                                 "% Passing Math":[pass_math*100],
                                 "% Passing Reading":[pass_read*100],
                                 "% Overall Passing Rate":[all_pass*100]})


# In[95]:


district_summary.head()


# In[98]:


school_summary = data_all.groupby(['school_name'])
school_names = data_all.school_name.sort_values().unique()
school_types = data.sort_values(by="school_name").type
school_total_students = list(school_summary.student_name.count())
school_budget = list(school_summary.budget.mean())
school_per_student_budget = [i/j for i,j in zip(school_budget,school_total_students)]
school_avg_math_score = list(school_summary.math_score.mean())
school_avg_reading_score = list(school_summary.reading_score.mean())


school_summary = data_all[data_all['math_score'] >= 70].groupby(['school_name'])
school_pct_passing_math = [(i/j)*100 for i,j in zip(school_summary.math_score.count(),school_total_students)]
school_summary = data_all[data_all['reading_score'] >= 70].groupby(['school_name'])
school_pct_passing_reading = [(i/j)*100 for i,j in zip(school_summary.reading_score.count(),school_total_students)]
school_overall_passing = [(i+j)/2 for i,j in zip(school_pct_passing_math,school_pct_passing_reading)]

school_summary_df = pd.DataFrame({"School Names":school_names,
                                  "School Type":school_types,
                                  "Total Students":school_total_students,
                                  "Total School Budget":school_budget,
                                  "Per Student Budget":school_per_student_budget,
                                  "Average Math Score":school_avg_math_score,
                                  "Average Reading Score":school_avg_reading_score,
                                  "% Passing Math":school_pct_passing_math,
                                  "% Passing Reading":school_pct_passing_reading,
                                  "Overall Passing Rate":school_overall_passing})

school_summary_df = school_summary_df.reset_index(drop=True)
school_summary_df


# In[99]:


bot_5 = school_summary_df.sort_values(by='Overall Passing Rate', ascending=True).head(5).reset_index(drop=True)
bot_5


# In[107]:


def average_math_by_grade(grade):
    school_summary = data_all.loc[data_all.grade == grade].groupby(['school_name'])
    school_names = data_all.school_name.sort_values().unique()
    school_avg_math_score = list(school_summary.math_score.mean())

 
    average_math_df = pd.DataFrame({"School Names":school_names,
                                    f"{grade} Avg Math Score":school_avg_math_score})

    average_math_df = average_math_df.reset_index(drop=True)
    return average_math_df


def average_reading_by_grade(grade):
    school_summary = data_all.loc[data_all.grade == grade].groupby(['school_name'])
    school_names = data_all.school_name.sort_values().unique()
    school_avg_reading_score = list(school_summary.reading_score.mean())

   
    average_reading_df = pd.DataFrame({"School Names":school_names,
                                    f"{grade} Avg Reading Score":school_avg_reading_score})

    average_reading_df = average_reading_df.reset_index(drop=True)
    return average_reading_df


# In[108]:


grade_9 = average_math_by_grade('9th')
grade_10 = average_math_by_grade('10th')
grade_11 = average_math_by_grade('11th')
grade_12 = average_math_by_grade('12th')
avg_math_score_by_grade = pd.merge(grade_9,grade_10,how='inner',suffixes=('',''))
avg_math_score_by_grade = pd.merge(avg_math_score_by_grade,grade_11,how='inner',suffixes=('',''))
avg_math_score_by_grade = pd.merge(avg_math_score_by_grade,grade_12,how='inner',suffixes=('',''))
avg_math_score_by_grade


# In[109]:


grade_9 = average_reading_by_grade('9th')
grade_10 = average_reading_by_grade('10th')
grade_11 = average_reading_by_grade('11th')
grade_12 = average_reading_by_grade('12th')
avg_reading_score_by_grade = pd.merge(grade_9,grade_10,how='inner',suffixes=('',''))
avg_reading_score_by_grade = pd.merge(avg_reading_score_by_grade,grade_11,how='inner',suffixes=('',''))
avg_reading_score_by_grade = pd.merge(avg_reading_score_by_grade,grade_12,how='inner',suffixes=('',''))
avg_reading_score_by_grade


# In[110]:


spending_bins = [0, 585, 615, 645, 675]
group_names = ["<$585", "$585-615", "$615-645", "$645-675"]

scores_by_spending = school_summary_df[["School Names",
                                    "Average Math Score",
                                    "Average Reading Score",
                                    "% Passing Math",
                                    "% Passing Reading",
                                    "Overall Passing Rate"]]
scores_by_spending["Spending Summary"] = pd.cut(school_summary_df["Per Student Budget"], spending_bins, labels=group_names)
scores_by_spending = scores_by_spending.groupby(["Spending Summary"])
scores_by_spending.mean()


# In[111]:


size_bins = [0, 1000, 2000, 5000]
group_names = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]

scores_by_school_size = school_summary_df[["School Names",
                                    "Average Math Score",
                                    "Average Reading Score",
                                    "% Passing Math",
                                    "% Passing Reading",
                                    "Overall Passing Rate"]]
scores_by_school_size["School Size Summary"] = pd.cut(school_summary_df["Total Students"], size_bins, labels=group_names)
scores_by_school_size = scores_by_school_size.groupby(["School Size Summary"])
scores_by_school_size.mean()


# In[112]:


scores_by_type = school_summary_df[["School Names",
                                    "School Type",
                                    "Average Math Score",
                                    "Average Reading Score",
                                    "% Passing Math",
                                    "% Passing Reading",
                                    "Overall Passing Rate"]]
scores_by_type = scores_by_type.groupby("School Type")
scores_by_type.mean()


# In[ ]:




