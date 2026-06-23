import streamlit as st
import pandas as pd
import plotly.express as px
from groq import Groq
from fpdf import FPDF

# إعداد الصفحة
st.set_page_config(page_title="AI Business Intelligence", layout="wide")

# تهيئة عدّاد المحاولات
if 'counter' not in st.session_state:
    st.session_state.counter = 0

st.title("📊 AI Business Intelligence Dashboard 🚀")
st.markdown("---")

uploaded_file = st.file_uploader("Upload your sales CSV:", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    # بطاقات الأداء بتصميم أنيق
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Sales", f"${df['Sales'].sum():,}")
    c2.metric("Best Product", df.loc[df['Sales'].idxmax(), 'Product'])
    c3.metric("Number of Items", len(df))
    
    st.markdown("---")
    
    # الرسم البياني
    with st.expander("📈 View Visual Analytics", expanded=True):
        fig = px.bar(df, x='Product', y='Sales', color='Sales', 
                     color_continuous_scale='Bluered', title="Revenue Distribution")
        st.plotly_chart(fig, use_container_width=True)

    # نظام الـ 3 محاولات
    if st.button("🚀 Generate Strategic Report"):
        if st.session_state.counter < 3:
            
            # --- منطقة معالجة التقرير ---
            client = Groq(api_key="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")
            prompt = f"Analyze these sales: {df.to_string()}. Provide a high-level strategic business report in professional English."
            
            with st.spinner("AI is crafting your strategic report..."):
                response = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama-3.3-70b-versatile",
                )
                analysis = response.choices[0].message.content
                clean_analysis = analysis.encode('ascii', 'ignore').decode('ascii')
                
                # إنشاء PDF في الذاكرة
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", 'B', 20)
                pdf.cell(0, 10, txt="Strategic Business Report", ln=True, align='C')
                pdf.ln(10)
                pdf.set_font("Arial", size=12)
                pdf.multi_cell(0, 10, txt=clean_analysis)
                
                # عرض النتيجة
                st.success("Analysis Complete!")
                st.write(clean_analysis)
                
                # زر التحميل المباشر
               # بدلاً من الكود السابق، استخدمي هذا الجزء للتحميل
                pdf_output = pdf.output(dest='S').encode('latin-1')
                
                st.download_button(
                    label="📥 Download Professional PDF",
                    data=pdf_output,
                    file_name="Strategic_Report.pdf",
                    mime="application/pdf"
                )   
                # زيادة العداد
                st.session_state.counter += 1
                st.info(f"You have used {st.session_state.counter} out of 3 free reports.")
        else:
            # رسالة الحظر بعد 3 محاولات
            st.error("⚠️ You have reached your limit of 3 free reports.")
            st.warning("To unlock unlimited access and advanced analytics, please contact us for a subscription.")
            st.markdown("[💬 Contact us on WhatsApp for Subscription](https://wa.me/رقمك_هنا)")

# تذييل الصفحة
st.markdown("---")
st.caption("Powered by LINA AI Business Intelligence © 2026")