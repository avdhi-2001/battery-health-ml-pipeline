import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql://avdhipagaria@localhost:5432/battery_health_db')

print("Connected to PostgreSQL!")
merge_df = pd.read_csv('merged_df.csv')

print(f"Loaded {len(merge_df)} rows from merged_df.csv")

predictions = merge_df[['battery_id', 'cycle_number','avg_voltage', 'avg_temperature',
'avg_current', 'SoH', 'RUL']].copy()

predictions.columns = ['battery_id', 'cycle_number','avg_voltage', 'avg_temperature',
'avg_current', 'soh', 'rul']

predictions.to_sql('battery_predictions',engine,if_exists='replace',index=False)

print(f"Stored {len(predictions)} rows in battery_predictions!")

anomalies = merge_df[
    merge_df['anomaly_label'] == 'Anomaly'
][[
    'battery_id', 'cycle_number',
    'avg_voltage', 'avg_temperature',
    'avg_current', 'SoH', 'anomaly_label'
]].copy()

anomalies.columns = [
    'battery_id', 'cycle_number',
    'avg_voltage', 'avg_temperature',
    'avg_current', 'soh', 'anomaly_label'
]

anomalies.to_sql(
    'anomaly_alerts',
    engine,
    if_exists='replace',
    index=False
)

print(f"Stored {len(anomalies)} anomalies in anomaly_alerts!")

summary = merge_df.groupby('battery_id').agg(
    total_cycles  = ('cycle_number', 'max'),
    max_capacity  = ('avg_voltage', 'max'),
    min_capacity  = ('avg_voltage', 'min'),
    avg_soh       = ('SoH', 'mean'),
    avg_rul       = ('RUL', 'mean')
).reset_index()

summary['status'] = summary['avg_soh'].apply(
    lambda x: 'Healthy' if x >= 70 else 'Recycle'
)

summary.to_sql(
    'battery_summary',
    engine,
    if_exists='replace',
    index=False
)



print(f"Stored {len(summary)} batteries in battery_summary!")
print("\nAll data successfully stored in PostgreSQL!")