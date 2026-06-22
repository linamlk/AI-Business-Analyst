import streamlit as st
import pandas as pd
import plotly.express as px
from groq import Groq
from fpdf import FPDF

st.set_page_config(page_title="AI Business Intelligence", layout="wide")

# تصميم الواجهة الاحترافية
st.title("📊 AI Business Intelligence Dashboard 🚀")
st.markdown("---")

uploaded_file = st.file_uploader("Upload your sales CSV:", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    # بطاقات الأداء (Dashboard Cards)
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales", f"${df['Sales'].sum():,}")
    col2.metric("Best Product", df.loc[df['Sales'].idxmax(), 'Product'])
    col3.metric("Number of Items", len(df))
    
    st.markdown("---")
    
    # الرسم البياني المطور
    st.write("### 📈 Visual Analytics")
    fig = px.bar(df, x='Product', y='Sales', color='Sales', 
                 color_continuous_scale='Bluered', title="Revenue Distribution")
    st.plotly_chart(fig, use_container_width=True)

    if st.button("🚀 Generate Strategic Report"):
        client = Groq(api_key="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")
        prompt = f"Analyze these sales: {df.to_string()}. Provide a high-level strategic business report in professional English."
        
        with st.spinner("Analyzing..."):
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
            )
            analysis = response.choices[0].message.content
            st.success("Analysis Complete")
            st.write(analysis)

            # إنشاء الـ PDF الاحترافي
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 20)
            pdf.cell(0, 10, txt="Strategic Business Report", ln=True, align='C')
            pdf.ln(10)
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, txt=analysis)
            pdf.output("Business_Report.pdf")

            with open("Business_Report.pdf", "rb") as f:
                st.download_button("Download Report 📄", data=f, file_name="Report.pdf")