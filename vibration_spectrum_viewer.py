# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 10:25:24 2026

@author: 20233208
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from imutils import paths
import numpy as np



def load_spectrum(row, channel, delta_f):
    y = np.load(row['path'])[channel, :]
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
    data_dir = st.text_input(
        'Data directory',
        value=r"C:/PhD project/Research data/Drive train vibration/STFT_data_all_round2_05Hz/",
        placeholder='Enter the directory of the data files'
        )
    
with c2:
    metadata_dir = st.text_input(
        'Metadata directory',
        value=r"C:/PhD project/Research data/Drive train vibration/meta_data_accelerometer.csv",
        placeholder='Enter the directory of the metadata file'
        )
    
with c3:
    load_data_action = st.button('Load data')
    

    
#metadata ("C:/PhD project/Research data/Drive train vibration/meta_data_accelerometer.csv")
#spectra_folder 'C:/PhD project/Research data/Drive train vibration/STFT_data_all_round2_05Hz/'


delta_f = 0.5
sensor_locs = ['Gear box', 'Main bearing', 'Tower top']
directions = ['Forward-back', 'Vertical', 'Side-side']
channel_dict = {
    ('Gear box', 'Side-side') : 0,
    ('Gear box', 'Forward-back') : 1,
    ('Gear box', 'Vertical') : 2,
    ('Main bearing', 'Side-side') : 3,
    ('Main bearing', 'Forward-back') : 4,
    ('Main bearing', 'Vertical') : 5,
    ('Tower top', 'Forward-back') : 6,
    ('Tower top', 'Vertical') : 7,
    ('Tower top', 'Side-side') : 8
    }

if load_data_action:
    if data_dir.strip() == '' or metadata_dir.strip() == '':
        st.warning("Please enter the data directories.")
        st.stop()
    else:
        st.session_state["metadata_path"] = metadata_dir
        st.session_state["npy_folder"] = data_dir
        st.session_state["data_loaded"] = True

if st.session_state["data_loaded"]:
       
    metadata = pd.read_csv(st.session_state["metadata_path"])
    spectra_folder = st.session_state["npy_folder"]
    

    spectra_paths = list(paths.list_files(spectra_folder))
    paths_series = pd.Series(spectra_paths)
    names_series = pd.Series([spectra_paths[i][-27:-4] for i in range(len(spectra_paths))])
    file_df = pd.DataFrame(
        {'File_name' : names_series,
        'path' : paths_series}
        )
    metadata = metadata.merge(file_df, 'left', on='File_name')
    
    st.session_state['metadata'] = metadata
    
                

#==========================After data loading======================================




if st.session_state['data_loaded'] == True:  
# Sidebar filters
    metadata = st.session_state['metadata']
    filtered = metadata.copy()
    attributes = ['Damage', 'Wind speed', 'RPM']
    cols = ['Blade 1', 'Set_wind_speed', 'RPM']
    
    st.sidebar.title("Attributes filter")
    for i in range(len(attributes)):
        col = cols[i]
        attribute = attributes[i]
        if col == 'Work_as_turbine':
            options = sorted(metadata[col].dropna().unique())
            chosen = st.sidebar.multiselect(attribute, options, default=options)
            filtered = filtered[filtered[col].isin(chosen)]
        else:
            options = sorted(metadata[col].dropna().unique())
            chosen = st.sidebar.multiselect(attribute, options, default=[])
            filtered = filtered[filtered[col].isin(chosen)]
    
    
    st.subheader('Data selection')
    top_left, top_right = st.columns([3, 3], gap="medium")
    
    
    with top_left:    
        st.write("Matched data:", len(filtered))
        event = st.dataframe(filtered[['File_name', 'Date', 'first day']],
                     hide_index=True,
                     on_select="rerun",
                     selection_mode="multi-row",
                     width='stretch'
                     )
        
        selected_rows = event.selection["rows"]
        
    with top_right:
        st.write("Selected data:", len(selected_rows))
        
        selected_df = filtered.iloc[selected_rows].copy()
        st.dataframe(selected_df[['File_name', 'Date']], hide_index=True)
        
    
        #selected_df = pd.DataFrame()
    
    
    
    
    st.divider()
    
    st.subheader("Let's plot")
    
    
    c1, c2, c3, c4 = st.columns([1, 1, 1, 1])
    
    with c1:
        sensor_loc = st.selectbox('Sensor location', sensor_locs)
    
    with c2:
        direction = st.selectbox('Vibration directin', directions)
    
    channel = channel_dict[(sensor_loc, direction)]
    
    
    

    default_colors = [
        "#1f77b4", "#d62728", "#2ca02c", "#9467bd", "#ff7f0e",
        "#17becf", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22"
    ]

    plot_settings = {}
    
    if selected_df.empty:
        c1, c2, c3 = st.columns([3, 1, 3])
        
        with c1:
            name = st.text_input(
                "File name",
                value=None,
                disabled=True
            )

        with c2:
            color = st.color_picker(
                "Color",
                value=None
            )

        with c3:
            label = st.text_input(
                "Label",
                value=None
            )

    else:    
        
        for i, row in selected_df.reset_index(drop=True).iterrows():
            fname = row["File_name"]
    
            c1, c2, c3 = st.columns([3, 1, 3])
            
            with c1:
                name = st.text_input(
                    "File name",
                    value=fname,
                    disabled=True
                )
    
            with c2:
                color = st.color_picker(
                    "Color",
                    value=default_colors[i % len(default_colors)],
                    key=f"color_{fname}_{i}"
                )
    
            with c3:
                label = st.text_input(
                    "Label",
                    value=fname,
                    key=f"label_{fname}_{i}"
                )
    
            plot_settings[fname] = {
                "color": color,
                "label": label
            }
    
            
#====================================plots=====================================            
    
    st.divider()
    
    st.subheader("Plots")
    
    
    if not selected_df.empty:
        
        x, _ = load_spectrum(selected_df.iloc[0], channel, delta_f)
        
        def reset_xrange():
            st.session_state["freq_x_min"] = x[0]
            st.session_state["freq_x_max"] = x[-1]
    
        
        
        c1, c2, c3, c4, c5 = st.columns([1, 1, 1, 1, 1], vertical_alignment="bottom")
        
        with c1:
            x_min = st.number_input(
                label='Frequency min.',
                value=x[0],
                key='freq_x_min'
            )
        
        with c2:
            x_max = st.number_input(
                label='Frequency max.',
                value=x[-1],
                key='freq_x_max'
            )
        
        with c3:
            st.button("Reset", on_click=reset_xrange)
            
        with c4:
            plot_difference = st.checkbox("Plot difference", value=False)
            
        with c5:
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
                            y=np.log10(y)-np.log10(baseline_y),
                            mode="lines",
                            name=plot_settings[row["File_name"]]["label"],
                            line=dict(color=plot_settings[row["File_name"]]["color"], width=1)
                        )
                    )
    
                fig.update_layout(
                    width = 2000,
                    height = 400,
                    font=dict(family="Arial", size=25, color="black"),
                    xaxis_title="Frequency [Hz]",
                    yaxis_title="Power spectral density",
                    template="plotly_dark"
                    )
                
                fig.update_xaxes(
                    type="log",
                    range=[np.log10(x_min), np.log10(x_max)],
                    tickmode="array",
                    tickvals=[1, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000],
                    ticktext=['1', '5', "10", "20", "50", "100", "200", "500", "1k", "2k", "5k", "10k"],
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
                            line=dict(color=plot_settings[row["File_name"]]["color"], width=1)
                        )
                    )
    
                fig.update_layout(
                    width = 2000,
                    height = 400,
                    font=dict(family="Arial", size=25, color="black"),
                    xaxis_title="Frequency [Hz]",
                    yaxis_title="Power spectral density",
                    template="plotly_dark"
                    )
                
                fig.update_xaxes(
                    type="log",
                    range=[np.log10(x_min), np.log10(x_max)],
                    tickmode="array",
                    tickvals=[1, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000],
                    ticktext=['1', '5', "10", "20", "50", "100", "200", "500", "1k", "2k", "5k", "10k"],
                    ticks="outside",
                    showgrid=True,
                    griddash="dot",
                    ticklen=6
                )
                
                fig.update_yaxes(
                    type="log",
                    tickmode="array",
                    tickvals=[1e-4, 1e-3, 1e-2, 1e-1, 1],
                    ticktext=["1e-4", "1e-3", "1e-2", "1e-1", "1"],
                    ticks="outside",
                    showgrid=True,
                    griddash="dot",
                    ticklen=6
                )
    
                st.plotly_chart(fig, width='stretch')









