import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Configuration de la page
st.set_page_config(
    page_title="HR Dashboard Pro",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé pour les couleurs
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #1E3A8A 0%, #3B82F6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }
    .card {
        background-color: #FFFFFF;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #3B82F6;
        margin-bottom: 1rem;
    }
    .employee-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .stat-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .delete-btn {
        background-color: #EF4444 !important;
        color: white !important;
        border: none !important;
    }
    .update-btn {
        background-color: #10B981 !important;
        color: white !important;
        border: none !important;
    }
    .add-btn {
        background: linear-gradient(90deg, #10B981 0%, #34D399 100%) !important;
        color: white !important;
        border: none !important;
    }
    .stButton > button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Initialisation des données
if "employees" not in st.session_state:
    # Exemple de données initiales
    st.session_state.employees = [
        {"id": 1, "name": "Ali Benali", "role": "Développeur", "department": "IT", "salary": 25000, "join_date": "2023-01-15", "status": "Actif"},
        {"id": 2, "name": "Fatima Zahra", "role": "RH Manager", "department": "RH", "salary": 35000, "join_date": "2022-05-10", "status": "Actif"},
        {"id": 3, "name": "Karim Alami", "role": "Analyste", "department": "Finance", "salary": 28000, "join_date": "2023-08-22", "status": "Actif"},
        {"id": 4, "name": "Salma Toufiq", "role": "Designer", "department": "Marketing", "salary": 22000, "join_date": "2024-01-08", "status": "Actif"},
    ]
    st.session_state.next_id = 5

# Titre principal avec style
st.markdown('<h1 class="main-header">👥 Tableau de Bord RH - Gestion des Employés</h1>', unsafe_allow_html=True)

# Sidebar pour la navigation
with st.sidebar:
    st.markdown("### 🎨 Navigation")
    page = st.radio(
        "Choisir une section:",
        ["📊 Vue d'ensemble", "➕ Ajouter Employé", "👥 Liste des Employés", "📈 Statistiques", "⚙️ Paramètres"]
    )
    
    st.markdown("---")
    st.markdown("### 🏢 Départements")
    departments = ["Tous"] + list(set([emp["department"] for emp in st.session_state.employees]))
    selected_dept = st.selectbox("Filtrer par département:", departments)
    
    st.markdown("---")
    st.markdown("### 🔍 Recherche")
    search_name = st.text_input("Rechercher par nom:")
    
    st.markdown("---")
    st.markdown("### 📊 Résumé")
    total_emp = len(st.session_state.employees)
    active_emp = len([e for e in st.session_state.employees if e["status"] == "Actif"])
    avg_salary = sum(e["salary"] for e in st.session_state.employees) / total_emp if total_emp > 0 else 0
    
    st.metric("👥 Total Employés", total_emp)
    st.metric("✅ Actifs", active_emp)
    st.metric("💰 Salaire Moyen", f"{avg_salary:,.0f} MAD")

# Filtrage des employés
filtered_employees = st.session_state.employees
if selected_dept != "Tous":
    filtered_employees = [e for e in filtered_employees if e["department"] == selected_dept]
if search_name:
    filtered_employees = [e for e in filtered_employees if search_name.lower() in e["name"].lower()]

# Pages principales
if page == "📊 Vue d'ensemble":
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="stat-card">', unsafe_allow_html=True)
        st.metric("💰 Budget Total Salaire", 
                 f"{sum(e['salary'] for e in st.session_state.employees):,.0f} MAD",
                 delta="+12% vs mois dernier")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="stat-card">', unsafe_allow_html=True)
        dept_counts = pd.DataFrame([e["department"] for e in st.session_state.employees]).value_counts()
        top_dept = dept_counts.index[0] if not dept_counts.empty else "N/A"
        st.metric("🏆 Département Principal", top_dept)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="stat-card">', unsafe_allow_html=True)
        avg_tenure = sum((datetime.now() - datetime.strptime(e["join_date"], "%Y-%m-%d")).days 
                        for e in st.session_state.employees) / (len(st.session_state.employees) * 365)
        st.metric("⏳ Ancienneté Moyenne", f"{avg_tenure:.1f} ans")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Graphiques
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Répartition des Salaires")
        if st.session_state.employees:
            df_salary = pd.DataFrame(st.session_state.employees)
            fig_salary = px.bar(df_salary, x='name', y='salary', 
                              color='department',
                              title="Salaires par Employé",
                              labels={'salary': 'Salaire (MAD)', 'name': 'Employé'},
                              color_discrete_sequence=px.colors.qualitative.Set3)
            st.plotly_chart(fig_salary, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Répartition par Département")
        if st.session_state.employees:
            dept_data = pd.DataFrame([e["department"] for e in st.session_state.employees])
            dept_counts = dept_data[0].value_counts()
            fig_dept = px.pie(values=dept_counts.values, 
                            names=dept_counts.index,
                            title="Employés par Département",
                            color_discrete_sequence=px.colors.sequential.RdBu)
            st.plotly_chart(fig_dept, use_container_width=True)

elif page == "➕ Ajouter Employé":
    st.subheader("🎯 Ajouter un Nouvel Employé")
    
    with st.form("add_employee_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Nom Complet *", placeholder="Ex: Mohamed Alami")
            role = st.text_input("Poste *", placeholder="Ex: Développeur Full Stack")
            department = st.selectbox("Département *", ["IT", "RH", "Finance", "Marketing", "Ventes", "Support"])
        
        with col2:
            salary = st.number_input("Salaire Mensuel (MAD) *", min_value=3000, max_value=100000, value=15000, step=1000)
            join_date = st.date_input("Date d'embauche", datetime.now())
            status = st.selectbox("Statut", ["Actif", "En congé", "Démission"])
        
        submitted = st.form_submit_button("➕ Ajouter Employé", type="primary", use_container_width=True)
        
        if submitted:
            if name.strip() and role.strip():
                new_employee = {
                    "id": st.session_state.next_id,
                    "name": name,
                    "role": role,
                    "department": department,
                    "salary": salary,
                    "join_date": join_date.strftime("%Y-%m-%d"),
                    "status": status
                }
                st.session_state.employees.append(new_employee)
                st.session_state.next_id += 1
                st.success(f"✅ Employé {name} ajouté avec succès!")
                st.balloons()
            else:
                st.error("❌ Veuillez remplir tous les champs obligatoires (*)")

elif page == "👥 Liste des Employés":
    st.subheader("📋 Liste des Employés")
    
    if not filtered_employees:
        st.warning("Aucun employé trouvé avec les critères de recherche.")
    else:
        for i, emp in enumerate(filtered_employees):
            status_color = {
                "Actif": "🟢",
                "En congé": "🟡", 
                "Démission": "🔴"
            }.get(emp["status"], "⚪")
            
            with st.container():
                col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 2, 2, 1, 1])
                
                with col1:
                    st.markdown(f"**{emp['name']}**")
                    st.caption(f"{status_color} {emp['status']}")
                
                with col2:
                    st.write(emp["role"])
                    st.caption(f"🏢 {emp['department']}")
                
                with col3:
                    st.write(f"💰 {emp['salary']:,.0f} MAD")
                    st.caption("Mensuel")
                
                with col4:
                    st.write(f"📅 {emp['join_date']}")
                    days_diff = (datetime.now() - datetime.strptime(emp['join_date'], "%Y-%m-%d")).days
                    st.caption(f"({days_diff} jours)")
                
                with col5:
                    if st.button("✏️", key=f"edit_{emp['id']}", help="Modifier"):
                        st.session_state.edit_id = emp['id']
                
                with col6:
                    if st.button("🗑️", key=f"delete_{emp['id']}", help="Supprimer", type="secondary"):
                        st.session_state.employees = [e for e in st.session_state.employees if e['id'] != emp['id']]
                        st.rerun()
                
                st.divider()
        
        # Section de modification
        if 'edit_id' in st.session_state:
            emp_to_edit = next((e for e in st.session_state.employees if e['id'] == st.session_state.edit_id), None)
            if emp_to_edit:
                st.subheader(f"✏️ Modifier: {emp_to_edit['name']}")
                
                with st.form("edit_employee_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        new_name = st.text_input("Nom", emp_to_edit["name"])
                        new_role = st.text_input("Poste", emp_to_edit["role"])
                        new_dept = st.selectbox("Département", 
                                               ["IT", "RH", "Finance", "Marketing", "Ventes", "Support"],
                                               index=["IT", "RH", "Finance", "Marketing", "Ventes", "Support"].index(emp_to_edit["department"]))
                    
                    with col2:
                        new_salary = st.number_input("Salaire", emp_to_edit["salary"], min_value=3000, max_value=100000, step=1000)
                        new_join_date = st.date_input("Date d'embauche", 
                                                     datetime.strptime(emp_to_edit["join_date"], "%Y-%m-%d"))
                        new_status = st.selectbox("Statut", ["Actif", "En congé", "Démission"],
                                                 index=["Actif", "En congé", "Démission"].index(emp_to_edit["status"]))
                    
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        if st.form_submit_button("💾 Enregistrer les modifications", use_container_width=True, type="primary"):
                            emp_to_edit.update({
                                "name": new_name,
                                "role": new_role,
                                "department": new_dept,
                                "salary": new_salary,
                                "join_date": new_join_date.strftime("%Y-%m-%d"),
                                "status": new_status
                            })
                            del st.session_state.edit_id
                            st.success("✅ Employé mis à jour avec succès!")
                            st.rerun()
                    
                    if st.form_submit_button("❌ Annuler", use_container_width=True):
                        del st.session_state.edit_id
                        st.rerun()

elif page == "📈 Statistiques":
    st.subheader("📊 Statistiques Avancées")
    
    if st.session_state.employees:
        df = pd.DataFrame(st.session_state.employees)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Distribution des Salaires")
            fig_hist = px.histogram(df, x='salary', nbins=10, 
                                   title="Distribution des Salaires",
                                   labels={'salary': 'Salaire (MAD)'},
                                   color_discrete_sequence=['#3B82F6'])
            fig_hist.update_layout(bargap=0.1)
            st.plotly_chart(fig_hist, use_container_width=True)
            
            st.markdown("### 🏢 Salaires par Département")
            dept_stats = df.groupby('department')['salary'].agg(['mean', 'count']).reset_index()
            fig_dept_bar = px.bar(dept_stats, x='department', y='mean',
                                 title="Salaire Moyen par Département",
                                 labels={'mean': 'Salaire Moyen (MAD)', 'department': 'Département'},
                                 color='department',
                                 color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig_dept_bar, use_container_width=True)
        
        with col2:
            st.markdown("### 📅 Embauches par Mois")
            df['join_date'] = pd.to_datetime(df['join_date'])
            df['join_month'] = df['join_date'].dt.strftime('%Y-%m')
            monthly_hire = df.groupby('join_month').size().reset_index(name='count')
            
            fig_timeline = px.line(monthly_hire, x='join_month', y='count',
                                  title="Embauches par Mois",
                                  markers=True,
                                  line_shape='spline',
                                  color_discrete_sequence=['#10B981'])
            fig_timeline.update_traces(fill='tozeroy', fillcolor='rgba(16, 185, 129, 0.1)')
            st.plotly_chart(fig_timeline, use_container_width=True)
            
            st.markdown("### 📋 Tableau des Données")
            st.dataframe(df[['name', 'department', 'role', 'salary', 'join_date', 'status']], 
                        use_container_width=True,
                        hide_index=True)

else:  # Paramètres
    st.subheader("⚙️ Paramètres")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎨 Personnalisation")
        theme_color = st.color_picker("Couleur Principale", "#3B82F6")
        
        export_format = st.selectbox("Format d'export", ["CSV", "Excel", "JSON"])
        
        if st.button("📥 Exporter les Données", use_container_width=True):
            df = pd.DataFrame(st.session_state.employees)
            if export_format == "CSV":
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("Télécharger CSV", csv, "employees.csv", "text/csv")
            elif export_format == "Excel":
                df.to_excel("employees.xlsx", index=False)
                with open("employees.xlsx", "rb") as f:
                    st.download_button("Télécharger Excel", f, "employees.xlsx")
            else:
                import json
                json_data = df.to_json(orient='records', indent=2)
                st.download_button("Télécharger JSON", json_data, "employees.json", "application/json")
    
    with col2:
        st.markdown("### ⚠️ Zone de Danger")
        
        if st.button("🗑️ Supprimer Tous les Employés", type="secondary", use_container_width=True):
            st.warning("Cette action est irréversible!")
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                confirm = st.text_input("Écrire 'CONFIRMER' pour supprimer:")
                if confirm == "CONFIRMER":
                    st.session_state.employees = []
                    st.session_state.next_id = 1
                    st.error("✅ Tous les employés ont été supprimés!")
                    st.rerun()

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col2:
    st.caption("© 2026 HR Dashboard Pro | Développé avec Streamlit 🎈")
    st.caption(f"Dernière mise à jour: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.caption(f"Nombre d'employés: {len(st.session_state.employees)}")
