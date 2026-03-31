# ERP ANALYTICS DASHBOARD - QUICK REFERENCE

## 🚀 START THE DASHBOARD

```bash
# Option 1: Quick start (recommended)
./start_dashboard.sh

# Option 2: Manual start
source venv/bin/activate && streamlit run app.py

# Option 3: Background mode
source venv/bin/activate && streamlit run app.py &
```

## 🧪 RUN TESTS

```bash
source venv/bin/activate && python test_erp.py
```

## 🌐 ACCESS THE DASHBOARD

Once running, open in your browser:
- **Local**: http://localhost:8501
- **Network**: http://<your-ip>:8501

## 🛑 STOP THE DASHBOARD

```bash
# If running in foreground: Press Ctrl+C

# If running in background:
pkill -f "streamlit run app.py"

# Or find and kill the process:
ps aux | grep streamlit
kill <PID>
```

## 📦 REINSTALL DEPENDENCIES

```bash
source venv/bin/activate
pip install -r requirements.txt --upgrade
```

## 💾 EXPORT DATA FROM DASHBOARD

1. Open the dashboard at http://localhost:8501
2. Scroll to bottom section "View Raw Data"
3. Click "Download CSV" button
4. Data saves as `erp_data.csv`

## 🔍 DASHBOARD FEATURES QUICK GUIDE

### Sidebar Filters
- **Project ID**: Filter by specific project (PRJ-001 to PRJ-015)
- **Vendor Name**: Filter by vendor
- **Payment Status**: Show Paid, Pending, or All

### Key Metrics (Top Row)
- Total Project Cost (with variance)
- Average Delivery Delay
- Delayed Deliveries Count
- Pending Payments Amount

### Visualizations
1. **Planned vs Actual Cost**: Bar chart showing budget comparison
2. **Payment Status**: Pie chart of paid vs pending
3. **Cost Trend**: Line chart of cumulative spending over time

### Analytics Tables
- **Top Vendors by Delay**: Identifies problematic suppliers
- **Cost Overruns by Material**: Shows which materials exceed budget

### Decision Insights
- Automated recommendations based on:
  - Vendor performance (delay thresholds)
  - Budget overruns (>15%)
  - Payment processing needs
  - Material cost variances

## 🎨 CUSTOMIZATION

### Change Number of Data Rows
Edit `app.py` line 258:
```python
df = generate_erp_data(300)  # Change 300 to desired number
```

### Add New Projects/Vendors
Edit `app.py` lines 31-42:
```python
projects = [f"PRJ-{i:03d}" for i in range(1, 16)]  # Adjust range
vendors = ["BuildCorp Ltd", ...]  # Add vendors to list
materials = ["Concrete Grade M30", ...]  # Add materials
```

### Modify Delay Thresholds
Edit `app.py` line 133 (Decision Insights):
```python
high_delay_vendors = vendor_stats[vendor_stats['Avg_Delay_Days'] > 10]  # Change 10
```

### Change Budget Overrun Alert Level
Edit `app.py` line 143:
```python
if pct > 15:  # Change 15 to desired percentage
```

## 📊 DATA SCHEMA REFERENCE

| Column | Type | Example | Description |
|--------|------|---------|-------------|
| Project_ID | String | PRJ-007 | Project identifier |
| Vendor_Name | String | BuildCorp Ltd | Supplier name |
| Material | String | Concrete Grade M30 | Material type |
| Quantity | Integer | 450 | Units ordered |
| Unit_Cost | Float | 2500.00 | Cost per unit |
| Total_Cost | Float | 1125000.00 | Quantity × Unit_Cost |
| Planned_Cost | Float | 1050000.00 | Budgeted amount |
| Actual_Cost | Float | 1175000.00 | Real expenditure |
| Procurement_Date | Date | 2025-03-15 | Order date |
| Delivery_Date | Date | 2025-03-22 | Delivery date |
| Delay_Days | Integer | 7 | Days delayed |
| Billing_Amount | Float | 1180000.00 | Invoice total |
| Payment_Status | String | Pending | Paid/Pending |
| Cost_Variance | Float | 125000.00 | Actual - Planned |
| Cost_Overrun_Pct | Float | 11.90 | Variance % |

## 🐛 TROUBLESHOOTING

### Port Already in Use
```bash
# Kill existing Streamlit process
pkill -f streamlit

# Or use different port
streamlit run app.py --server.port=8502
```

### Module Not Found
```bash
# Ensure venv is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Slow Performance
```bash
# Clear Streamlit cache
streamlit cache clear

# Or restart the app
```

### Browser Doesn't Auto-Open
Manually navigate to: http://localhost:8501

## 📞 FILE REFERENCE

- `app.py` - Main dashboard application
- `test_erp.py` - Data validation tests
- `requirements.txt` - Python dependencies
- `start_dashboard.sh` - Quick start script
- `ERP_README.md` - Full documentation
- `PROJECT_SUMMARY.md` - Project overview
- `QUICK_REFERENCE.md` - This file

## ⚡ PERFORMANCE TIPS

1. Data is cached - refresh browser to regenerate
2. Filters update in real-time (no refresh needed)
3. Use specific filters to reduce data processing
4. CSV export uses filtered data only

## 🎯 COMMON WORKFLOWS

### Analyze Specific Project
1. Sidebar → Select Project → Choose project ID
2. View updated metrics and charts
3. Check decision insights for recommendations

### Identify Problem Vendors
1. Check "Top Vendors by Delay" table
2. Click vendor in sidebar filter
3. Review their specific delivery performance

### Export Filtered Data
1. Apply desired filters
2. Expand "View Raw Data"
3. Click "Download CSV"

### Monthly Review Process
1. No filters (view all data)
2. Check key metrics dashboard
3. Review decision insights
4. Note top 3 delayed vendors
5. Identify cost overrun projects

---

**Quick Help**: For full documentation, see `ERP_README.md`  
**Dashboard URL**: http://localhost:8501  
**Stop Server**: Ctrl+C or `pkill -f streamlit`
