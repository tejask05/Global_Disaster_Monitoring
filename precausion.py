import streamlit as st

def main():
    st.header("Safety Protocols for Disaster Prevention")

    col1, col2, col3= st.columns(3)

    with col1:
        st.subheader("Avalanche")
        st.markdown("""
        1. Avoid areas prone to avalanches during times of high risk.
        2. Carry avalanche safety gear such as transceivers, probes, and shovels.
        3. Travel in groups and keep an eye on each other.
        4. Be aware of warning signs like recent snowfall, wind-loading, and terrain features.
        """)
        st.subheader("Heatwave")
        st.markdown("""
        1. Stay hydrated and avoid prolonged exposure to the sun.
        2. Use fans or air conditioning to stay cool.
        3. Check on vulnerable individuals like the elderly and young children.
        4. Dress in lightweight, light-colored clothing.
        """)
        
        st.subheader("Flood")
        st.markdown("""
        1. Evacuate to higher ground if necessary.
        2. Avoid walking or driving through floodwaters.
        3. Turn off utilities if instructed to do so.
        4. Have an emergency flood kit ready with essential items.
        """)
        st.subheader("Hurricane")
        st.markdown("""
        1. Follow evacuation orders from local authorities.
        2. Board up windows and secure outdoor items.
        3. Stay indoors during the storm.
        4. Have a communication plan in place with family and friends.
        """)

    with col2:
        st.subheader("Landslide")
        st.markdown("""
        1. Avoid areas susceptible to landslides during heavy rainfall.
        2. Monitor for signs of land movement like cracks or unusual noises.
        3. Evacuate if instructed by authorities.
        4. Have an emergency plan and supplies ready.
        """)
        st.subheader("Blizzard")
        st.markdown("""
        1. Stay indoors and avoid unnecessary travel.
        2. Keep emergency supplies stocked, including food, water, and blankets.
        3. Dress warmly in layers if you must go outside.
        4. Watch for signs of frostbite and hypothermia.          
        """)
        st.subheader("Cyclone")
        st.markdown("""
        1. Evacuate if advised by local authorities.
        2. Secure loose objects and reinforce windows and doors.
        3. Stay indoors during the storm.
        4. Listen to weather updates from reliable sources.
        """)
        st.subheader("Tsunami")
        st.markdown("""
        1. Evacuate immediately if you are in a tsunami evacuation zone.
        2. Move inland or to higher ground.
        3. Stay away from the coast and low-lying areas.
        4. Listen to emergency alerts and follow instructions.
        """)

        
    with col3:
        st.subheader("Volcano")
        st.markdown("""
        1. Follow evacuation orders from authorities if in an affected area.
        2. Protect yourself from ashfall by staying indoors with windows and doors closed.
        3. Wear masks to protect against volcanic ash inhalation.
        4. Monitor volcanic activity updates from official sources.
        """)
        st.subheader("Earthquake")
        st.markdown("""
        1. Drop, cover, and hold on during shaking.
        2. Move away from windows and heavy objects.
        3. Have an emergency kit with supplies like water, food, and first aid.
        4. Identify safe spots in each room of your home.
        """)
        st.subheader("Drought")
        st.markdown("""
        1. Conserve water by fixing leaks and reducing usage.
        2. Avoid outdoor burning and adhere to water restrictions.
        3. Plant drought-resistant crops and trees.
        4. Monitor water sources and report any issues promptly.
        """)
        st.subheader("Tornado")
        st.markdown("""
        1. Seek shelter in a sturdy building or underground.
        2. Stay away from windows and doors.
        3. If outdoors, find a low-lying area and lie flat, covering your head.
        4. Have a tornado emergency plan for your household.
        """)

if __name__ == "__main__":
    main()
