import streamlit as st
import backend
import pandas as pd
from datetime import date
import requests

st.header("Hello")

st.subheader("Sub-header shu")

st.write("paragraphiin heseg shu")

st.divider()

name = st.text_input("Нэр")

st.write("Таны нэр:",name)
age = st.number_input("Таны нас")
st.write("Таны нас:",age)

pwd = st.text_input("Password",type="password")

colors=st.selectbox("Өнгө сонгох",["Хар", "Цагаан", "Ягаан", "Бор", "Шар", "Улаан", "Ногоон"])
st.selectbox("Улс сонгох",["Япон", "Солонгос", "Хятад", "Австрали", "Орос", "Герман", "Монгол"])
colors=st.multiselect("Өнгө сонгох",["Хар", "Цагаан", "Ягаан", "Бор", "Шар", "Улаан", "Ногоон"])

st.divider()
st.subheader("Cargo price calculator")
# Жингийн хэсэг
col1, col2 = st.columns(2)

with col1:
    weight = st.number_input(
        "Жин",
        min_value=0.0,
        value=0.0,
        step=0.1
    )

with col2:
    weight_unit = st.selectbox(
        "Жингийн нэгж",
        ["kg", "tn"]
    )

# Хэмжээсийн хэсэг
st.markdown("**Хэмжээс**")

col3, col4, col5, col6 = st.columns([1, 1, 1, 0.9])

with col3:
    height = st.number_input(
        "Өндөр",
        min_value=0.0,
        value=0.0,
        step=0.1
    )

with col4:
    depth = st.number_input(
        "Өргөн",
        min_value=0.0,
        value=0.0,
        step=0.1
    )

with col5:
    length = st.number_input(
        "Урт",
        min_value=0.0,
        value=0.0,
        step=0.1
    )

with col6:
    size_unit = st.selectbox(
        "Хэмжээсийн нэгж",
        ["cm", "m"]
    )

if st.button("Тооцоолох"):
    if weight <= 0 or height <= 0 or depth <= 0 or length <= 0:
        st.error("Жин болон бүх хэмжээсийг 0-ээс их утгаар оруулна уу.")
    else:
        weight_kg = weight * 1000 if weight_unit == "tn" else weight

        if size_unit == "cm":
            height_m = height / 100
            depth_m = depth / 100
            length_m = length / 100
        else:
            height_m = height
            depth_m = depth
            length_m = length

        volume = height_m * depth_m * length_m

        price = backend.cargo_price_calculator(
            height_m,
            depth_m,
            length_m,
            weight_kg,
            kg_price=3500,
            m3_price=3000
        )

        st.success(f"Таны каргоны тооцоолсон үнэ: {price:,.2f}₮")
        st.write(f"Жин: {weight_kg:,.2f} kg")
        st.write(f"Эзлэхүүн: {volume:,.4f} м³")
st.subheader("Alt mungunii une")
col1,col2,col3=st.columns([2,2,1])

start_date = st.date_input("Ehleh hugatsaa")
end_date = st.date_input("Duusah hugatsaa")

if st.button("Haih"):
    if start_date > end_date:
        st.error("Ognoonii songolt buruu bn.")
    else:
        df = backend.alt_mungunii_une(
            start_date.strftime("%Y-%m-%d"),
            end_date.strftime("%Y-%m-%d")
        )
        st.dataframe(df)
st.divider()
st.subheader("Excel file tseverlegee")
files=st.file_uploader("file aa oruulna uu",type=["xlsx",'xls'],accept_multiple_files=True)
key="excel_cleaner_upload"
for file in files:
    st.dataframe(backend.excel_sheet_append(file))

    ## 1- cargo price jin kg,tn songodog bolgoh,  cm,m ymuu edr geed
  


            