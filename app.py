import streamlit as st

# ===========================
# CONFIGURATION
# ===========================
st.set_page_config(page_title="HR Dashboard", layout="wide")

st.title("📊 HR Dashboard - Employee Management")

# ===========================
# INITIALISATION DES DONNÉES
# ===========================
if "employees" not in st.session_state:
    st.session_state.employees = []

# ===========================
# CREATE (AJOUT)
# ===========================
st.subheader("➕ Add Employee")

with st.form("add_employee_form"):
    name = st.text_input("Name")
    role = st.text_input("Role")
    salary = st.number_input("Salary", min_value=0)
    submitted = st.form_submit_button("Add Employee")

    if submitted:
        st.session_state.employees.append({
            "name": name,
            "role": role,
            "salary": salary
        })
        st.success("Employee added successfully ✅")

# ===========================
# READ (AFFICHAGE)
# ===========================
st.markdown("---")
st.subheader("📋 Employee List")

if len(st.session_state.employees) == 0:
    st.info("No employees yet.")
else:
    for i, emp in enumerate(st.session_state.employees):
        col1, col2, col3, col4 = st.columns([3, 3, 2, 2])

        col1.write(emp["name"])
        col2.write(emp["role"])
        col3.write(f"{emp['salary']} MAD")

        # ===========================
        # DELETE
        # ===========================
        if col4.button("❌ Delete", key=f"delete_{i}"):
            st.session_state.employees.pop(i)
            st.experimental_rerun()

# ===========================
# UPDATE (MODIFICATION)
# ===========================
st.markdown("---")
st.subheader("✏️ Update Employee")

if st.session_state.employees:
    index = st.selectbox(
        "Select employee to update",
        range(len(st.session_state.employees)),
        format_func=lambda x: st.session_state.employees[x]["name"]
    )

    emp = st.session_state.employees[index]

    with st.form("update_employee_form"):
        new_name = st.text_input("Name", emp["name"])
        new_role = st.text_input("Role", emp["role"])
        new_salary = st.number_input("Salary", emp["salary"], min_value=0)
        update_btn = st.form_submit_button("Update")

        if update_btn:
            st.session_state.employees[index] = {
                "name": new_name,
                "role": new_role,
                "salary": new_salary
            }
            st.success("Employee updated successfully ✨")
            st.experimental_rerun()

# ===========================
# FOOTER
# ===========================
st.markdown("---")
st.caption("© 2026 HR Dashboard - Streamlit CRUD (No Database)")

