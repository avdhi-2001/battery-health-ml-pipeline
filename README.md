# Battery Health ML Pipeline

An end to end machine learning pipeline for predicting battery health, estimating remaining useful life and detecting anomalies in real time. Built on real battery cycle data from NASA's battery research lab.

## Background

Lithium-ion batteries power everything from electric vehicles to grid storage systems. The problem is that batteries degrade over time — every charge and discharge cycle slowly reduces how much charge they can hold. Knowing exactly how healthy a battery is and how much longer it will last is a hard problem, and it is one that matters a lot as the world moves toward clean energy.

This project builds a complete pipeline that answers three questions:

- How healthy is this battery right now?
- How many cycles does it have left before it needs to be replaced?
- Is something unusual happening that someone should know about?

## The Data

I used the NASA Battery Dataset — real battery readings collected in a lab where researchers charged and discharged batteries hundreds of times until they died, recording voltage, current and temperature every second.

- 34 physical batteries
- 7,565 individual test files
- 7.3 million rows of raw sensor data
- 3 test types: charge, discharge and impedance

## How It Works

The first step was loading all 7,565 CSV files and combining them into one big dataframe. Each file is one test cycle of one battery — so one battery might have over a hundred files just for its discharge tests alone.

Once everything was loaded, I connected the raw sensor readings with a metadata file that maps each file to a real battery, tells us what type of test it was, and gives us the measured capacity at that cycle. This merge step was trickier than it sounds because the two tables had different column names for the same thing.

After merging, I filtered down to only the discharge cycles — capacity is only measured when a battery is being fully drained, so charge and impedance rows do not have a capacity value. From the discharge data I calculated State of Health (SoH) and Remaining Useful Life (RUL) for every cycle, and summarised each cycle into one row of average voltage, temperature and current readings.

With the processed data ready, I trained three models. A Random Forest for SoH prediction, another Random Forest for RUL prediction, and an Isolation Forest for anomaly detection. The SoH and RUL models are supervised — they learn from labelled examples. The anomaly model is unsupervised — it figures out what normal looks like on its own and flags anything that does not fit.

Finally everything comes together in a Streamlit dashboard that shows the health of the whole fleet, flags anomalies and lets you enter live battery readings to get instant predictions.

## Results

| Model | Metric | Score |
|---|---|---|
| SoH Prediction | R^2 Score | 0.90 |
| SoH Prediction | Mean Absolute Error | 2.29% |
| RUL Prediction | R^2 Score | 0.97 |
| RUL Prediction | Mean Absolute Error | 2.74 cycles |
| Anomaly Detection | Cycles Flagged | 139 |

The anomaly model flagged 139 unusual cycles — mostly from two batteries running at 51 to 54°C instead of the normal 32°C. That kind of temperature spike would be a clear signal to inspect those batteries before something goes wrong.

## Tech Stack

- Python 3.13
- Pandas and NumPy for data processing
- Scikit-learn for model training
- Matplotlib for visualisation
- Streamlit for the dashboard
- Pickle for saving and loading models

## Project Structure
```
battery-health-ml-pipeline/
├── battery_exploration.ipynb
├── dashboard.py
├── model_soh.pkl
├── model_rul.pkl
├── model_anomaly.pkl
├── merged_df.csv
├── battery_aging.png
└── README.md
```

## How to Run

Clone the repo and set up a virtual environment:
```bash
git clone https://github.com/avdhi-2001/battery-health-ml-pipeline.git
cd battery-health-ml-pipeline
python -m venv venv
source venv/bin/activate
pip install pandas numpy matplotlib scikit-learn streamlit
```

Download the NASA Battery Dataset from Kaggle and place it in a folder called cleaned_dataset/ in the project root:

https://www.kaggle.com/datasets/patrickfleith/nasa-battery-dataset

Open battery_exploration.ipynb and run all cells. This processes the data and trains the models, generating the pkl and csv files the dashboard needs. Then launch the dashboard:
```bash
streamlit run dashboard.py
```

## Challenges

The trickiest part was not the model training — it was getting the data pipeline right. The dataset has 7,565 files with slightly different column structures depending on the test type. Merging everything correctly without losing the battery identity column took a few attempts. Two batteries had near zero voltage readings in some cycles which caused NaN values in the SoH calculation. Investigating those taught me not to clean data blindly without first understanding why the values are missing.

## What is Next

- PostgreSQL integration to store predictions and battery history
- Apache Airflow to automate the full pipeline on a schedule
- Real time data simulation to mimic live BMS telemetry streaming