import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set Page Properties
PAGE_CONFIG = {"page_title": "CarbonMeter: Data Center Carbon Footprint Calculator",
               "layout": "wide"}

st.set_page_config(**PAGE_CONFIG)

# Dashboard title
st.title('Data Center Carbon Footprint Calculator')
st.subheader('Part of L2D Project')

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["Embodied", "Operational", "Recycling", "Data Center Analyzer"])

# GLOBALS
server_per_rack = 52
server_manu_footprint = 4000

# Embodied Footprint Tab
with tab1:
   st.title("Embodied Carbon Footprint")

   col1, col2, col3 = st.columns(3)

   with col1:
       st.subheader('Server Manufacturing Footprint')
       server_model = st.selectbox(
           'Choose server model?',
           ('Dell R710', 'Dell R740', 'HPE ProLiant DL380'))

       if server_model == "Dell R740":
           server_manu_footprint = 4200
       elif server_model == "Dell R710":
           server_manu_footprint = 400
       elif server_model == "HPE ProLiant DL380":
           server_manu_footprint = 2000
       else:
           server_manu_footprint = 400

       power_capacity = st.number_input('Power Capacity (kW)', value=4000, help="Data center power capacity")
       pue = st.number_input('PUE', min_value=1.0, step=0.05, value=1.2, help="Power Usage Effectiveness. Usually a value between 1.1 to 1.5")
       utilization = st.slider('Average System Utilization', 0.2, 1.0, 0.5, help="Average server utilization is usually a value between 40% to 80%")
       per_rack_power = st.slider('Per-rack Power (kW)', 10, 25, 15, help="Typical range is 10 to 25 kW")
       it_power_consumption = power_capacity * utilization / pue
       number_of_racks = it_power_consumption/per_rack_power
       number_of_servers = number_of_racks * server_per_rack
       manufacturing_footprint = number_of_servers * server_manu_footprint
       st.write('Server Power Consumption (kW):', round(it_power_consumption,2))
       st.markdown('<p class="big-font"><b>Server Manufacturing Footprint (kg CO2-eq):</b> {}</p>'.format(round(manufacturing_footprint,2)), unsafe_allow_html=True)

   with col2:
       st.subheader('Network Equipment Footprint')
       server_count = st.number_input("Number of Servers", value=number_of_servers)
       port_count = st.number_input("Port-per-Switch", value=4)
       topology = st.selectbox(
           'Network Topology',
           ('Fat Tree', 'CLOS', 'Three-Tier', 'Spine Leaf'))

       core_switches = (port_count/2) ** 2
       pods = port_count
       server_count_per_switch = (port_count ** 3) / 4
       number_of_switches = server_count/server_count_per_switch
       st.write('Number of Switches Required: ', round(number_of_switches, 2))
       manufacturing_footprint_network = 80.7 * number_of_switches
       st.write('Network manufacturing footprint (kgCO2-eq): ', round(manufacturing_footprint_network, 2))
       # server_count**(1./3.)

   with col3:
       st.subheader('Data Center Construction Footprint')
       dc_area = st.number_input('Data Center Area (sqf)', value=5000, help="Data center white space")

       # Material footprints
       base_area = 5700.0
       foundation = (4.7 / base_area) * dc_area
       flooring = (39.9 / base_area) * dc_area
       ceilings = (2.3 / base_area) * dc_area
       structure = (15.4 / base_area) * dc_area
       external_walls = (32.1 / base_area) * dc_area
       internal_walls = (8.7 / base_area) * dc_area
       stairs = (1.1 / base_area) * dc_area
       windows = (0.59 / base_area) * dc_area
       roof = (23.4 / base_area) * dc_area

       construction_footprint = foundation + flooring + ceilings + structure + external_walls + internal_walls + stairs + windows + roof
       worst_case_footprint = (dc_area * 0.092) * 71
       st.markdown('<p class="big-font"><b>Building Construction Footprint (kg CO2-eq):</b> {}</p>'.format(worst_case_footprint), unsafe_allow_html=True)

       labels = 'Foundation', "Flooring", "Ceilings", "Structure", "External Walls", "Internal Walls", "Stairs", "Windows", "Roof"
       sizes = [foundation/construction_footprint, flooring/construction_footprint, ceilings/construction_footprint, structure/construction_footprint, external_walls/construction_footprint, internal_walls/construction_footprint, stairs/construction_footprint, windows/construction_footprint, roof/construction_footprint]
       fig1, ax1 = plt.subplots()
       ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
               shadow=True, startangle=90)
       ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
       st.pyplot(fig1)


with tab2:
   st.title("IT Operational Footprint")
   col1, col2, col3 = st.columns(3)
   with col1:
       energy_source_carbon_intensity = st.number_input('Energy Source Carbon Intensity (kg CO2-eq/kWh)', value=0.026, help="Carbon intensity of the energy source based on electricitymaps.com data")
       daily_energy_usage = it_power_consumption * 24
       daily_carbon_footprint = energy_source_carbon_intensity * daily_energy_usage * 24
       lifetime = st.slider('IT Equipment Lifetime (years)', 2, 10, 5, help="Typical value is 5 years")
       wue = st.slider('Water Usage Effectiveness (WUE)', 0.1, 2.0, 0.2, help="Typical value is 0.2 (reported by Google)")
       lifetime_operational_footprint = lifetime * 365 * daily_carbon_footprint
       water_consumption = wue * lifetime_operational_footprint
       lifetime_water_footprint = water_consumption * 0.376 * 0.001

       st.write('IT Power Consumption (kW):', round(it_power_consumption, 2))
       st.write('Daily Energy Usage (kWh):', round(daily_energy_usage, 2))
       st.write('Daily Carbon Footprint (kgCO2-eq):', round(daily_carbon_footprint, 2))
       st.write('Life-time Water Usage (liters):', round(water_consumption, 2))
       st.write('Life-time Water Usage Footprint (kgCO2-eq)', round(lifetime_water_footprint, 2))
       st.markdown('<p class="big-font"><b>IT Operational Footprint (kg CO2-eq):</b> {}</p>'.format(round(lifetime_operational_footprint + lifetime_water_footprint)), unsafe_allow_html=True)

   with col2:
       st.subheader('Data Center Total Footprint Breakdown')
       labels_total = 'IT Manufacturing', "Construction", "Operational"
       sizes_total = [manufacturing_footprint, worst_case_footprint, lifetime_operational_footprint]
       fig1, ax1 = plt.subplots()
       ax1.pie(sizes_total, labels=labels_total, autopct='%1.1f%%',
               shadow=True, startangle=90)
       ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
       st.pyplot(fig1)

with tab3:
   st.title("Recycling/Waste")
   col1, col2, col3 = st.columns(3)

   with col1:
       st.subheader('Server Recycling')
       aluminium = -5.3
       steel = -21.1
       paper = 5.13
       thermal = 1.71
       power = 0.7
       copper = -8.8
       gold = -169.14
       palladium = -2.62
       pwb = 0.81
       silver = -0.17
       platinum = -0.08
       landfill = 0.06

       net_results = (aluminium + steel + paper + thermal + power + copper + gold + palladium + pwb + silver + platinum + landfill) * number_of_servers
       st.write("Aluminium (kgCO2-eq): ", aluminium)
       st.write("Steel (kgCO2-eq): ", steel)
       st.write("Paper (kgCO2-eq): ", paper)
       st.write("Thermal materials (kgCO2-eq): ", thermal)
       st.write("Power (kgCO2-eq): ", power)
       st.write("Copper (kgCO2-eq): ", copper)
       st.write("Gold (kgCO2-eq): ", gold)
       st.write("Palladium (kgCO2-eq): ", palladium)
       st.write("PWB (kgCO2-eq): ", pwb)
       st.write("Silver (kgCO2-eq): ", silver)
       st.write("Platinum (kgCO2-eq): ", platinum)
       st.write("Landfill (kgCO2-eq): ", landfill)
       st.write('Server Recycling Net Results (kgCO2-eq):', net_results)

   with col2:
       st.subheader('Network Recycling')
       network_recycling = (manufacturing_footprint_network / 61) * -2
       st.write("Network Recycling Net Results (kgCO2-eq): ", network_recycling)

with tab4:
    uploaded_file = st.file_uploader("Choose a file", type = 'xlsx')

    if uploaded_file is not None:
        df1 = pd.read_excel(uploaded_file)
        print(df1)
