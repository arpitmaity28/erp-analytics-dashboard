"""
Test script to verify ERP data generation and analytics functions
"""

import sys
sys.path.insert(0, '/home/harpyb/Documents/valentines')

from app import (
    generate_erp_data,
    calculate_vendor_performance,
    identify_top_overruns,
    generate_insights,
    generate_decision_insights
)

print("=" * 80)
print("ERP ANALYTICS DASHBOARD - DATA VALIDATION TEST")
print("=" * 80)

# Generate test data
print("\n1. Generating synthetic ERP data (300 rows)...")
df = generate_erp_data(300)
print(f"   ✓ Generated {len(df)} rows")
print(f"   ✓ Columns: {list(df.columns)}")

# Validate data structure
print("\n2. Validating data structure...")
expected_columns = [
    'Project_ID', 'Vendor_Name', 'Material', 'Quantity', 'Unit_Cost',
    'Total_Cost', 'Planned_Cost', 'Actual_Cost', 'Procurement_Date',
    'Delivery_Date', 'Delay_Days', 'Billing_Amount', 'Payment_Status',
    'Cost_Variance', 'Cost_Overrun_Pct'
]
for col in expected_columns:
    assert col in df.columns, f"Missing column: {col}"
print(f"   ✓ All {len(expected_columns)} required columns present")

# Display sample data
print("\n3. Sample data (first 5 rows):")
print(df.head()[['Project_ID', 'Vendor_Name', 'Material', 'Total_Cost', 'Delay_Days']].to_string())

# Test vendor performance calculation
print("\n4. Vendor Performance Analysis...")
vendor_perf = calculate_vendor_performance(df)
print(f"   ✓ Analyzed {len(vendor_perf)} vendors")
print(f"\n   Top 3 vendors by delay:")
print(vendor_perf.head(3)[['Avg_Delay_Days', 'Total_Cost', 'Order_Count']].to_string())

# Test cost overrun identification
print("\n5. Cost Overrun Analysis...")
overruns = identify_top_overruns(df, top_n=5)
print(f"   ✓ Identified top {len(overruns)} cost overrun materials")
print(f"\n   Top 3 materials by cost variance:")
print(overruns.head(3)[['Cost_Variance', 'Cost_Overrun_Pct']].to_string())

# Test insights generation
print("\n6. Key Insights Generation...")
insights = generate_insights(df)
print(f"   ✓ Total Project Cost: ${insights['total_project_cost']:,.2f}")
print(f"   ✓ Total Planned Cost: ${insights['total_planned_cost']:,.2f}")
print(f"   ✓ Average Delay: {insights['avg_delay']:.2f} days")
print(f"   ✓ Delayed Deliveries: {insights['delayed_deliveries']} of {insights['total_deliveries']}")
print(f"   ✓ Pending Payments: ${insights['pending_payments']:,.2f}")
print(f"   ✓ Max Overrun Project: {insights['max_overrun_project']} (${insights['max_overrun_amount']:,.2f})")

# Test decision insights
print("\n7. Decision Insights & Recommendations...")
recommendations = generate_decision_insights(df, vendor_perf)
print(f"   ✓ Generated {len(recommendations)} recommendations:")
for i, rec in enumerate(recommendations[:3], 1):
    # Remove markdown formatting for console output
    clean_rec = rec.replace('**', '').replace('⚠️', '[!]').replace('💰', '[$]').replace('📋', '[#]').replace('🔧', '[+]')
    print(f"   {i}. {clean_rec}")

# Summary statistics
print("\n8. Data Summary Statistics:")
print(f"   ✓ Projects: {df['Project_ID'].nunique()}")
print(f"   ✓ Vendors: {df['Vendor_Name'].nunique()}")
print(f"   ✓ Materials: {df['Material'].nunique()}")
print(f"   ✓ Payment Status - Paid: {len(df[df['Payment_Status']=='Paid'])}")
print(f"   ✓ Payment Status - Pending: {len(df[df['Payment_Status']=='Pending'])}")
print(f"   ✓ Average Cost Overrun: {df['Cost_Overrun_Pct'].mean():.2f}%")
print(f"   ✓ Date Range: {df['Procurement_Date'].min()} to {df['Procurement_Date'].max()}")

print("\n" + "=" * 80)
print("✓ ALL TESTS PASSED SUCCESSFULLY!")
print("=" * 80)
print("\nThe ERP Analytics Dashboard is ready to use.")
print("Run with: streamlit run app.py")
print("=" * 80)
