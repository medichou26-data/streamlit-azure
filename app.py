import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import numpy as np

# ===========================
# CONFIGURATION
# ===========================
st.set_page_config(page_title="HR Dashboard", layout="wide")

# Load dataset
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("employees.csv")
        # Ensure required columns exist
        required_columns = ['Gender', 'Years_at_Company', 'Salary', 'Department', 
                           'MaritalStatus', 'AgeGroup', 'HireDate', 'Source']
        for col in required_columns:
            if col not in df.columns:
                df[col] = None
        return df
    except:
        # Create sample data if file doesn't exist
        return create_sample_data()

def create_sample_data():
    """Create sample data for demo purposes"""
    data = {
        'EmployeeID': list(range(1, 101)),
        'FirstName': [f'First{i}' for i in range(1, 101)],
        'LastName': [f'Last{i}' for i in range(1, 101)],
        'Gender': np.random.choice(['Male', 'Female'], 100),
        'Department': np.random.choice(['HR', 'IT', 'Sales', 'Marketing', 'Finance'], 100),
        'MaritalStatus': np.random.choice(['Single', 'Married', 'Divorced'], 100),
        'AgeGroup': np.random.choice(['20-30', '31-40', '41-50', '51-60'], 100),
        'Years_at_Company': np.random.randint(1, 20, 100),
        'Salary': np.random.randint(30000, 150000, 100),
        'HireDate': pd.date_range(start='2010-01-01', periods=100, freq='D').strftime('%Y-%m-%d'),
        'Source': np.random.choice(['LinkedIn', 'Job Board', 'Referral', 'Campus'], 100),
        'Email': [f'employee{i}@company.com' for i in range(1, 101)]
    }
    return pd.DataFrame(data)

# Load data
df = load_data()

# Theme colors (modifiable)
PRIMARY = st.sidebar.color_picker("Primary Color", "#1E88E5")
BACKGROUND = st.sidebar.color_picker("Background Color", "#F5F7FA")
CARD_BG = st.sidebar.color_picker("Card Background", "#FFFFFF")

st.markdown(f"""
<style>
    body {{
        background-color: {BACKGROUND};
    }}
    .metric-card {{
        background-color: {CARD_BG};
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        text-align: center;
    }}
    .stDataFrame {{
        background-color: {CARD_BG};
        border-radius: 12px;
        padding: 10px;
    }}
</style>
""", unsafe_allow_html=True)

# ===========================
# SIDEBAR - CRUD OPERATIONS
# ===========================
st.sidebar.title("📝 CRUD Operations")

operation = st.sidebar.selectbox(
    "Select Operation",
    ["View Data", "Add Employee", "Update Employee", "Delete Employee", "Search Employees"]
)

# ===========================
# CRUD FUNCTIONS
# ===========================
def add_employee(new_data):
    """Add new employee to dataframe"""
    global df
    new_id = df['EmployeeID'].max() + 1 if 'EmployeeID' in df.columns and len(df) > 0 else 1
    new_data['EmployeeID'] = new_id
    df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
    save_data()
    st.success(f"✅ Employee added successfully! Employee ID: {new_id}")

def update_employee(employee_id, updated_data):
    """Update existing employee data"""
    global df
    if employee_id in df['EmployeeID'].values:
        idx = df[df['EmployeeID'] == employee_id].index[0]
        for key, value in updated_data.items():
            if key in df.columns:
                df.at[idx, key] = value
        save_data()
        st.success("✅ Employee updated successfully!")
    else:
        st.error("❌ Employee ID not found!")

def delete_employee(employee_id):
    """Delete employee from dataframe"""
    global df
    if employee_id in df['EmployeeID'].values:
        df = df[df['EmployeeID'] != employee_id]
        save_data()
        st.success("✅ Employee deleted successfully!")
    else:
        st.error("❌ Employee ID not found!")

def save_data():
    """Save dataframe to CSV"""
    df.to_csv("employees.csv", index=False)

# ===========================
# CRUD INTERFACES
# ===========================
if operation == "Add Employee":
    st.sidebar.subheader("➕ Add New Employee")
    
    with st.sidebar.form("add_employee_form"):
        first_name = st.text_input("First Name*", max_chars=50)
        last_name = st.text_input("Last Name*", max_chars=50)
        email = st.text_input("Email*")
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        department = st.selectbox("Department", ["HR", "IT", "Sales", "Marketing", "Finance", "Operations"])
        marital_status = st.selectbox("Marital Status", ["Single", "Married", "Divorced", "Widowed"])
        age_group = st.selectbox("Age Group", ["20-30", "31-40", "41-50", "51-60", "60+"])
        years_at_company = st.number_input("Years at Company", min_value=0, max_value=50, value=1)
        salary = st.number_input("Salary ($)", min_value=20000, max_value=300000, value=50000)
        hire_date = st.date_input("Hire Date", value=datetime.today())
        source = st.selectbox("Recruitment Source", ["LinkedIn", "Job Board", "Referral", "Campus", "Other"])
        
        submitted = st.form_submit_button("Add Employee")
        
        if submitted:
            if first_name and last_name and email:
                new_employee = {
                    'FirstName': first_name,
                    'LastName': last_name,
                    'Email': email,
                    'Gender': gender,
                    'Department': department,
                    'MaritalStatus': marital_status,
                    'AgeGroup': age_group,
                    'Years_at_Company': years_at_company,
                    'Salary': salary,
                    'HireDate': hire_date.strftime('%Y-%m-%d'),
                    'Source': source
                }
                add_employee(new_employee)
            else:
                st.error("Please fill all required fields (*)")

elif operation == "Update Employee":
    st.sidebar.subheader("✏️ Update Employee")
    
    employee_ids = sorted(df['EmployeeID'].unique()) if 'EmployeeID' in df.columns else []
    if employee_ids:
        selected_id = st.sidebar.selectbox("Select Employee ID", employee_ids)
        
        if selected_id:
            employee_data = df[df['EmployeeID'] == selected_id].iloc[0]
            
            with st.sidebar.form("update_employee_form"):
                st.write(f"Updating: {employee_data.get('FirstName', '')} {employee_data.get('LastName', '')}")
                
                # Create editable fields with current values
                first_name = st.text_input("First Name", value=employee_data.get('FirstName', ''))
                last_name = st.text_input("Last Name", value=employee_data.get('LastName', ''))
                email = st.text_input("Email", value=employee_data.get('Email', ''))
                gender = st.selectbox("Gender", ["Male", "Female", "Other"], 
                                    index=["Male", "Female", "Other"].index(employee_data.get('Gender', 'Male')))
                department = st.selectbox("Department", ["HR", "IT", "Sales", "Marketing", "Finance", "Operations"],
                                        index=["HR", "IT", "Sales", "Marketing", "Finance", "Operations"].index(
                                            employee_data.get('Department', 'HR')))
                salary = st.number_input("Salary ($)", min_value=20000, max_value=300000, 
                                       value=int(employee_data.get('Salary', 50000)))
                
                submitted = st.form_submit_button("Update Employee")
                
                if submitted:
                    updated_data = {
                        'FirstName': first_name,
                        'LastName': last_name,
                        'Email': email,
                        'Gender': gender,
                        'Department': department,
                        'Salary': salary
                    }
                    update_employee(selected_id, updated_data)

elif operation == "Delete Employee":
    st.sidebar.subheader("🗑️ Delete Employee")
    
    employee_ids = sorted(df['EmployeeID'].unique()) if 'EmployeeID' in df.columns else []
    if employee_ids:
        selected_id = st.sidebar.selectbox("Select Employee ID to Delete", employee_ids)
        
        if selected_id:
            employee_info = df[df['EmployeeID'] == selected_id].iloc[0]
            st.sidebar.write(f"**Employee:** {employee_info.get('FirstName', '')} {employee_info.get('LastName', '')}")
            st.sidebar.write(f"**Department:** {employee_info.get('Department', '')}")
            
            if st.sidebar.button("Delete Employee", type="primary"):
                delete_employee(selected_id)

elif operation == "Search Employees":
    st.sidebar.subheader("🔍 Search Employees")
    
    search_by = st.sidebar.selectbox("Search by", ["Name", "Department", "Email"])
    search_term = st.sidebar.text_input("Search term")
    
    if search_term:
        if search_by == "Name":
            mask = df['FirstName'].str.contains(search_term, case=False, na=False) | \
                   df['LastName'].str.contains(search_term, case=False, na=False)
        elif search_by == "Department":
            mask = df['Department'].str.contains(search_term, case=False, na=False)
        else:  # Email
            mask = df['Email'].str.contains(search_term, case=False, na=False)
        
        results = df[mask]
        st.sidebar.write(f"Found {len(results)} employees")

# ===========================
# DASHBOARD TITLE
# ===========================
st.title("📊 Workforce Diversity Dashboard")

# Show current operation status
st.info(f"**Current Mode:** {operation}")

# ===========================
# TOP KPI CARDS
# ===========================
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Employees", df.shape[0])
col2.metric("Males", df[df["Gender"]=="Male"].shape[0] if 'Gender' in df.columns else 0)
col3.metric("Females", df[df["Gender"]=="Female"].shape[0] if 'Gender' in df.columns else 0)
col4.metric("Avg Service (Years)", round(df["Years_at_Company"].mean(), 1) if 'Years_at_Company' in df.columns else 0)
col5.metric("Avg Salary", f"{int(df['Salary'].mean()/1000)}K" if 'Salary' in df.columns else "0K")

# ===========================
# DATA PREVIEW SECTION
# ===========================
st.subheader("👥 Employee Data")
st.dataframe(
    df.head(20),
    use_container_width=True,
    column_config={
        "EmployeeID": "ID",
        "FirstName": "First Name",
        "LastName": "Last Name",
        "Years_at_Company": st.column_config.NumberColumn("Years", format="%.1f"),
        "Salary": st.column_config.NumberColumn("Salary", format="$%d")
    },
    hide_index=True
)

# Show total records
st.caption(f"Showing 20 of {len(df)} total employees")

# ===========================
# GRAPHS
# ===========================

if operation == "View Data" or operation == "Search Employees":
    # Create columns for graphs
    c1, c2 = st.columns(2)
    
    with c1:
        if 'Department' in df.columns and len(df) > 0:
            fig_dept = px.bar(
                df["Department"].value_counts().reset_index(),
                x="Department", y="count",
                title="Employees by Department",
                color="Department",
                color_discrete_sequence=[PRIMARY]
            )
            st.plotly_chart(fig_dept, use_container_width=True)
    
    with c2:
        if 'MaritalStatus' in df.columns and len(df) > 0:
            fig_marital = px.bar(
                df["MaritalStatus"].value_counts().reset_index(),
                x="count", y="MaritalStatus", orientation="h",
                title="Marital Status Breakdown",
                color="MaritalStatus",
                color_discrete_sequence=[PRIMARY]
            )
            st.plotly_chart(fig_marital, use_container_width=True)
    
    c3, c4 = st.columns(2)
    
    with c3:
        if 'AgeGroup' in df.columns and len(df) > 0:
            fig_age = px.pie(
                df,
                names="AgeGroup",
                title="Employees by Age Group",
                hole=0.55,
                color_discrete_sequence=px.colors.sequential.Blues
            )
            st.plotly_chart(fig_age, use_container_width=True)
    
    with c4:
        if 'HireDate' in df.columns and len(df) > 0:
            df2 = df.copy()
            df2["HireDate"] = pd.to_datetime(df2["HireDate"], errors='coerce')
            df2 = df2.dropna(subset=['HireDate'])
            df2 = df2.sort_values('HireDate')
            df2 = df2.groupby("HireDate").size().cumsum().reset_index(name="Cumulative")
            
            if len(df2) > 0:
                fig_hire = px.area(
                    df2, x="HireDate", y="Cumulative",
                    title="Cumulative Headcount",
                    color_discrete_sequence=[PRIMARY]
                )
                st.plotly_chart(fig_hire, use_container_width=True)
    
    if 'Source' in df.columns and len(df) > 0:
        fig_rec = px.bar(
            df["Source"].value_counts().reset_index(),
            y="Source", x="count",
            orientation="h",
            title="Employees by Recruitment Source",
            color="Source",
            color_discrete_sequence=[PRIMARY]
        )
        st.plotly_chart(fig_rec, use_container_width=True)

# ===========================
# DATA DOWNLOAD
# ===========================
st.sidebar.markdown("---")
st.sidebar.subheader("💾 Data Export")

# Export current view
csv = df.to_csv(index=False).encode('utf-8')
st.sidebar.download_button(
    label="Download CSV",
    data=csv,
    file_name="employees_data.csv",
    mime="text/csv",
    help="Download the complete employee database"
)

# Reset button
if st.sidebar.button("🔄 Reset to Original Data"):
    df = create_sample_data()
    save_data()
    st.rerun()

# ===========================
# FOOTER
# ===========================
st.markdown("---")
st.caption("HR Dashboard v2.0 | CRUD Operations Enabled")
