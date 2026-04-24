# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 10:22:28 2026

@author: 20233208
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from imutils import paths
import numpy as np



def load_spectrum(row, channel, delta_f):
    y = np.load(row['Path'])[channel, :]
    x = np.linspace(delta_f, delta_f*len(y), len(y))
    return x, y


st.set_page_config(layout="wide")



# Load data
st.markdown("""
<style>
.block-container {
    padding-top: 1rem;
}
</style>
""", unsafe_allow_html=True)

st.title("Spectra Viewer")

#@st.cache_data(show_spinner="Loading metadata...")

if "data_loaded" not in st.session_state:
    st.session_state["data_loaded"] = False

c1, c2, c3 = st.columns([1, 1, 1], vertical_alignment='bottom')

with c1:
    metadata_dir = st.text_input(
        'Metadata directory',
        value=r"C:/PhD project/Research data/Aeroacoustic/metadata.csv",
        placeholder='Enter the directory of the metadata file'
        )
    
with c2:
    load_data_action = st.button('Load data')
    


delta_f = 10
channels = np.linspace(0, 63, 64).astype(np.int32)

if load_data_action:
    if metadata_dir.strip() == '':
        st.warning("Please enter the data directories.")
        st.stop()
    else:
        st.session_state["metadata_path"] = metadata_dir
        st.session_state["data_loaded"] = True
    

#==========================After data loading======================================




if st.session_state['data_loaded'] == True:  
# Sidebar filters
    metadata = pd.read_csv(st.session_state["metadata_path"])
    filtered = metadata.copy()
    attributes = ['Crack', 'Wind speed', 'Angle of attack', 'Turbulence intensity']
    cols = ['Crack', 'Wind_velocity', 'Angle_of_attack', 'Turbulence_intensity']
    
    st.sidebar.title("Attributes filter")
    for i in range(len(attributes)):
        col = cols[i]
        attribute = attributes[i]
        
        options = sorted(metadata[col].dropna().unique())
        chosen = st.sidebar.multiselect(attribute, options, default=[])
        filtered = filtered[filtered[col].isin(chosen)]
    
    
    st.subheader('Data selection')
    top_left, top_right = st.columns([3, 3], gap="medium")
    
    
    with top_left:    
        st.write("Matched data:", len(filtered))
        event = st.dataframe(filtered[['File_name', 'Crack', 'Wind_velocity', 'Angle_of_attack', 'Turbulence_intensity']],
                     hide_index=True,
                     on_select="rerun",
                     selection_mode="multi-row",
                     width='stretch'
                     )
        
        selected_rows = event.selection["rows"]
        
    with top_right:
        st.write("Selected data:", len(selected_rows))
        
        selected_df = filtered.iloc[selected_rows].copy()
        st.dataframe(selected_df[['File_name', 'Crack']], hide_index=True)
    
    
    
    
    st.divider()
    
    st.subheader("Let's plot")
    
    if not selected_df.empty:

        default_colors = [
            "#1f77b4", "#d62728", "#2ca02c", "#9467bd", "#ff7f0e",
            "#17becf", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22"
        ]
    
        plot_settings = {}
        for i, row in selected_df.reset_index(drop=True).iterrows():
            fname = row["File_name"]
    
            plot_settings[fname] = {
                "color": default_colors[i % len(default_colors)],
                "label": fname
            }
        

        
        
        
        def reset_xrange():
            st.session_state["freq_x_min"] = x[0]
            st.session_state["freq_x_max"] = x[-1]
    
        
        
        c1, c2, c3, c4, c5, c6 = st.columns([1, 1, 1, 1, 1, 1], vertical_alignment="bottom")
        
        with c1:
            channel = st.selectbox('Channel to plot', channels)
        
        x, _ = load_spectrum(selected_df.iloc[0], channel, delta_f)
        
        with c2:
            x_min = st.number_input(
                label='Frequency min.',
                value=x[0],
                key='freq_x_min'
            )
        
        with c3:
            x_max = st.number_input(
                label='Frequency max.',
                value=x[-1],
                key='freq_x_max'
            )
        
        with c4:
            st.button("Reset", on_click=reset_xrange)
            
        with c5:
            plot_difference = st.checkbox("Plot difference", value=False)
            
        with c6:
            baseline = st.selectbox(
                "Baseline",
                options=selected_df["File_name"].tolist(),
                index=None,
                placeholder="Select a baseline spectrum",
                disabled=not plot_difference
            )
            
        
        plot_box = st.container()
        with plot_box:
            fig = go.Figure()
            
            if plot_difference and baseline is not None:
                
                baseline_x, baseline_y = load_spectrum(selected_df.loc[selected_df['File_name'] == baseline].iloc[0], channel, delta_f)
                
                for _, row in selected_df.iterrows():
                    x, y = load_spectrum(row, channel, delta_f)
                
                    fig.add_trace(
                        go.Scatter(
                            x=x,
                            y=y-baseline_y,
                            mode="lines",
                            name=plot_settings[row["File_name"]]["label"],
                            line=dict(color=plot_settings[row["File_name"]]["color"], width=2)
                        )
                    )
    
                fig.update_layout(
                    width = 1500,
                    height = 600,
                    font=dict(family="Arial", size=25, color="black"),
                    xaxis_title="Frequency [Hz]",
                    yaxis_title="Power spectral density",
                    template="plotly_dark"
                    )
                
                fig.update_xaxes(
                    type="log",
                    range=[np.log10(x_min), np.log10(x_max)],
                    tickmode="array",
                    tickvals=[100, 200, 500, 1000, 2000, 5000, 10000],
                    ticktext=["100", "200", "500", "1k", "2k", "5k", "10k"],
                    ticks="outside",
                    showgrid=True,
                    griddash="dot",
                    ticklen=6
                )
                 
                fig.update_yaxes(
                    ticks="outside",
                    showgrid=True,
                    griddash="dot",
                    ticklen=6
                )
                
                st.plotly_chart(fig, width='stretch')
            
            else: # Plot_difference is True
                for _, row in selected_df.iterrows():
                    x, y = load_spectrum(row, channel, delta_f)
                
                    fig.add_trace(
                        go.Scatter(
                            x=x,
                            y=y,
                            mode="lines",
                            name=plot_settings[row["File_name"]]["label"],
                            line=dict(color=plot_settings[row["File_name"]]["color"], width=2)
                        )
                    )
    
                fig.update_layout(
                    width = 1500,
                    height = 600,
                    font=dict(family="Arial", size=25, color="black"),
                    xaxis_title="Frequency [Hz]",
                    yaxis_title="Power spectral density",
                    template="plotly_dark"
                    )
                
                fig.update_xaxes(
                    type="log",
                    range=[np.log10(x_min), np.log10(x_max)],
                    tickmode="array",
                    tickvals=[100, 200, 500, 1000, 2000, 5000, 10000],
                    ticktext=["100", "200", "500", "1k", "2k", "5k", "10k"],
                    ticks="outside",
                    showgrid=True,
                    griddash="dot",
                    ticklen=6
                )
                
                fig.update_yaxes(
                    ticks="outside",
                    showgrid=True,
                    griddash="dot",
                    ticklen=6
                )
    
                st.plotly_chart(fig, width='stretch')