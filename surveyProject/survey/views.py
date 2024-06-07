import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import squarify
import base64
from django.shortcuts import render
from io import BytesIO

data2020 = pd.read_csv("C:/SURVEY_ANALYSIS/DATA/stack-overflow-developer-survey-2020/survey_results_public.csv")
data2023 = pd.read_csv("C:/SURVEY_ANALYSIS/DATA/stack-overflow-developer-survey-2023/survey_results_public.csv")
num_rows = 64441
data23_limited = data2023.head(num_rows)


def used_tech(request):
    return render(request, 'survey/tech.html')


def stack_license(request):
    return render(request, 'survey/license.html')


def survey_summary(request):
    return render(request, 'survey/summary.html')


def survey_description(request):
    return render(request, 'survey/about.html')


def survey_results(request):
    data1 = load_csv_file1()
    chart1 = generate_chart_data1(data1)

    data2 = load_csv_file2()
    chart2 = generate_chart_data2(data2)

    return render(request, 'survey/age_results.html', {'chart1': chart1, 'chart2': chart2})


def load_csv_file1():
    data2020['Age'].fillna(-1, inplace=True)

    col = 'Age'
    conditions = [
        (data2020[col] > 0) & (data2020[col] <= 18),
        (data2020[col] > 18) & (data2020[col] <= 24),
        (data2020[col] > 24) & (data2020[col] <= 34),
        (data2020[col] > 34) & (data2020[col] <= 44),
        (data2020[col] > 44) & (data2020[col] <= 54),
        (data2020[col] > 54) & (data2020[col] <= 64),
        (data2020[col] > 64),
        (data2020[col] == -1)
    ]
    choices = [
        '18 and less',
        '18-24',
        '25-34',
        '35-44',
        '45-54',
        '55-64',
        '65 or older',
        'Prefer not to say'
    ]
    data2020['age_cat'] = np.select(conditions, choices)

    data2020['age_cat'] = pd.Categorical(data2020['age_cat'], categories=choices, ordered=False)

    value_counts = data2020['age_cat'].value_counts().reindex(choices)

    return value_counts


def load_csv_file2():
    age_replacements = {
        'Under 18 years old': '18 and less',
        '18-24 years old': '18-24',
        '25-34 years old': '25-34',
        '35-44 years old': '35-44',
        '45-54 years old': '45-54',
        '55-64 years old': '55-64',
        '65 years or older': '65 or older',
        'Prefer not to say': 'Prefer not to say'
    }
    data23_limited['Age'].replace(age_replacements, inplace=True)

    choices = [
        '18 and less',
        '18-24',
        '25-34',
        '35-44',
        '45-54',
        '55-64',
        '65 or older',
        'Prefer not to say',
    ]

    data23_limited['Age'] = pd.Categorical(data23_limited['Age'], categories=choices, ordered=True)

    grouped_data23_lim = data23_limited['Age'].value_counts().reindex(choices, fill_value=0)

    return grouped_data23_lim


def generate_chart_data1(value_counts):
    plt.figure()
    ax = value_counts.plot(kind='bar',
                           title='Number of respondents in particular age group in 2020',
                           ylabel="Number of respondents in each group",
                           xlabel="Age group",
                           figsize=(8, 6),
                           legend=False)

    for i, v in enumerate(value_counts):
        ax.text(i, v + 1, str(v), ha='center', va='bottom')

    plt.xticks(rotation=90)
    plt.yticks(np.arange(0, 27500, 2500))
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close()

    graphic1 = base64.b64encode(image_png).decode('utf-8')

    return graphic1


def generate_chart_data2(grouped_data23_lim):
    plt.figure()
    ax = grouped_data23_lim.plot(kind='bar',
                                 title='Number of respondents in particular age group in 2023',
                                 ylabel="Number of respondents in each group",
                                 xlabel="Age group",
                                 figsize=(8, 6),
                                 legend=False,
                                 color='navy')

    for i, v in enumerate(grouped_data23_lim):
        ax.text(i, v + 0.5, str(v), ha='center', va='bottom')

    plt.xticks(rotation=90)
    plt.yticks(np.arange(0, 27500, 2500))
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close()

    graphic2 = base64.b64encode(image_png).decode('utf-8')

    return graphic2


def generate_combined_age_chart(data2020, data23_limited):
    fig, ax = plt.subplots(figsize=(10, 5))

    # Bar width and positions
    bar_width = 0.35
    index = np.arange(len(data2020.index))

    # Bars for 2020
    bars_2020 = ax.bar(index, data2020.values, bar_width, label='2020', color='skyblue')
    # Bars for 2023
    bars_2023 = ax.bar(index + bar_width, data23_limited.values, bar_width, label='2023', color='#4f6d7a')

    # Adding the data labels on top of the bars
    for bar in bars_2020:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, yval + 1, int(yval), ha='center', va='bottom', color='black')

    for bar in bars_2023:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, yval + 1, int(yval), ha='center', va='bottom', color='black')

    ax.set_xlabel('Age Group')
    ax.set_ylabel('Number of Respondents')
    ax.set_xticks(index + bar_width / 2)
    ax.set_xticklabels(data2020.index, rotation=90)
    ax.legend()

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close()

    combined_chart = base64.b64encode(image_png).decode('utf-8')

    return combined_chart


def age_compared(request):
    data1 = load_csv_file1()
    data2 = load_csv_file2()
    combined_chart = generate_combined_age_chart(data1, data2)

    return render(request, 'survey/age_compared.html', {'combined_chart': combined_chart})


# main branch 2020 and 2023
def main_b_results(request):
    data3 = load_csv_file3()
    chart3 = generate_chart_data3(data3)

    data4 = load_csv_file4()
    chart4 = generate_chart_data4(data4)

    return render(request, 'survey/main_b_results.html', {'chart3': chart3, 'chart4': chart4})


def load_csv_file3():
    data2020['MainBranch'].fillna('None of these', inplace=True)
    counts_2020 = data2020['MainBranch'].value_counts()

    return counts_2020


def generate_chart_data3(counts_2020):
    plt.figure(figsize=(8, 6))
    bars_2020 = plt.bar(counts_2020.index, counts_2020.values, width=0.5, color='skyblue')

    for bar in bars_2020:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.02 * max(counts_2020.values), int(yval), ha='center',
                 va='bottom', color='navy')

    plt.xticks(rotation=90)
    plt.yticks(np.arange(0, 55000, 5000))
    plt.title('Main branch in 2020')
    plt.ylabel('Number of respondents')
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close()

    graphic3 = base64.b64encode(image_png).decode('utf-8')

    return graphic3


def load_csv_file4():
    counts_2023 = data23_limited['MainBranch'].value_counts()

    return counts_2023


def generate_chart_data4(counts_2023):
    plt.figure(figsize=(8, 6))
    bars_2023 = plt.bar(counts_2023.index, counts_2023.values, width=0.5, color='green')
    for bar in bars_2023:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.02 * max(counts_2023.values), int(yval), ha='center',
                 va='bottom', color=(0, 0.2, 0))
    plt.xticks(rotation=90)
    plt.yticks(np.arange(0, 55000, 5000))
    plt.title('Main branch in 2023')
    plt.ylabel('Number of respondents')
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close()

    graphic4 = base64.b64encode(image_png).decode('utf-8')

    return graphic4


# level of education 2020 and 2023
def level_of_education(request):
    data5 = load_csv_file5()
    chart5 = generate_chart_data5(data5)

    data6 = load_csv_file6()
    chart6 = generate_chart_data6(data6)

    return render(request, 'survey/level_of_edu.html', {'chart5': chart5, 'chart6': chart6})


def load_csv_file5():
    data2020['EdLevel'].replace('Secondary school (e.g. American high school, German Realschule or Gymnasium, etc.)',
                                'Secondary school', inplace=True)
    data2020['EdLevel'].replace('Associate degree (A.A., A.S., etc.)',
                                'Associate degree', inplace=True)
    data2020['EdLevel'].replace('Bachelor’s degree (B.A., B.S., B.Eng., etc.)',
                                'Bachelor’s degree', inplace=True)
    data2020['EdLevel'].replace('Master’s degree (M.A., M.S., M.Eng., MBA, etc.)',
                                'Master’s degree', inplace=True)
    data2020['EdLevel'].replace('Professional degree (JD, MD, etc.)',
                                'Professional degree', inplace=True)
    data2020['EdLevel'].replace('Professional degree (JD, MD, etc.)',
                                'Professional degree', inplace=True)
    data2020['EdLevel'].replace('Other doctoral degree (Ph.D., Ed.D., etc.)',
                                'Professional degree', inplace=True)
    data2020['EdLevel'].replace('I never completed any formal education',
                                'Something else', inplace=True)

    ed_level_2020 = data2020['EdLevel'].value_counts()

    return ed_level_2020


def generate_chart_data5(ed_level_2020):
    plt.figure()
    bars_ed_lev_2020 = plt.bar(ed_level_2020.index, ed_level_2020.values, width=0.5)
    for bar in bars_ed_lev_2020:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.02 * max(ed_level_2020.values), int(yval), ha='center',
                 va='bottom', color='black')
    plt.xticks(rotation=90)
    plt.yticks(np.arange(0, max(ed_level_2020.values * 1.1), 5000))
    plt.title('Level of formal education in 2020')
    plt.ylabel('Number of respondents')
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close()

    graphic5 = base64.b64encode(image_png).decode('utf-8')

    return graphic5


def load_csv_file6():

    data23_limited['EdLevel'].replace(
        'Secondary school (e.g. American high school, German Realschule or Gymnasium, etc.)',
        'Secondary school', inplace=True)
    data23_limited['EdLevel'].replace('Associate degree (A.A., A.S., etc.)', 'Associate degree', inplace=True)
    data23_limited['EdLevel'].replace('Bachelor’s degree (B.A., B.S., B.Eng., etc.)', 'Bachelor’s degree', inplace=True)
    data23_limited['EdLevel'].replace('Master’s degree (M.A., M.S., M.Eng., MBA, etc.)', 'Master’s degree',
                                      inplace=True)
    data23_limited['EdLevel'].replace('Professional degree (JD, MD, Ph.D, Ed.D, etc.)', 'Professional degree',
                                      inplace=True)

    counts_bars_edu_23 = data23_limited['EdLevel'].value_counts()

    return counts_bars_edu_23


def generate_chart_data6(counts_bars_edu_23):
    plt.figure()
    bars_edu_23 = plt.bar(counts_bars_edu_23.index, counts_bars_edu_23.values, width=0.5, color='orange')
    for bar in bars_edu_23:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.02 * max(counts_bars_edu_23.values), int(yval),
                 ha='center',
                 va='bottom', color='black')
    plt.xticks(rotation=90)
    plt.yticks(np.arange(0, 30000, 5000))
    plt.title('Level of formal education in 2023')
    plt.ylabel('Number of respondents')
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close()

    # Encode the image to base64
    graphic6 = base64.b64encode(image_png).decode('utf-8')

    return graphic6


# 4th question
# Which programming, scripting, and markup languages have you done # extensive development work in over the past year,
# and which do you want to work # in over the next year? (If you both worked with the language and want to continue
# to do so, please check both boxes in that row.)

# language 2020
def lang_worked_with_20(request):
    data7 = load_csv_file7()
    chart7 = generate_chart_data7(data7)

    data8 = load_csv_file8()
    chart8 = generate_chart_data8(data8)

    return render(request, 'survey/lang_worked_with_20.html', {'chart7': chart7, 'chart8': chart8})


def load_csv_file7():
    df_expanded = data2020['LanguageWorkedWith'].str.split(';', expand=True)

    df_long = df_expanded.melt(var_name='variable', value_name='value').dropna()

    value_counts_lang = df_long['value'].value_counts()

    value_counts_df = value_counts_lang.reset_index()
    value_counts_df.columns = ['value', 'count']

    return value_counts_df


def generate_chart_data7(value_counts_df):
    plt.figure(figsize=(16, 10))

    y_pos = np.arange(len(value_counts_df)) * 2
    bars = plt.barh(y_pos, value_counts_df['count'], color='#32CD32', height=0.8)
    plt.yticks(y_pos, value_counts_df['value'])
    plt.xticks(np.arange(0, 40000, 2500), rotation=90)

    for bar in bars:
        plt.text(
            bar.get_width() + 0.1,  # x-coordinate for the text
            bar.get_y() + bar.get_height() / 2,  # y-coordinate for the text
            f'{int(bar.get_width())}',  # text to display
            va='center',  # vertical alignment
            fontsize=10
        )

    plt.subplots_adjust(left=0.2, right=0.9, top=0.9, bottom=0.1)  # Adjust bottom as needed

    plt.xlabel('Number of respondents')
    plt.ylabel('Language')
    plt.title('Language to have worked with in 2020')

    plt.gca().invert_yaxis()
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close()

    graphic7 = base64.b64encode(image_png).decode('utf-8')

    return graphic7


def load_csv_file8():
    df_expanded = data2020['LanguageDesireNextYear'].str.split(';', expand=True)

    # Melt the expanded DataFrame to long format
    df_long = df_expanded.melt(var_name='variable', value_name='value').dropna()

    # Count the occurrences of each value
    value_counts_lang = df_long['value'].value_counts()

    # Convert to DataFrame for easier plotting
    value_counts_df = value_counts_lang.reset_index()
    value_counts_df.columns = ['value', 'count']

    return value_counts_df


def generate_chart_data8(value_counts_df):
    plt.figure(figsize=(16, 10))

    y_pos = np.arange(len(value_counts_df)) * 2
    bars = plt.barh(y_pos, value_counts_df['count'], color='#006400', height=0.8)
    plt.yticks(y_pos, value_counts_df['value'])
    plt.xticks(np.arange(0, 30000, 2500), rotation=90)

    for bar in bars:
        plt.text(
            bar.get_width() + 0.1,
            bar.get_y() + bar.get_height() / 2,
            f'{int(bar.get_width())}',
            va='center',
            fontsize=10
        )

    plt.subplots_adjust(left=0.2, right=0.9, top=0.9, bottom=0.1)

    plt.xlabel('Number of respondents')
    plt.ylabel('Language')
    plt.title('Language want to work with next year')

    plt.gca().invert_yaxis()
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close()

    graphic8 = base64.b64encode(image_png).decode('utf-8')

    return graphic8


def tree_map_20(request):
    data9 = load_csv_file9()
    chart9 = generate_chart_data9(data9)
    data10 = load_csv_file10()
    chart10 = generate_chart_data10(data10)

    return render(request, 'survey/tree_map_20.html', {'chart9': chart9, 'chart10': chart10})


def load_csv_file9():
    df_expanded = data2020['LanguageWorkedWith'].str.split(';', expand=True)

    df_long = df_expanded.melt(var_name='variable', value_name='value').dropna()

    value_counts = df_long['value'].value_counts()

    total_count = value_counts.sum()
    value_percentages = (value_counts / total_count) * 100

    value_percentages_df = value_percentages[value_percentages > 1]

    return value_percentages_df


def generate_chart_data9(value_percentages_df):
    plt.figure(figsize=(12, 8))

    labels = [f'{name}\n ({value:.2f}%)' for name, value in
              zip(value_percentages_df.index, value_percentages_df.values)]

    # Define shades of brown
    colors = ['#F5DEB3', '#DEB887', '#D2B48C', '#BC8F8F', '#FFE4C4']

    squarify.plot(sizes=value_percentages_df.values, label=labels, alpha=.8, color=colors, edgecolor='black')
    plt.axis('off')
    plt.title('Language to have worked with in 2020 - values only above 1% included', fontsize=18)

    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close()

    graphic9 = base64.b64encode(image_png).decode('utf-8')

    return graphic9


def load_csv_file10():
    df_expanded = data2020['LanguageDesireNextYear'].str.split(';', expand=True)

    df_long = df_expanded.melt(var_name='variable', value_name='value').dropna()

    value_counts = df_long['value'].value_counts()

    total_count = value_counts.sum()
    value_percentages = (value_counts / total_count) * 100

    value_percentages_df = value_percentages[value_percentages > 1]

    return value_percentages_df


def generate_chart_data10(value_percentages_df):
    plt.figure(figsize=(12, 8))

    labels = [f'{name}\n ({value:.2f}%)' for name, value in
              zip(value_percentages_df.index, value_percentages_df.values)]

    # Define shades of green
    colors = ['#B2DFDB', '#A5D6A7', '#C8E6C9', '#DCEDC8', '#E8F5E9']

    squarify.plot(sizes=value_percentages_df.values, label=labels, alpha=.8, color=colors, edgecolor='black')
    plt.axis('off')
    plt.title('Language declared to learn next year - values only above 1% included', fontsize=18)

    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close()

    graphic10 = base64.b64encode(image_png).decode('utf-8')

    return graphic10


# language 2023
def lang_worked_with_23(request):
    data11 = load_csv_file11()
    chart11 = generate_chart_data11(data11)

    data12 = load_csv_file12()
    chart12 = generate_chart_data12(data12)

    return render(request, 'survey/lang_worked_with_23.html', {'chart11': chart11, 'chart12': chart12})


def load_csv_file11():
    df_expanded = data23_limited['LanguageHaveWorkedWith'].str.split(';', expand=True)

    df_long = df_expanded.melt(var_name='variable', value_name='value').dropna()

    value_counts_lang = df_long['value'].value_counts()

    value_counts_df = value_counts_lang.reset_index()
    value_counts_df.columns = ['value', 'count']
    value_counts_df = value_counts_df.sort_values(by='count', ascending=False)

    return value_counts_df


def generate_chart_data11(value_counts_df):
    plt.figure(figsize=(16, 10))

    y_pos = np.arange(len(value_counts_df)) * 2
    bars = plt.barh(y_pos, value_counts_df['count'], color='#006400', height=0.8)
    plt.yticks(y_pos, value_counts_df['value'])
    plt.xticks(np.arange(0, 45000, 2500), rotation=90)

    for bar in bars:
        plt.text(
            bar.get_width() + 0.1,  # x-coordinate for the text
            bar.get_y() + bar.get_height() / 2,  # y-coordinate for the text
            f'{int(bar.get_width())}',  # text to display
            va='center',  # vertical alignment
            fontsize=10
        )

    plt.subplots_adjust(left=0.2, right=0.9, top=0.9, bottom=0.1)  # Adjust bottom as needed

    plt.xlabel('Number of respondents')
    plt.ylabel('Language')
    plt.title('Language to have worked with in 2023')

    plt.gca().invert_yaxis()
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close()

    graphic11 = base64.b64encode(image_png).decode('utf-8')

    return graphic11


def load_csv_file12():
    df_expanded = data23_limited['LanguageWantToWorkWith'].str.split(';', expand=True)

    df_long = df_expanded.melt(var_name='variable', value_name='value').dropna()

    value_counts_lang = df_long['value'].value_counts()

    value_counts_df = value_counts_lang.reset_index()
    value_counts_df.columns = ['value', 'count']
    value_counts_df = value_counts_df.sort_values(by='count', ascending=False)

    return value_counts_df


def generate_chart_data12(value_counts_df):
    plt.figure(figsize=(16, 10))

    y_pos = np.arange(len(value_counts_df)) * 2
    bars = plt.barh(y_pos, value_counts_df['count'], color='#006400', height=0.8)
    plt.yticks(y_pos, value_counts_df['value'])
    plt.xticks(np.arange(0, 30000, 2500), rotation=90)

    for bar in bars:
        plt.text(
            bar.get_width() + 0.1,
            bar.get_y() + bar.get_height() / 2,
            f'{int(bar.get_width())}',
            va='center',
            fontsize=10
        )

    plt.subplots_adjust(left=0.2, right=0.9, top=0.9, bottom=0.1)

    plt.xlabel('Number of respondents')
    plt.ylabel('Language')
    plt.title('Language want to work next year')

    plt.gca().invert_yaxis()
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close()

    graphic12 = base64.b64encode(image_png).decode('utf-8')

    return graphic12


def tree_map_23(request):
    data13 = load_csv_file13()
    chart13 = generate_chart_data13(data13)

    data14 = load_csv_file14()
    chart14 = generate_chart_data14(data14)

    return render(request, 'survey/tree_map_23.html', {'chart13': chart13, 'chart14': chart14})


def load_csv_file13():
    df_expanded = data23_limited['LanguageHaveWorkedWith'].str.split(';', expand=True)

    df_long = df_expanded.melt(var_name='variable', value_name='value').dropna()

    value_counts = df_long['value'].value_counts()

    total_count = value_counts.sum()
    value_percentages = (value_counts / total_count) * 100

    value_percentages_df = value_percentages[value_percentages > 1]

    return value_percentages_df


def generate_chart_data13(value_percentages_df):
    # Define the aspect ratio
    aspect_ratio = 4 / 3  # Example aspect ratio
    width = 18  # Adjust the width to make the plot larger
    height = width / aspect_ratio  # Calculate height to maintain the aspect ratio

    plt.figure(figsize=(width, height))

    labels = [f'{name} \n ({value:.2f}%)' for name, value in
              zip(value_percentages_df.index, value_percentages_df.values)]

    # Define shades of brown
    colors = ['#F5DEB3', '#DEB887', '#D2B48C', '#BC8F8F', '#FFE4C4']

    squarify.plot(
        sizes=value_percentages_df.values,
        label=labels,
        alpha=.8,
        color=colors,
        edgecolor='black',
        text_kwargs={'fontsize': 14}
    )
    plt.axis('off')
    plt.title('Language to have worked with in 2023 - values only above 1% included', fontsize=18)

    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close()

    graphic13 = base64.b64encode(image_png).decode('utf-8')

    return graphic13


def load_csv_file14():
    df_expanded = data23_limited['LanguageWantToWorkWith'].str.split(';', expand=True)

    df_long = df_expanded.melt(var_name='variable', value_name='value').dropna()

    value_counts = df_long['value'].value_counts()

    total_count = value_counts.sum()
    value_percentages = (value_counts / total_count) * 100

    value_percentages_df = value_percentages[value_percentages > 1]

    return value_percentages_df


def generate_chart_data14(value_percentages_df):
    # Define the aspect ratio
    aspect_ratio = 4 / 3  # Example aspect ratio
    width = 18  # Adjust the width to make the plot larger
    height = width / aspect_ratio  # Calculate height to maintain the aspect ratio

    plt.figure(figsize=(width, height))

    labels = [f'{name} \n ({value:.2f}%)' for name, value in
              zip(value_percentages_df.index, value_percentages_df.values)]

    # Define shades of green
    colors = ['#B2DFDB', '#A5D6A7', '#C8E6C9', '#DCEDC8', '#E8F5E9']

    squarify.plot(
        sizes=value_percentages_df.values,
        label=labels, alpha=.8,
        color=colors,
        edgecolor='black',
        text_kwargs={'fontsize': 14}
    )
    plt.axis('off')
    plt.title('Language declared to learn next year - values only above 1% included', fontsize=18)

    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close()

    graphic14 = base64.b64encode(image_png).decode('utf-8')

    return graphic14


# current job 2020
def current_job(request):
    data15 = load_csv_file15()
    chart15 = generate_chart_data15(data15)

    data16 = load_csv_file16()
    chart16 = generate_chart_data16(data16)

    return render(request, 'survey/current_job_20.html', {'chart15': chart15, 'chart16': chart16})


def load_csv_file15():
    data2020['PrimaryDevType'] = data2020['DevType'].apply(lambda x: x.split(';')[0] if pd.notna(x) else x)

    value_counts_lang = data2020['PrimaryDevType'].value_counts()

    value_counts_df_20 = value_counts_lang.reset_index()
    value_counts_df_20.columns = ['value', 'count']

    return value_counts_df_20


def generate_chart_data15(value_counts_df_20):
    plt.figure(figsize=(12, 8))

    # Create an array of positions for the bars
    y_pos = np.arange(len(value_counts_df_20))

    bars = plt.barh(y_pos, value_counts_df_20['count'], color='#B22222', height=0.8)

    # Set the y-ticks to be the positions with a specified label
    plt.yticks(y_pos, value_counts_df_20['value'])
    plt.xticks(np.arange(0, 20000, 2500), rotation=90)

    # Add values to each bar
    for bar in bars:
        plt.text(
            bar.get_width() + 0.1,  # x-coordinate for the text
            bar.get_y() + bar.get_height() / 2,  # y-coordinate for the text
            f'{int(bar.get_width())}',  # text to display
            va='center',  # vertical alignment
            fontsize=10
        )

    # Adjust plot margins to reduce space between the x-axis and the first y-axis value
    plt.subplots_adjust(left=0.2, right=0.9, top=0.9, bottom=0.1)

    plt.xlabel('Number of respondents')
    plt.title('Describe your current job in 2020')

    plt.gca().invert_yaxis()
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close()

    graphic15 = base64.b64encode(image_png).decode('utf-8')

    return graphic15


def load_csv_file16():
    counts_dev_23 = data23_limited['DevType'].value_counts()

    return counts_dev_23


def generate_chart_data16(counts_dev_23):
    plt.figure(figsize=(10, 8))
    bars_dev_23 = plt.barh(counts_dev_23.index, counts_dev_23.values, color='#800020', height=0.8)
    plt.xticks(np.arange(0, 20000, 2500), rotation=90)
    plt.yticks(counts_dev_23.index, counts_dev_23.index)

    for bar in bars_dev_23:
        plt.text(
            bar.get_x() + bar.get_width() + 100,
            bar.get_y() + bar.get_height() / 2,  # y-coordinate for the text
            f'{int(bar.get_width())}',  # text to display
            va='center',  # vertical alignment
            fontsize=10
        )

    plt.subplots_adjust(left=0.2, right=0.9, top=0.9, bottom=0.1)

    plt.title('Describe your current job in 2023')
    plt.xlabel('Number of respondents')

    plt.gca().invert_yaxis()
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close()

    graphic16 = base64.b64encode(image_png).decode('utf-8')

    return graphic16
