import streamlit as st
import pandas as pd
import plotly.express as px
from groq import Groq
from fpdf import FPDF

# Page Configuration
st.set_page_config(page_title="AI Business Intelligence", layout="wide")

# Initialize Session State
if 'counter' not in st.session_state:
    st.session_state.counter = 0

st.title("📊 AI Business Intelligence Dashboard 🚀")
st.markdown("---")

uploaded_file = st.file_uploader("Upload your sales CSV:", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    # Metrics
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Sales", f"${df['Sales'].sum():,}")
    c2.metric("Best Product", df.loc[df['Sales'].idxmax(), 'Product'])
    c3.metric("Number of Items", len(df))
    
    st.markdown("---")
    
    # Visualization
    with st.expander("📈 View Visual Analytics", expanded=True):
        fig = px.bar(df, x='Product', y='Sales', color='Sales', 
                     color_continuous_scale='Bluered', title="Revenue Distribution")
        st.plotly_chart(fig, use_container_width=True)

    # Strategy Generation
    if st.button("🚀 Generate Strategic Report"):
        if st.session_state.counter < 3:
            try:
                # Initialize Client
                client = Groq(api_key="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")
                
                # Prepare Prompt
                prompt = f"Analyze these sales: {df.to_string()}. Provide a high-level strategic business report in professional English."
                
                with st.spinner("AI is crafting your strategic report..."):
                    response = client.chat.completions.create(
                        messages=[{"role": "user", "content": prompt}],
                        model="llama-3.3-70b-versatile",
                    )
                    analysis = response.choices[0].message.content
                    clean_analysis = analysis.encode('ascii', 'ignore').decode('ascii')
                    
                    # Create PDF
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Arial", 'B', 20)
                    pdf.cell(0, 10, txt="Strategic Business Report", ln=True, align='C')
                    pdf.ln(10)
                    pdf.set_font("Arial", size=12)
                    pdf.multi_cell(0, 10, txt=clean_analysis)
                    
                    # Display Result
                    st.success("Analysis Complete!")
                    st.write(clean_analysis)
                    
                    # Download Button
                    st.download_button(
                        label="📥 Download Professional PDF",
                        data=pdf.output(dest='S').encode('latin-1'),
                        file_name="Strategic_Report.pdf",
                        mime="application/pdf"
                    )
                    
                    st.session_state.counter += 1
                    st.info(f"You have used {st.session_state.counter} out of 3 free reports.")
            
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.error("⚠️ You have reached your limit of 3 free reports.")
            st.warning("To unlock unlimited access, please contact us for a subscription.")
            st.markdown("[💬 Contact us on WhatsApp](https://wa.me/213699892560)")

# Footer
st.markdown("---")
st.caption("Powered by LINA AI Business Intelligence © 2026")