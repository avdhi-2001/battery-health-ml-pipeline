import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import numpy as np
from sqlalchemy import create_engine

st.set_page_config(
    page_title="Battery Health Monitor",
    page_icon="🔋",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.main {
    background-color: #0f1117;
}

[data-testid="stSidebar"] {
    background-color: #0f1117;
    border-right: 1px solid #1f2937;
}

/* ── Sidebar ── */
.sidebar-logo {
    font-size: 15px;
    font-weight: 600;
    color: #f9fafb;
    letter-spacing: 0.5px;
    margin-bottom: 4px;
}

.sidebar-tagline {
    font-size: 11px;
    color: #6b7280;
    letter-spacing: 0.5px;
    margin-bottom: 24px;
}

.sidebar-section {
    font-size: 10px;
    font-weight: 600;
    color: #6b7280;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin: 20px 0px 10px 0px;
}

.sidebar-item {
    font-size: 13px;
    color: #9ca3af;
    margin: 6px 0px;
    display: flex;
    justify-content: space-between;
}

.sidebar-value {
    color: #f9fafb;
    font-weight: 500;
}

.sidebar-value-green {
    color: #34d399;
    font-weight: 500;
}

.sidebar-value-red {
    color: #f87171;
    font-weight: 500;
}

.status-indicator {
    display: inline-block;
    width: 6px;
    height: 6px;
    background: #34d399;
    border-radius: 50%;
    margin-right: 8px;
}

/* ── Page Header ── */
.page-header {
    margin-bottom: 32px;
}

.page-title {
    font-size: 24px;
    font-weight: 600;
    color: #f9fafb;
    margin-bottom: 4px;
}

.page-subtitle {
    font-size: 13px;
    color: #6b7280;
}

/* ── Metric Cards ── */
.metric-card {
    background-color: #161b27;
    border: 1px solid #1f2937;
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 16px;
}

.metric-label {
    font-size: 12px;
    color: #6b7280;
    font-weight: 500;
    letter-spacing: 0.3px;
    margin-bottom: 8px;
}

.metric-value {
    font-size: 32px;
    font-weight: 600;
    color: #f9fafb;
    line-height: 1;
}

.metric-value-green {
    font-size: 32px;
    font-weight: 600;
    color: #34d399;
    line-height: 1;
}

.metric-value-red {
    font-size: 32px;
    font-weight: 600;
    color: #f87171;
    line-height: 1;
}

.metric-sub {
    font-size: 12px;
    color: #6b7280;
    margin-top: 6px;
}

/* ── Section Headers ── */
.section-title {
    font-size: 15px;
    font-weight: 600;
    color: #f9fafb;
    margin: 32px 0px 16px 0px;
}

.section-divider {
    border: none;
    border-top: 1px solid #1f2937;
    margin: 24px 0px;
}

/* ── Alert Card ── */
.alert-card {
    background-color: #1a0f0f;
    border: 1px solid #7f1d1d;
    border-radius: 12px;
    padding: 20px 24px;
}

.alert-title {
    font-size: 12px;
    color: #ef4444;
    font-weight: 600;
    letter-spacing: 0.5px;
    margin-bottom: 8px;
}

.alert-value {
    font-size: 42px;
    font-weight: 600;
    color: #f87171;
    line-height: 1;
    margin-bottom: 16px;
}

.alert-detail {
    font-size: 12px;
    color: #6b7280;
    margin-bottom: 4px;
}

.alert-detail-value {
    font-size: 13px;
    color: #f87171;
    font-weight: 500;
}

/* ── Predict Section ── */
.predict-card {
    background-color: #161b27;
    border: 1px solid #1f2937;
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 12px;
}

.predict-label {
    font-size: 11px;
    color: #6b7280;
    font-weight: 500;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 8px;
}

.predict-value {
    font-size: 48px;
    font-weight: 600;
    color: #34d399;
    line-height: 1;
}

.predict-value-red {
    font-size: 48px;
    font-weight: 600;
    color: #f87171;
    line-height: 1;
}

.predict-sub {
    font-size: 12px;
    color: #6b7280;
    margin-top: 6px;
}

.decision-card-green {
    background-color: #052e16;
    border: 1px solid #166534;
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 12px;
}

.decision-card-red {
    background-color: #1a0f0f;
    border: 1px solid #7f1d1d;
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 12px;
}

.decision-label {
    font-size: 11px;
    color: #6b7280;
    font-weight: 500;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 8px;
}

.decision-value-green {
    font-size: 22px;
    font-weight: 600;
    color: #34d399;
    margin-bottom: 6px;
}

.decision-value-red {
    font-size: 22px;
    font-weight: 600;
    color: #f87171;
    margin-bottom: 6px;
}

.decision-sub {
    font-size: 12px;
    color: #6b7280;
}

.empty-state {
    background-color: #161b27;
    border: 1px solid #1f2937;
    border-radius: 12px;
    padding: 60px 24px;
    text-align: center;
    margin-bottom: 12px;
}

.empty-state-text {
    font-size: 13px;
    color: #6b7280;
    margin-top: 12px;
}

div[data-testid="stButton"] button {
    background-color: #2563eb;
    color: #ffffff;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-size: 14px;
    font-weight: 500;
    width: 100%;
    letter-spacing: 0.3px;
    transition: background 0.2s;
}

div[data-testid="stButton"] button:hover {
    background-color: #1d4ed8;
}

/* ── Table Styling ── */
[data-testid="stDataFrame"] {
    border: 1px solid #1f2937;
    border-radius: 12px;
    overflow: hidden;
}
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_models():
    with open('model_soh.pkl', 'rb') as f:
        model_soh = pickle.load(f)
    with open('model_rul.pkl', 'rb') as f:
        model_rul = pickle.load(f)
    with open('model_anomaly.pkl', 'rb') as f:
        model_anomaly = pickle.load(f)
    return model_soh, model_rul, model_anomaly

from sqlalchemy import create_engine

DB_URL = 'postgresql://avdhipagaria@localhost:5432/battery_health_db'

@st.cache_data(ttl=10)
def load_data():
    engine = create_engine(DB_URL)
    
    # Load predictions from PostgreSQL
    df = pd.read_sql(
        'SELECT * FROM battery_predictions', 
        engine
    )
    
    # Load anomalies from PostgreSQL
    anomalies_db = pd.read_sql(
        'SELECT * FROM anomaly_alerts', 
        engine
    )
    
    # Add anomaly label to main df
    df['anomaly_label'] = 'Normal'
    
    for _, row in anomalies_db.iterrows():
        mask = (
            (df['battery_id'] == row['battery_id']) & 
            (df['cycle_number'] == row['cycle_number'])
        )
        df.loc[mask, 'anomaly_label'] = 'Anomaly'
    
    # Rename columns to match dashboard
    df = df.rename(columns={
        'soh': 'SoH',
        'rul': 'RUL'
    })
    
    return df

model_soh, model_rul, model_anomaly = load_models()
df = load_data()

total_batteries = df['battery_id'].nunique()
total_cycles    = len(df)
anomaly_count   = len(df[df['anomaly_label'] == 'Anomaly'])
avg_soh         = df['SoH'].mean()
avg_rul         = df['RUL'].mean()
healthy         = len(df[df['SoH'] >= 70]['battery_id'].unique())
recycle         = total_batteries - healthy

with st.sidebar:

    st.markdown('<p class="sidebar-logo">Bridge Green Upcycle</p>',
                unsafe_allow_html=True)
    st.markdown('<p class="sidebar-tagline">Battery Intelligence Platform</p>',
                unsafe_allow_html=True)

    st.markdown('<hr style="border-color:#1f2937; margin:0px">', unsafe_allow_html=True)

    st.markdown('<p class="sidebar-section">System</p>',
                unsafe_allow_html=True)

    st.markdown(f'<p class="sidebar-item"><span><span class="status-indicator"></span>Pipeline</span><span class="sidebar-value-green">Active</span></p>', unsafe_allow_html=True)
    st.markdown(f'<p class="sidebar-item"><span><span class="status-indicator"></span>ML Models</span><span class="sidebar-value-green">Online</span></p>', unsafe_allow_html=True)
    st.markdown(f'<p class="sidebar-item"><span><span class="status-indicator"></span>Dashboard</span><span class="sidebar-value-green">Live</span></p>', unsafe_allow_html=True)

    st.markdown('<p class="sidebar-section">Fleet</p>',
                unsafe_allow_html=True)

    st.markdown(f'<p class="sidebar-item"><span>Total Batteries</span><span class="sidebar-value">{total_batteries}</span></p>', unsafe_allow_html=True)
    st.markdown(f'<p class="sidebar-item"><span>Total Cycles</span><span class="sidebar-value">{total_cycles}</span></p>', unsafe_allow_html=True)
    st.markdown(f'<p class="sidebar-item"><span>Avg SoH</span><span class="sidebar-value-green">{avg_soh:.1f}%</span></p>', unsafe_allow_html=True)
    st.markdown(f'<p class="sidebar-item"><span>Second Life</span><span class="sidebar-value-green">{healthy}</span></p>', unsafe_allow_html=True)
    st.markdown(f'<p class="sidebar-item"><span>For Recycling</span><span class="sidebar-value-red">{recycle}</span></p>', unsafe_allow_html=True)
    st.markdown(f'<p class="sidebar-item"><span>Anomalies</span><span class="sidebar-value-red">{anomaly_count}</span></p>', unsafe_allow_html=True)

    st.markdown('<p class="sidebar-section">Models</p>',
                unsafe_allow_html=True)

    st.markdown(f'<p class="sidebar-item"><span>SoH Model</span><span class="sidebar-value-green">R² = 0.90</span></p>', unsafe_allow_html=True)
    st.markdown(f'<p class="sidebar-item"><span>RUL Model</span><span class="sidebar-value-green">R² = 0.97</span></p>', unsafe_allow_html=True)
    st.markdown(f'<p class="sidebar-item"><span>Anomaly Model</span><span class="sidebar-value-green">Active</span></p>', unsafe_allow_html=True)

    st.markdown('<br><br>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:11px; color:#374151">NASA Battery Dataset<br>Bridge Green © 2025</p>', unsafe_allow_html=True)

st.markdown("""
<div class="page-header">
    <p class="page-title">Battery Health Monitor</p>
    <p class="page-subtitle">Real-time battery intelligence — SoH prediction, RUL estimation and anomaly detection</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<p class="section-title">Overview</p>',
            unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <p class="metric-label">Total Batteries</p>
        <p class="metric-value">{total_batteries}</p>
        <p class="metric-sub">across all chemistries</p>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <p class="metric-label">Total Cycles</p>
        <p class="metric-value">{total_cycles}</p>
        <p class="metric-sub">discharge cycles recorded</p>
    </div>""", unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <p class="metric-label">Average SoH</p>
        <p class="metric-value-green">{avg_soh:.1f}%</p>
        <p class="metric-sub">fleet health score</p>
    </div>""", unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <p class="metric-label">Second Life Ready</p>
        <p class="metric-value-green">{healthy}</p>
        <p class="metric-sub">batteries above 70% SoH</p>
    </div>""", unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="metric-card">
        <p class="metric-label">Anomalies</p>
        <p class="metric-value-red">{anomaly_count}</p>
        <p class="metric-sub">cycles flagged for review</p>
    </div>""", unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown('<p class="section-title">Battery Aging Analysis</p>',
            unsafe_allow_html=True)

fig, axes = plt.subplots(1, 2, figsize=(16, 4))
fig.patch.set_facecolor('#0f1117')

blues   = plt.cm.Blues(np.linspace(0.4, 0.9, total_batteries))
greens  = plt.cm.Greens(np.linspace(0.4, 0.9, total_batteries))

axes[0].set_facecolor('#161b27')
for i, battery in enumerate(df['battery_id'].unique()):
    bdata = df[df['battery_id'] == battery]
    axes[0].plot(bdata['cycle_number'],
                bdata['SoH'],
                alpha=0.6,
                linewidth=1.2,
                color=blues[i])

axes[0].axhline(y=70,
                color='#ef4444',
                linestyle='--',
                linewidth=1.5,
                label='Recycle threshold (70%)')
axes[0].fill_between([0, 210], 0, 70,
                     alpha=0.05,
                     color='#ef4444')
axes[0].set_xlabel('Cycle Number',
                   color='#6b7280',
                   fontsize=10)
axes[0].set_ylabel('State of Health (%)',
                   color='#6b7280',
                   fontsize=10)
axes[0].set_title('State of Health over Cycles',
                  color='#f9fafb',
                  fontsize=13,
                  fontweight='600',
                  pad=12)
axes[0].tick_params(colors='#6b7280', labelsize=9)
axes[0].legend(facecolor='#161b27',
               labelcolor='#9ca3af',
               edgecolor='#1f2937',
               fontsize=9)
for spine in axes[0].spines.values():
    spine.set_color('#1f2937')

axes[1].set_facecolor('#161b27')
for i, battery in enumerate(df['battery_id'].unique()):
    bdata = df[df['battery_id'] == battery]
    axes[1].plot(bdata['cycle_number'],
                bdata['RUL'],
                alpha=0.6,
                linewidth=1.2,
                color=greens[i])

axes[1].set_xlabel('Cycle Number',
                   color='#6b7280',
                   fontsize=10)
axes[1].set_ylabel('Remaining Useful Life (cycles)',
                   color='#6b7280',
                   fontsize=10)
axes[1].set_title('Remaining Useful Life over Cycles',
                  color='#f9fafb',
                  fontsize=13,
                  fontweight='600',
                  pad=12)
axes[1].tick_params(colors='#6b7280', labelsize=9)
for spine in axes[1].spines.values():
    spine.set_color('#1f2937')

plt.tight_layout(pad=2.5)
st.pyplot(fig)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown('<p class="section-title">Anomaly Alerts</p>',
            unsafe_allow_html=True)

anomalies = df[df['anomaly_label'] == 'Anomaly'][[
    'battery_id', 'cycle_number',
    'avg_voltage', 'avg_temperature',
    'avg_current', 'SoH',
    'anomaly_label'
]].round(2)

col1, col2 = st.columns([3, 1])

with col1:
    st.dataframe(
        anomalies,
        use_container_width=True,
        height=280,
        hide_index=True
    )

with col2:
    st.markdown(f"""
    <div class="alert-card">
        <p class="alert-title">ANOMALIES DETECTED</p>
        <p class="alert-value">{anomaly_count}</p>
        <p class="alert-detail">Batteries affected</p>
        <p class="alert-detail-value">B0029, B0030</p>
        <br>
        <p class="alert-detail">Primary cause</p>
        <p class="alert-detail-value">
            High temperature
            <br>51°C — 54°C
            <br>(normal: ~32°C)
        </p>
        <br>
        <p class="alert-detail">Recommendation</p>
        <p class="alert-detail-value">
            Inspect B0029, B0030
            <br>Check cooling system
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown('<p class="section-title">Live Battery Health Prediction</p>',
            unsafe_allow_html=True)
st.markdown('<p style="font-size:13px; color:#6b7280; margin-bottom:20px">Simulate live BMS telemetry — adjust readings to get instant AI predictions</p>',
            unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<p style="font-size:12px; color:#6b7280; font-weight:500; letter-spacing:0.5px; margin-bottom:16px">BATTERY READINGS</p>',
                unsafe_allow_html=True)

    cycle_number = st.slider(
        "Cycle Number",
        min_value=1,
        max_value=200,
        value=50
    )
    avg_voltage = st.slider(
        "Average Voltage (V)",
        min_value=0.0,
        max_value=5.0,
        value=3.5,
        step=0.01
    )
    avg_temperature = st.slider(
        "Average Temperature (°C)",
        min_value=0.0,
        max_value=60.0,
        value=32.0,
        step=0.1
    )
    avg_current = st.slider(
        "Average Current (A)",
        min_value=-5.0,
        max_value=0.0,
        value=-1.8,
        step=0.01
    )

    st.markdown("<br>", unsafe_allow_html=True)
    predict_btn = st.button(
        "Run Prediction",
        use_container_width=True
    )

with col2:
    st.markdown('<p style="font-size:12px; color:#6b7280; font-weight:500; letter-spacing:0.5px; margin-bottom:16px">PREDICTION RESULTS</p>',
                unsafe_allow_html=True)

    if predict_btn:
        input_data = pd.DataFrame([[
            cycle_number, avg_voltage,
            avg_temperature, avg_current
        ]], columns=['cycle_number', 'avg_voltage',
                     'avg_temperature', 'avg_current'])

        soh_pred = model_soh.predict(input_data)[0]

        input_rul = pd.DataFrame([[
            cycle_number, avg_voltage,
            avg_temperature, avg_current, soh_pred
        ]], columns=['cycle_number', 'avg_voltage',
                     'avg_temperature', 'avg_current',
                     'SoH'])

        rul_pred = model_rul.predict(input_rul)[0]

        soh_class = "predict-value" if soh_pred >= 70 else "predict-value-red"
        st.markdown(f"""
        <div class="predict-card">
            <p class="predict-label">State of Health</p>
            <p class="{soh_class}">{soh_pred:.1f}%</p>
            <p class="predict-sub">predicted from live sensor readings</p>
        </div>""", unsafe_allow_html=True)

        
        st.markdown(f"""
        <div class="predict-card">
            <p class="predict-label">Remaining Useful Life</p>
            <p class="predict-value">{rul_pred:.0f} <span style="font-size:18px; color:#6b7280; font-weight:400">cycles</span></p>
            <p class="predict-sub">estimated cycles before end of life</p>
        </div>""", unsafe_allow_html=True)

        if soh_pred >= 70:
            st.markdown(f"""
            <div class="decision-card-green">
                <p class="decision-label">Bridge Green Decision</p>
                <p class="decision-value-green">Second Life</p>
                <p class="decision-sub">
                    Battery qualifies for BESS deployment.
                    Estimated {rul_pred:.0f} cycles remaining.
                </p>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="decision-card-red">
                <p class="decision-label">Bridge Green Decision</p>
                <p class="decision-value-red">Recycle</p>
                <p class="decision-sub">
                    Battery below 70% threshold.
                    Extract lithium, cobalt and nickel.
                </p>
            </div>""", unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="empty-state">
            <p style="font-size:32px">→</p>
            <p class="empty-state-text">
                Adjust the sliders and click
                <br>
                <b style="color:#f9fafb">Run Prediction</b>
                <br>
                to see results
            </p>
        </div>""", unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<p style="font-size:11px; color:#374151">Bridge Green Upcycle</p>',
                unsafe_allow_html=True)
with col2:
    st.markdown('<p style="font-size:11px; color:#374151; text-align:center">Built on NASA Battery Dataset</p>',
                unsafe_allow_html=True)
with col3:
    st.markdown('<p style="font-size:11px; color:#374151; text-align:right">Battery Digital Technology Stack</p>',
                unsafe_allow_html=True)