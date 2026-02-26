from datetime import datetime

import humanize
import requests
import streamlit as st

from constants import CURRENCIES
from currency_converter import convert_currency, get_exchange_rate

st.title(":dollar: Currency Converter")
st.markdown("""This tools allows you to instantly convert amounts between different currencies :earth_americas:.
            Enter the amount you want to convert, and choose the currencies you want to convert from and to.
            Then click the "Convert" button to see the result!""")


url = f"https://api.exchangerate-api.com/v4/latest/USD"
response = requests.get(url)
currency_list = list(response.json()['rates'].keys())

base_currency = st.selectbox(
    "From currency(base)",
    CURRENCIES,
)
target_currency = st.selectbox(
    "To currency(target)",
    CURRENCIES,
)
amount = st.number_input("Insert amount", min_value=0.0, step=100.0)
if amount > 0 and base_currency and target_currency:
    exchange_rate = get_exchange_rate(base_currency, target_currency)
    exchange_rate, time_last_updated = get_exchange_rate(base_currency, target_currency)
    time_diff = datetime.now() - datetime.fromtimestamp(time_last_updated)
    # Use humanize to format the time difference
    time_ago = humanize.naturaltime(time_diff)
    
    if exchange_rate:
        targetted_amount = convert_currency(amount, exchange_rate)
        st.success(f":white_check_mark:  Exchange rate: {exchange_rate} (Last updated: {time_ago})")
        col1, col2, col3 = st.columns(3)
        col1.metric(f"Base currency {base_currency}", f"{amount}")
        col2.markdown("""
                        <div style="
                            display:flex;
                            flex-direction:column;
                            justify-content:center;
                            align-items:center;
                            height:10px;
                            margin-top:40px;
                            font-size:30px;
                            color:green;
                            line-height:1.5;
                        ">
                            <div style="color:green; text-shadow: 1px 0 green, -1px 0 green;">⟶</div>
                            <div style="color:green; text-shadow: 1px 0 green, -1px 0 green; margin-top:-35px;">⟵</div>
                        </div>
                        """, unsafe_allow_html=True)
        col3.metric(f"Exchanged currency {target_currency}", f"{targetted_amount:.1f}")
    else:
        st.error(":x: Error fetching exchange rate. Please try again later.")
        
    st.markdown("---")
    st.markdown("### ℹ️ About This Tool")
    st.markdown("""
    This currency converter uses real-time exchange rates provided by the ExchangeRate-API.
    - The conversion updates automatically as you input the amount or change the currency.
    - Enjoy seamless currency conversion without the need to press a button!
    """)