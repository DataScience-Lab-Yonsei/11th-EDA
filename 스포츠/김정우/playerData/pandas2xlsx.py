import pandas as pd

# Read hitterRecords.csv
hitter_file_path = './data/hitterRecords.csv'  # Specify the path to the hitterRecords.csv file
hitter_df = pd.read_csv(hitter_file_path, encoding='utf-8')

# Read pitcherRecords.csv
pitcher_file_path = './data/pitcherRecords.csv'  # Specify the path to the pitcherRecords.csv file
pitcher_df = pd.read_csv(pitcher_file_path, encoding='utf-8')

# Read validPlayerId
valid_player_id1 = './data/validPlayerId.csv'  # Specify the path to the validPlayerId1.csv file
valid_player_id1_df = pd.read_csv(valid_player_id1, encoding='utf-8')

# Export each DataFrame to XLSX files
hitter_df.to_excel('./data/hitterRecords.xlsx', index=False, engine='openpyxl')
pitcher_df.to_excel('./data/pitcherRecords.xlsx', index=False, engine='openpyxl')
valid_player_id1_df.to_excel('./data/validPlayerId.xlsx', index=False, engine='openpyxl')

print('Successfully converted the CSV files to XLSX files.')
