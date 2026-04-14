
import streamlit as st
import time
import pandas as pd
import numpy as np
import os
import requests
import openai
import json
import re
import datetime
import backend.functions as back
import ast
import operator

st.set_page_config(
    page_title="Way Academy - Demo chatbot",
    page_icon="🤖"
)

CONTACT_REPLY = "Манай холбоо барих утасны дугаар: 99887766"
LOCATION_REPLY = "Манай байршил: Galaxy tower 7 давхар, 705 тоот"

st.title("Way Academy - Demo chatbot")
st.info("AI chatbot course deliverable demonstration")


def is_date(text: str) -> bool:
    return bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", text.strip()))


def is_math_expression(text: str) -> bool:
    text = text.strip()
    return bool(re.fullmatch(r"[\d\s\+\-\*\/\%\.\(\)]+", text))


def safe_eval(expr: str):
    allowed_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Mod: operator.mod,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)

        elif isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("Зөвхөн тоон утга зөвшөөрнө.")

        elif isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type not in allowed_operators:
                raise ValueError("Дэмжигдээгүй үйлдэл байна.")
            left = _eval(node.left)
            right = _eval(node.right)
            return allowed_operators[op_type](left, right)

        elif isinstance(node, ast.UnaryOp):
            op_type = type(node.op)
            if op_type not in allowed_operators:
                raise ValueError("Дэмжигдээгүй unary үйлдэл байна.")
            operand = _eval(node.operand)
            return allowed_operators[op_type](operand)

        raise ValueError("Буруу илэрхийлэл байна.")

    tree = ast.parse(expr, mode="eval")
    return _eval(tree)


def get_rate_by_date(date_str: str):
    url = "https://www.mongolbank.mn/mn/currency-rates/data"
    params = {
        "startDate": date_str,
        "endDate": date_str
    }

    try:
        response = requests.post(url, params=params, timeout=15)
        response.raise_for_status()

        result = response.json()

        if "data" not in result or not result["data"]:
            return f"{date_str} өдрийн ханш олдсонгүй."

        raw_df = pd.DataFrame(result["data"])

        df = raw_df.melt(
            id_vars=["RATE_DATE"],
            var_name="Currency",
            value_name="Rate"
        )

        df = df.rename(columns={"RATE_DATE": "Date"})
        return df

    except requests.exceptions.RequestException as e:
        return f"Хүсэлт амжилтгүй: {e}"
    except ValueError:
        return "JSON өгөгдөл уншихад алдаа гарлаа."


def generate_response(query: str):
    q = query.strip()
    q_lower = q.lower()

    replies = []

    if any(keyword in q_lower for keyword in ["утас", "contact", "холбоо барих"]):
        replies.append(CONTACT_REPLY)

    if any(keyword in q_lower for keyword in ["байршил", "location", "хаяг", "address"]):
        replies.append(LOCATION_REPLY)

    if replies:
        return "\n\n".join(replies)

    if is_date(q):
        try:
            return get_rate_by_date(q)
        except Exception as e:
            return f"Ханш авахад алдаа гарлаа: {e}"

    if is_math_expression(q):
        try:
            result = safe_eval(q)
            return f"Хариу: {result}"
        except Exception as e:
            return f"Бодоход алдаа гарлаа: {e}"

    return q


if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["type"] == "dataframe":
            st.dataframe(message["output"], use_container_width=True, hide_index=True)
        else:
            st.markdown(message["output"])


prompt = st.chat_input("Танд юугаар туслах вэ?")

if prompt:
    st.session_state.messages.append({
        "role": "user",
        "output": prompt,
        "type": "text"
    })

    with st.spinner("Хариу бичиж байна..."):
        answer = generate_response(prompt)

    st.session_state.messages.append({
        "role": "assistant",
        "output": answer,
        "type": "dataframe" if isinstance(answer, pd.DataFrame) else "text"
    })

    st.rerun()
#### 2.
# Хэрэглэгчийн бичсэн query-нд
## if "утас", 'contact', 'холбоо барих' гэсэн үгс орсон байвал 'Манай холбооо барих утасны дугаар: 99887766' гэдэг хариу илгээдэг байх
## if 'байршил', 'location' гэсэн үгс орсон байвал 'Манай байршил: Galaxy tower 7 давхар, 705 тоот' гэдэг хариу илгээдэг байх

#### 3.
# Хэрэглэгчийн бичсэн query нь math тэгшитгэл байвад бодоод хариуг нь өгдөг байх
### Жишээ нь: (2+3)*2 -->> str-г бодох --->

#### 4.
# Хэрэглэгчийн бичсэн query нь YYYY-mm-dd формат бүхий огноо байвал монгол банкны ханшийн API-г дуудаад хариуг нь илгээдэг байх (start, end date-г нь ижил огноогоор өгөх)

### Бусад тохиолдолд Хэрэглэгчийн бичсэн query-г шууд буцаагаад хариултанд өгдөг байх


