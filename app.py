"""
ERP-Based Cost & Procurement Analytics Dashboard
Streamlit application for infrastructure project management analytics
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# Set page configuration
st.set_page_config(
    page_title="ERP Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# ============================================================================
# DATA GENERATION FUNCTIONS
# ============================================================================

@st.cache_data
def generate_erp_data(num_rows=250):
    """
    Generate synthetic ERP data for infrastructure projects
    """
    np.random.seed(42)
    random.seed(42)
    
    # Define reference data
    projects = [f"PRJ-{i:03d}" for i in range(1, 16)]
    vendors = [
        "BuildCorp Ltd", "SteelMax Industries", "ConcreteWorks Inc",
        "ElectroPower Solutions", "PipeLine Suppliers", "Machinery Depot",
        "WoodWorks Co", "MetalFab Inc", "Transportation Services",
        "SafetyEquip Ltd", "TechInstall Group", "Foundation Experts"
    ]
    materials = [
        "Concrete Grade M30", "Steel Reinforcement", "Electrical Cables",
        "Cement Bags", "Bricks", "Pipes (PVC)", "Sand", "Aggregates",
        "Paint (Industrial)", "Tiles", "Wood Planks", "Glass Panels",
        "Insulation Material", "Fasteners & Bolts", "Roofing Sheets"
    ]
    
    data = {
        'Project_ID': np.random.choice(projects, num_rows),
        'Vendor_Name': np.random.choice(vendors, num_rows),
        'Material': np.random.choice(materials, num_rows),
        'Quantity': np.random.randint(10, 1000, num_rows),
        'Unit_Cost': np.round(np.random.uniform(50, 5000, num_rows), 2),
    }
    
    # Calculate Total_Cost
    data['Total_Cost'] = np.round(data['Quantity'] * data['Unit_Cost'], 2)
    
    # Generate Planned vs Actual costs with variance
    data['Planned_Cost'] = np.round(data['Total_Cost'] * np.random.uniform(0.85, 1.15, num_rows), 2)
    data['Actual_Cost'] = np.round(data['Total_Cost'] * np.random.uniform(0.90, 1.25, num_rows), 2)
    
    # Generate dates
    start_date = datetime(2025, 1, 1)
    data['Procurement_Date'] = [
        start_date + timedelta(days=int(x)) 
        for x in np.random.randint(0, 365, num_rows)
    ]
    
    # Calculate delivery dates with delays
    delay_days = np.random.choice(
        [-5, 0, 2, 5, 10, 15, 20, 30, 45], 
        num_rows, 
        p=[0.05, 0.15, 0.20, 0.25, 0.15, 0.10, 0.05, 0.03, 0.02]
    )
    data['Delay_Days'] = delay_days
    data['Delivery_Date'] = [
        data['Procurement_Date'][i] + timedelta(days=int(delay_days[i])) 
        for i in range(num_rows)
    ]
    
    # Billing and payment status
    data['Billing_Amount'] = np.round(data['Actual_Cost'] * np.random.uniform(0.95, 1.05, num_rows), 2)
    data['Payment_Status'] = np.random.choice(
        ['Paid', 'Pending'], 
        num_rows, 
        p=[0.65, 0.35]
    )
    
    df = pd.DataFrame(data)
    
    # Calculate additional metrics
    df['Cost_Variance'] = df['Actual_Cost'] - df['Planned_Cost']
    df['Cost_Overrun_Pct'] = np.round((df['Cost_Variance'] / df['Planned_Cost']) * 100, 2)
    
    return df

# ============================================================================
# DATA PROCESSING FUNCTIONS
# ============================================================================

def calculate_vendor_performance(df):
    """
    Aggregate vendor performance metrics
    """
    vendor_stats = df.groupby('Vendor_Name').agg({
        'Delay_Days': 'mean',
        'Total_Cost': 'sum',
        'Cost_Variance': 'mean',
        'Project_ID': 'count'
    }).round(2)
    
    vendor_stats.columns = ['Avg_Delay_Days', 'Total_Cost', 'Avg_Cost_Variance', 'Order_Count']
    vendor_stats = vendor_stats.sort_values('Avg_Delay_Days', ascending=False)
    
    return vendor_stats

def identify_top_overruns(df, top_n=10):
    """
    Identify materials with highest cost overruns
    """
    overruns = df.groupby('Material').agg({
        'Cost_Variance': 'sum',
        'Cost_Overrun_Pct': 'mean',
        'Total_Cost': 'sum'
    }).round(2)
    
    overruns = overruns.sort_values('Cost_Variance', ascending=False).head(top_n)
    return overruns

def generate_insights(df):
    """
    Generate key business insights from the data
    """
    insights = {
        'total_project_cost': df['Actual_Cost'].sum(),
        'total_planned_cost': df['Planned_Cost'].sum(),
        'avg_delay': df['Delay_Days'].mean(),
        'delayed_deliveries': len(df[df['Delay_Days'] > 5]),
        'total_deliveries': len(df),
        'max_overrun_project': df.loc[df['Cost_Variance'].idxmax(), 'Project_ID'],
        'max_overrun_amount': df['Cost_Variance'].max(),
        'pending_payments': df[df['Payment_Status'] == 'Pending']['Billing_Amount'].sum(),
        'total_cost_variance': df['Cost_Variance'].sum()
    }
    return insights

def generate_decision_insights(df, vendor_stats):
    """
    Generate automated decision recommendations
    """
    recommendations = []
    
    # Vendor delay analysis
    high_delay_vendors = vendor_stats[vendor_stats['Avg_Delay_Days'] > 10].head(3)
    for vendor in high_delay_vendors.index:
        avg_delay = high_delay_vendors.loc[vendor, 'Avg_Delay_Days']
        recommendations.append(
            f"⚠️ **{vendor}** shows average delay of {avg_delay:.1f} days. Consider alternate sourcing or penalty clauses."
        )
    
    # Cost overrun analysis
    high_overrun_projects = df.groupby('Project_ID')['Cost_Variance'].sum().sort_values(ascending=False).head(3)
    for project, variance in high_overrun_projects.items():
        if variance > 0:
            pct = (variance / df[df['Project_ID'] == project]['Planned_Cost'].sum()) * 100
            if pct > 15:
                recommendations.append(
                    f"💰 **{project}** exceeding budget by {pct:.1f}% (${variance:,.2f}). Requires immediate review."
                )
    
    # Payment pending analysis
    pending_amount = df[df['Payment_Status'] == 'Pending']['Billing_Amount'].sum()
    if pending_amount > df['Billing_Amount'].sum() * 0.3:
        recommendations.append(
            f"📋 High pending payments detected: ${pending_amount:,.2f}. Prioritize payment processing to maintain vendor relationships."
        )
    
    # Material cost analysis
    material_overruns = df.groupby('Material')['Cost_Variance'].sum().sort_values(ascending=False).head(1)
    if len(material_overruns) > 0:
        material = material_overruns.index[0]
        variance = material_overruns.values[0]
        if variance > 0:
            recommendations.append(
                f"🔧 **{material}** shows highest cost variance (${variance:,.2f}). Review procurement process and vendor contracts."
            )
    
    return recommendations

# ============================================================================
# VISUALIZATION FUNCTIONS
# ============================================================================

def plot_planned_vs_actual(df):
    """
    Bar chart comparing Planned vs Actual costs by project
    """
    project_costs = df.groupby('Project_ID')[['Planned_Cost', 'Actual_Cost']].sum().reset_index()
    
    fig = go.Figure(data=[
        go.Bar(name='Planned Cost', x=project_costs['Project_ID'], y=project_costs['Planned_Cost'], marker_color='lightblue'),
        go.Bar(name='Actual Cost', x=project_costs['Project_ID'], y=project_costs['Actual_Cost'], marker_color='coral')
    ])
    
    fig.update_layout(
        title='Planned vs Actual Cost by Project',
        xaxis_title='Project ID',
        yaxis_title='Cost ($)',
        barmode='group',
        height=400
    )
    
    return fig

def plot_payment_status(df):
    """
    Pie chart for payment status distribution
    """
    payment_data = df.groupby('Payment_Status')['Billing_Amount'].sum().reset_index()
    
    fig = px.pie(
        payment_data, 
        values='Billing_Amount', 
        names='Payment_Status',
        title='Payment Status Distribution',
        color_discrete_sequence=['#2ecc71', '#e74c3c'],
        hole=0.3
    )
    
    fig.update_layout(height=400)
    return fig

def plot_cost_trend(df):
    """
    Line chart showing cost trend over time
    """
    df_sorted = df.sort_values('Procurement_Date')
    df_sorted['Cumulative_Cost'] = df_sorted['Actual_Cost'].cumsum()
    
    fig = px.line(
        df_sorted, 
        x='Procurement_Date', 
        y='Cumulative_Cost',
        title='Cumulative Cost Trend Over Time',
        labels={'Cumulative_Cost': 'Cumulative Cost ($)', 'Procurement_Date': 'Date'}
    )
    
    fig.update_layout(height=400)
    return fig

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """
    Main Streamlit application
    """
    
    # Header
    st.title("📊 ERP-Based Cost & Procurement Analytics Dashboard")
    st.markdown("---")
    
    # Generate data
    df = generate_erp_data(300)
    
    # Sidebar filters
    st.sidebar.header("🔍 Filters")
    
    # Project filter
    projects = ['All'] + sorted(df['Project_ID'].unique().tolist())
    selected_project = st.sidebar.selectbox("Select Project", projects)
    
    # Vendor filter
    vendors = ['All'] + sorted(df['Vendor_Name'].unique().tolist())
    selected_vendor = st.sidebar.selectbox("Select Vendor", vendors)
    
    # Payment status filter
    payment_statuses = ['All', 'Paid', 'Pending']
    selected_payment = st.sidebar.selectbox("Select Payment Status", payment_statuses)
    
    # Apply filters
    filtered_df = df.copy()
    if selected_project != 'All':
        filtered_df = filtered_df[filtered_df['Project_ID'] == selected_project]
    if selected_vendor != 'All':
        filtered_df = filtered_df[filtered_df['Vendor_Name'] == selected_vendor]
    if selected_payment != 'All':
        filtered_df = filtered_df[filtered_df['Payment_Status'] == selected_payment]
    
    # Display filter info
    st.sidebar.markdown("---")
    st.sidebar.info(f"**Showing {len(filtered_df)} of {len(df)} records**")
    
    # Key Metrics Row
    st.header("📈 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    insights = generate_insights(filtered_df)
    
    with col1:
        st.metric(
            "Total Project Cost",
            f"${insights['total_project_cost']:,.2f}",
            delta=f"${insights['total_cost_variance']:,.2f}" if insights['total_cost_variance'] != 0 else None,
            delta_color="inverse"
        )
    
    with col2:
        st.metric(
            "Average Delay",
            f"{insights['avg_delay']:.1f} days"
        )
    
    with col3:
        st.metric(
            "Delayed Deliveries",
            f"{insights['delayed_deliveries']} / {insights['total_deliveries']}",
            delta=f"{(insights['delayed_deliveries']/insights['total_deliveries']*100):.1f}%"
        )
    
    with col4:
        st.metric(
            "Pending Payments",
            f"${insights['pending_payments']:,.2f}"
        )
    
    st.markdown("---")
    
    # Visualizations
    st.header("📊 Analytics & Visualizations")
    
    # Row 1: Planned vs Actual and Payment Status
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(plot_planned_vs_actual(filtered_df), use_container_width=True)
    
    with col2:
        st.plotly_chart(plot_payment_status(filtered_df), use_container_width=True)
    
    # Row 2: Cost Trend
    st.plotly_chart(plot_cost_trend(filtered_df), use_container_width=True)
    
    st.markdown("---")
    
    # Tables
    st.header("📋 Detailed Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top Vendors by Delay")
        vendor_perf = calculate_vendor_performance(filtered_df)
        st.dataframe(
            vendor_perf.head(10).style.background_gradient(cmap='Reds', subset=['Avg_Delay_Days']),
            use_container_width=True
        )
    
    with col2:
        st.subheader("Highest Cost Overruns by Material")
        overruns = identify_top_overruns(filtered_df)
        st.dataframe(
            overruns.style.background_gradient(cmap='Oranges', subset=['Cost_Variance']),
            use_container_width=True
        )
    
    st.markdown("---")
    
    # Key Insights Section
    st.header("💡 Key Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"""
        **Project Overview:**
        - Total Actual Cost: **${insights['total_project_cost']:,.2f}**
        - Total Planned Cost: **${insights['total_planned_cost']:,.2f}**
        - Overall Variance: **${insights['total_cost_variance']:,.2f}**
        """)
    
    with col2:
        st.warning(f"""
        **Delivery Performance:**
        - Average Delay: **{insights['avg_delay']:.1f} days**
        - Delayed Deliveries: **{insights['delayed_deliveries']} ({(insights['delayed_deliveries']/insights['total_deliveries']*100):.1f}%)**
        - Worst Project: **{insights['max_overrun_project']}** (${insights['max_overrun_amount']:,.2f} overrun)
        """)
    
    st.markdown("---")
    
    # Decision Insights Section
    st.header("🎯 Decision Insights & Recommendations")
    
    vendor_stats = calculate_vendor_performance(df)  # Use full dataset for better recommendations
    recommendations = generate_decision_insights(df, vendor_stats)
    
    if recommendations:
        for rec in recommendations[:3]:  # Show top 3 recommendations
            st.markdown(rec)
    else:
        st.success("✅ All metrics within acceptable thresholds. No immediate action required.")
    
    st.markdown("---")
    
    # Raw Data Section (collapsible)
    with st.expander("📄 View Raw Data"):
        st.dataframe(filtered_df, use_container_width=True)
        
        # Download button
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name='erp_data.csv',
            mime='text/csv'
        )
    
    # Footer
    st.markdown("---")
    st.caption("ERP Analytics Dashboard | Infrastructure Project Management | Data refreshes on page reload")

# ============================================================================
# RUN APPLICATION
# ============================================================================

if __name__ == "__main__":
    main()
