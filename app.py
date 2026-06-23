import streamlit as st
import pandas as pd
import plotly.express as px
from groq import Groq
from fpdf import FPDF

# إعداد الواجهة
st.set_page_config(page_title="AI Business Intelligence", layout="wide")

st.title("📊 AI Business Intelligence Dashboard 🚀")
st.markdown("---")

uploaded_file = st.file_uploader("Upload your sales CSV:", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales", f"${df['Sales'].sum():,}")
    col2.metric("Best Product", df.loc[df['Sales'].idxmax(), 'Product'])
    col3.metric("Number of Items", len(df))
    
    st.markdown("---")
    
    st.write("### 📈 Visual Analytics")
    fig = px.bar(df, x='Product', y='Sales', color='Sales', 
                 color_continuous_scale='Bluered', title="Revenue Distribution")
    st.plotly_chart(fig, use_container_width=True)

    if st.button("🚀 Generate Strategic Report"):
        # تأكدي من وضع مفتاح الـ API الخاص بك هنا بدون أي مسافات أو أحرف عربية
        client = Groq(api_key="YOUR_GROQ_API_KEY_HERE")
        
        # تنظيف الـ prompt ليحتوي على إنجليزية فقط
        prompt = f"Analyze these sales: {df.to_string()}. Provide a high-level strategic business report in professional English."
        
        with st.spinner("Analyzing..."):
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
            )
            analysis = response.choices[0].message.content
            
            # تنظيف النص الناتج ليصبح إنجليزياً فقط
            clean_analysis = analysis.encode('ascii', 'ignore').decode('ascii')
            
            st.success("Analysis Complete")
            st.write(clean_analysis)

            # إنشاء الـ PDF باستخدام النص النظيف
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 20)
            pdf.cell(0, 10, txt="Strategic Business Report", ln=True, align='C')
            pdf.ln(10)
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, txt=clean_analysis)
            pdf.output("Business_Report.pdf")

        # عرض التقرير والنموذج
        st.subheader("💡 Need the Full Professional Report?")
        st.write("Get the detailed strategic report via email.")

        with st.form("contact_form"):
            user_email = st.text_input("Enter your email or WhatsApp number:")
            submit_button = st.form_submit_button("Request Professional Report")

        if submit_button:
            if user_email:
                st.success(f"Request received successfully! We will contact you at {user_email}")
            else:
                st.warning("Please enter your contact details.")