import pandas as pd
import glob
import os


folder_with_data = r"C:\Users\milos_lkzm8yy\OneDrive\Desktop\100 micM_M"

first_5_minutes_df = pd.DataFrame()
last_5_minutes_df = pd.DataFrame()

total_files = 0

for file_path in glob.glob(os.path.join(folder_with_data, "*cropped*.csv")):
    # Read the CSV file
    df = pd.read_csv(file_path)

    # Convert start and end times to datetime objects
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # Calculate the duration of each activity
    df['Duration'] = (df['End Time'] - df['Start Time']).apply(lambda x: x.total_seconds())

    df["fly_index"] = total_files

    # Filter the data for the first 5 minutes and last 5 minutes
    first_5_minutes_data = df[(df['End Time'] <= pd.Timestamp('00:05:00'))]
    last_5_minutes_data = df[(df['Start Time'] >= pd.Timestamp('00:20:00'))]

    first_5_minutes_df = pd.concat([first_5_minutes_df, first_5_minutes_data], ignore_index=True)
    last_5_minutes_df = pd.concat([last_5_minutes_df, last_5_minutes_data], ignore_index=True)

    total_files += 1


results = []

raw_sum_duratioin_first_5_df = pd.DataFrame()
raw_sum_duratioin_last_5_df = pd.DataFrame()
raw_count_first_5_df = pd.DataFrame()
raw_count_last_5_df = pd.DataFrame()

labels_in_first_and_last_5_min = set(first_5_minutes_df["Label Name"].unique()).union(set(last_5_minutes_df["Label Name"].unique()))

# Calculate the average and standard deviation for each label for the first 5 minutes and last 5 minutes
for label in labels_in_first_and_last_5_min:
    label_data_first_5_minutes = first_5_minutes_df[first_5_minutes_df['Label Name'] == label]
    label_data_last_5_minutes = last_5_minutes_df[last_5_minutes_df['Label Name'] == label]

    raw_sum_duratioin_first_5_df = pd.concat([raw_sum_duratioin_first_5_df, 
                                              pd.DataFrame(label_data_first_5_minutes.groupby("fly_index")["Duration"].sum()).rename(columns={"Duration": label})], axis=1)
    raw_sum_duratioin_last_5_df = pd.concat([raw_sum_duratioin_last_5_df, 
                                            pd.DataFrame(label_data_last_5_minutes.groupby("fly_index")["Duration"].sum()).rename(columns={"Duration": label})], axis=1)

    raw_count_first_5_df = pd.concat([raw_count_first_5_df, 
                                              pd.DataFrame(label_data_first_5_minutes.groupby("fly_index")["Label Name"].count()).rename(columns={"Label Name": label})], axis=1)
    raw_count_last_5_df = pd.concat([raw_count_last_5_df, 
                                            pd.DataFrame(label_data_last_5_minutes.groupby("fly_index")["Label Name"].count()).rename(columns={"Label Name": label})], axis=1)

    results.append({
        'Label': label,
        'Sum duration for first 5 minutes': label_data_first_5_minutes['Duration'].sum(),
        'Average of the sums of durations for first 5 minutes': label_data_first_5_minutes.groupby("fly_index")["Duration"].sum().mean(),
        'Standard deviation of the sums of durations for first 5 minutes': label_data_first_5_minutes.groupby("fly_index")["Duration"].sum().std(),
        'Average duration for first 5 minutes': label_data_first_5_minutes['Duration'].mean(),
        'Standard deviation for first 5 minutes': label_data_first_5_minutes['Duration'].std(),

        'Sum duration for last 5 minutes': label_data_last_5_minutes['Duration'].sum(),
        'Average of the sums of durations for last 5 minutes': label_data_last_5_minutes.groupby("fly_index")["Duration"].sum().mean(),
        'Standard deviation of the sums of durations for last 5 minutes': label_data_last_5_minutes.groupby("fly_index")["Duration"].sum().std(),
        'Average duration for last 5 minutes': label_data_last_5_minutes['Duration'].mean(),
        'Standard deviation for last 5 minutes': label_data_last_5_minutes['Duration'].std()
    })

df_results = pd.DataFrame(results)
results_path = os.path.join(os.getcwd(),"results_fX100_M.xlsx")
df_results.fillna(0).to_excel(results_path)

first_5_path = os.path.join(os.getcwd(),"raw_sum_duratioin_first_5_fX100_M.xlsx")
last_5_path = os.path.join(os.getcwd(),"raw_sum_duratioin_last_5_fX100_M.xlsx")
count_first_5_path = os.path.join(os.getcwd(),"raw_count_first_5_fX100_M.xlsx")
count_last_5_path = os.path.join(os.getcwd(),"raw_count_last_5_fX100_M.xlsx")

raw_sum_duratioin_first_5_df.fillna(0).to_excel(first_5_path)
raw_sum_duratioin_last_5_df.fillna(0).to_excel(last_5_path)
raw_count_first_5_df.fillna(0).to_excel(count_first_5_path)
raw_count_last_5_df.fillna(0).to_excel(count_last_5_path)

print("Results saved to:", results_path)
print("First 5 minutes raw sum duration results saved to:", first_5_path)
print("Last 5 minutes raw sum duration results saved to:", last_5_path)
print("First 5 minutes raw count results saved to:", count_first_5_path)
print("Last 5 minutes raw count results saved to:", count_last_5_path)

