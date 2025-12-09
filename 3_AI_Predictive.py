import streamlit as st
import pandas as pd
import io

# Set page configuration
st.set_page_config(layout="wide", page_title="AI Sales Suggestions")

def get_ai_suggestions(df):
    """
    Analyzes the sales data and generates suggestions to improve sales and profit.
    This function now assumes column names have been standardized before it is called.
    """
    suggestions = []

    try:
        # --- 1. Identify Top and Bottom Performing Products ---
        product_sales = df.groupby('Product')['TotalPrice'].sum().sort_values(ascending=False)
        
        if product_sales.empty:
            st.warning("Could not find product sales data to analyze.")
            return []

        top_product = product_sales.index[0]
        top_product_sales = product_sales.iloc[0]
        worst_product = product_sales.index[-1]
        worst_product_sales = product_sales.iloc[-1]

        suggestions.append({
            "title": "Product Performance Insights",
            "emoji": "🚀",
            "text": f"Your best-selling product is **{top_product}**, generating **${top_product_sales:,.2f}** in revenue. Consider promoting this product more heavily through marketing campaigns or bundling it with other items."
        })
        suggestions.append({
            "title": "Areas for Improvement",
            "emoji": "📉",
            "text": f"The product **{worst_product}** is your lowest performer, with sales of only **${worst_product_sales:,.2f}**. It might be time to evaluate its market fit, consider a promotional discount, or discontinue it to focus on more profitable items."
        })

        # --- 2. Analyze Sales Trends Over Time ---
        df['Month'] = df['OrderDate'].dt.to_period('M')
        monthly_sales = df.groupby('Month')['TotalPrice'].sum()
        
        if len(monthly_sales) > 1:
            last_month_sales = monthly_sales.iloc[-1]
            prev_month_sales = monthly_sales.iloc[-2]
            monthly_growth = ((last_month_sales - prev_month_sales) / prev_month_sales) * 100 if prev_month_sales != 0 else float('inf')

            trend_emoji = "📈" if monthly_growth >= 0 else "📉"
            trend_text = f"Your sales in the last month grew by **{monthly_growth:.2f}%** compared to the previous month. Keep up the great work!" if monthly_growth >= 0 else f"Your sales in the last month decreased by **{abs(monthly_growth):.2f}%**. Let's look at strategies to reverse this trend."
            suggestions.append({
                "title": "Monthly Sales Trend",
                "emoji": trend_emoji,
                "text": trend_text
            })

        # --- 3. Suggestion for a specific action ---
        suggestions.append({
            "title": "Actionable Suggestion: Bundles",
            "emoji": "💡",
            "text": f"Consider creating a product bundle. For example, you could pair your top-seller, **'{top_product}'**, with a complementary mid-range item. Bundles often increase the average order value and can help move less popular inventory."
        })

        # --- 4. General Profit Maximization Tip ---
        suggestions.append({
            "title": "Profit Maximization Tip",
            "emoji": "💰",
            "text": f"Review your pricing strategy. Analyze your profit margins on each product. A small price increase on high-demand items like **'{top_product}'** could significantly boost your overall profit without deterring customers."
        })

        return suggestions

    except KeyError as e:
        st.error(f"Analysis failed. A required column is missing: {e}. Please ensure your file contains columns for products, sales totals, and dates.")
        return []
    except Exception as e:
        st.error(f"An unexpected error occurred during analysis: {e}")
        return []

# --- Streamlit UI ---

st.title("🤖 AI-Powered Sales Advisor")
st.markdown("Upload your sales data (CSV or Excel), and our AI will provide actionable suggestions to help you increase revenue and profitability.")

# File Uploader - Now accepts both CSV and XLSX
uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        # Read the file into a pandas dataframe
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        # --- FIX: Standardize column names ---
        # This block checks for common variations and renames them
        rename_map = {
            'Item_Name': 'Product',
            'Item Name': 'Product',
            'Total_Sale': 'TotalPrice',
            'Total Sale': 'TotalPrice',
            'Date': 'OrderDate'
        }
        df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns}, inplace=True)
        
        # --- Data Validation ---
        required_columns = ['OrderDate', 'Product', 'TotalPrice']
        missing_cols = [col for col in required_columns if col not in df.columns]

        if missing_cols:
            st.error(f"Error: Your file is missing the following required columns: **{', '.join(missing_cols)}**. Please check your file and try again.")
            st.info("The tool looks for columns like 'OrderDate' (or 'Date'), 'Product' (or 'Item_Name'), and 'TotalPrice' (or 'Total_Sale').")
        else:
            # Convert date column safely
            df['OrderDate'] = pd.to_datetime(df['OrderDate'])
            
            st.success("File uploaded successfully! Here's a preview of your data with standardized columns:")
            st.dataframe(df.head())

            if st.button("Generate AI Suggestions", type="primary"):
                with st.spinner("🧠 AI is analyzing your data..."):
                    suggestions = get_ai_suggestions(df.copy()) # Pass a copy to be safe

                if suggestions:
                    st.subheader("Here are your personalized suggestions:")
                    for suggestion in suggestions:
                        st.markdown(f"### {suggestion['emoji']} {suggestion['title']}")
                        st.info(suggestion['text'])
                else:
                    st.warning("AI analysis did not produce any suggestions. This could be due to issues with the data format.")

    except Exception as e:
        st.error(f"Error processing the file: {e}")

else:
    st.info("Please upload a CSV or Excel file with your sales data to get started.")
