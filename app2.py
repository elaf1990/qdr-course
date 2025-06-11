import streamlit as st
st.set_page_config(page_title=" اختبار القدرات الكمي - بعد الدورة", layout="centered")
st.title(" اختبار القدرات الكمي - بعد الدورة")

import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime
import os
import time
from fpdf import FPDF
import arabic_reshaper
from bidi.algorithm import get_display


# كلمة المرور الخاصة بطلابك فقط
PASSWORD = "qdr2025"  # غيرها لكلمة سر تحبها

# نموذج إدخال كلمة المرور
password = st.text_input("أدخل كلمة المرور للدخول إلى الاختبار", type="password")

if password != PASSWORD:
    st.warning("كلمة المرور غير صحيحة أو لم تُدخل بعد.")
    st.stop()  # يوقف التطبيق إذا كلمة السر خطأ




student_name = st.text_input("👤 أدخل اسمك كما كتبته في الاختبار التأسيسي:")
notes = st.text_area(" ملاحظاتك أو الصعوبات التي واجهتها (اختياري):")


def ar(text):
    return get_display(arabic_reshaper.reshape(text))

from fpdf import FPDF
import arabic_reshaper
from bidi.algorithm import get_display

def ar(text):
    return get_display(arabic_reshaper.reshape(text))

def generate_pdf(name, old_scores, new_scores, notes, avg_before, avg_after, improvement):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("Arabic", "", "Amiri-Regular.ttf", uni=True)
    pdf.set_font("Arabic", size=16)
    
    
    pdf.set_text_color(0, 102, 204)
    pdf.cell(0, 10, ar(f"📘 تقرير الأداء النهائي"), ln=True, align="C")
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arabic", size=13)
    pdf.cell(0, 10, ar(f"اسم الطالب: {name}"), ln=True)
    pdf.cell(0, 10, ar(f"📅 التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M')}"), ln=True)
    pdf.ln(5)

    
    pdf.set_font("Arabic", size=12)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(0, 10, ar("📊 مقارنة الأداء حسب القسم:"), ln=True)
    pdf.set_text_color(0, 0, 0)
    for sec in new_scores:
        before = old_scores.get(sec, "N/A")
        after = new_scores.get(sec, "N/A")
        msg = f"🔸 {sec}: قبل = {before}٪، بعد = {after}٪"
        pdf.cell(0, 8, ar(msg), ln=True)
    
    pdf.ln(5)
    pdf.cell(0, 8, ar(f"✅ المتوسط قبل الدورة: {round(avg_before)}٪"), ln=True)
    pdf.cell(0, 8, ar(f"✅ المتوسط بعد الدورة: {round(avg_after)}٪"), ln=True)
    pdf.cell(0, 8, ar(f" نسبة التحسن: {round(improvement)}٪"), ln=True)

    
    pdf.ln(10)
    pdf.set_font("Arabic", size=13)
    pdf.set_text_color(0, 153, 51)
    if improvement > 15:
        msg = "🎉 تحسن مذهل! أداؤك تطوّر بشكل رائع، أنت من القلة المتميزة."
    elif improvement >= 5:
        msg = " تحسن جيد! تحتاج تعزيز بعض المهارات، لكنك على الطريق الصحيح."
    else:
        msg = " التحسن محدود. ننصحك بمراجعة الأساسيات من جديد لتحقيق تقدم أكبر."
    pdf.multi_cell(0, 8, ar(msg))

   
    if notes.strip():
        pdf.ln(10)
        pdf.set_font("Arabic", size=12)
        pdf.set_text_color(0, 0, 102)
        pdf.cell(0, 10, ar("📝 ملاحظاتك الشخصية:"), ln=True)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arabic", size=11)
        pdf.multi_cell(0, 8, ar(notes))

    
    pdf.ln(10)
    pdf.set_font("Arabic", size=11)
    pdf.set_text_color(102, 0, 102)
    pdf.multi_cell(0, 8, ar(" النجاح لا يأتي صدفة، بل نتيجة للتدريب والمثابرة. "))

    pdf.ln(5)
    pdf.set_font("Arabic", size=10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, ar("📍 تقرير خاص - أُنشئ بواسطة منصة القدرات الذكية"), ln=True, align="C")

    
    file_name = f"{name.strip().replace(' ', '_')}_report.pdf"
    pdf.output(file_name)
    return file_name



found = False
old_scores = {}
if student_name:
    try:
        with open(f"student_{student_name.replace(' ', '_')}.json", "r", encoding="utf-8") as f:
            old_scores = json.load(f)["section_scores"]
            found = True
            st.success("✅ تم تحميل نتيجتك السابقة.")
    except:
        st.warning("⚠️ لم يتم العثور على نتيجتك السابقة.")


questions = {
    "النسب": [
        {"question": "زاد عدد بنسبة 20% ليصبح 120، ما العدد الأصلي؟", "options": ["100", "96", "110", "80"], "answer": "100"},
        {"question": "نسبة 8 إلى 12 هي نفسها نسبة؟", "options": ["2 إلى 3", "3 إلى 2", "1 إلى 2", "4 إلى 5"], "answer": "2 إلى 3"},
        {"question": "إذا كان س:ص = 2:5، والمجموع 49، كم س؟", "options": ["14", "21", "28", "35"], "answer": "14"},
    ],
    "الجبر": [
        {"question": "حل المعادلة: 3س - 2 = 10", "options": ["4", "6", "5", "3"], "answer": "4"},
        {"question": "س² - 16 = 0، فما س؟", "options": ["4", "-4", "±4", "8"], "answer": "±4"},
        {"question": "ما قيمة س: إذا 2(س + 3) = 14؟", "options": ["4", "5", "6", "3"], "answer": "4"},
    ],
    "الهندسة": [
        {"question": "مساحة مستطيل طوله 10 وعرضه 4؟", "options": ["40", "14", "28", "50"], "answer": "40"},
        {"question": "إذا نصف قطر دائرة 7 سم، ما المساحة؟ (π ≈ 3.14)", "options": ["153.86", "49", "100", "38.5"], "answer": "153.86"},
        {"question": "مجموع زوايا المثمن؟", "options": ["1080", "1260", "1440", "960"], "answer": "1080"},
    ],
}


user_answers = {}
start_times = {}
for section, qs in questions.items():
    st.subheader(f"📘 قسم: {section}")
    for i, q in enumerate(qs):
        key = f"{section}_{i}"
        start_times[key] = time.time()
        user_answers[q["question"]] = st.radio(q["question"], q["options"], key=key, index=None)
        st.markdown("---")


if st.button(" عرض النتيجة والتحليل"):
    end_times = {k: time.time() for k in start_times}
    durations = {k: round(end_times[k] - start_times[k], 1) for k in start_times}
    section_scores = {}
    timing_data = {}
    for section, qs in questions.items():
        correct = 0
        total_time = 0
        for i, q in enumerate(qs):
            key = f"{section}_{i}"
            if user_answers.get(q["question"]) == q["answer"]:
                correct += 1
            total_time += durations.get(key, 0)
        score = round((correct / len(qs)) * 100)
        section_scores[section] = score
        timing_data[section] = round(total_time, 1)

        st.markdown(f"🔹 **{section}**: {score}%")
        st.markdown(f"⏱️ الوقت المستغرق: {timing_data[section]} ثانية")

        if score < 50:
            st.error(f"{section}: مستواك ضعيف.")
            st.markdown(f" [شرح تأسيسي لقسم {section}](https://example.com/{section}_تأسيس)")
        elif score < 75:
            st.warning(f"{section}: مستواك متوسط.")
            st.markdown(f" [تمارين لقسم {section}](https://example.com/{section}_تمارين)")
        else:
            st.success(f"{section}: ممتاز! أداء عالي.")
            st.markdown(f"🔥 [تحدي قسم {section}](https://example.com/{section}_تحدي)")

    
    if found:
        before = [old_scores.get(s, 0) for s in section_scores]
        after = [section_scores[s] for s in section_scores]
        avg_before = sum(before) / len(before)
        avg_after = sum(after) / len(after)
        improvement = avg_after - avg_before

        
        x = np.arange(len(section_scores))
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(x - 0.2, before, width=0.4, label='قبل', color='gray')
        ax.bar(x + 0.2, after, width=0.4, label='بعد', color='green')
        ax.set_xticks(x)
        ax.set_xticklabels(section_scores.keys(), rotation=45)
        ax.set_title("📊 مقارنة الأداء قبل وبعد")
        ax.legend()
        fig.patch.set_alpha(0.0)
        st.pyplot(fig)

       
        excel_file = "all_results.xlsx"
        data = []
        for s in section_scores:
            data.append({
                "اسم الطالب": student_name,
                "القسم": s,
                "قبل الدورة": old_scores.get(s, 0),
                "بعد الدورة": section_scores[s],
                "المدة": timing_data[s],
                "ملاحظات": notes,
                "تاريخ": datetime.now().strftime("%Y-%m-%d %H:%M")
            })
        df_new = pd.DataFrame(data)
        if os.path.exists(excel_file):
            df_old = pd.read_excel(excel_file)
            df_old = df_old[df_old["اسم الطالب"] != student_name]
            df_all = pd.concat([df_old, df_new], ignore_index=True)
        else:
            df_all = df_new
        try:
            df_all.to_excel(excel_file, index=False)
            st.success("✅ تم حفظ النتائج.")
        except:
            st.error("⚠️ تأكد أن ملف Excel مغلق.")

        # توليد PDF
        pdf_file = generate_pdf(student_name, old_scores, section_scores, notes, avg_before, avg_after, improvement)
        with open(pdf_file, "rb") as f:
            st.download_button(" تحميل تقرير PDF", f, file_name=pdf_file, mime="application/pdf")
    else:
        st.warning("⚠️ لا توجد بيانات سابقة للمقارنة.")

# لوحة تحكم المعلم
st.markdown("---")
st.markdown("###  لوحة تحكم المعلم")
with st.expander("🔐 دخول المعلم"):
    admin_pass = st.text_input("كلمة المرور:", type="password")
    if admin_pass == "koon123":
        st.success("تم الدخول كمعلم.")
        if os.path.exists("all_results.xlsx"):
            df = pd.read_excel("all_results.xlsx")
            st.dataframe(df)
            name_filter = st.text_input("فلتر حسب الاسم:")
            if name_filter:
                st.dataframe(df[df["اسم الطالب"].str.contains(name_filter, case=False, na=False)])
    elif admin_pass:
        st.error("❌ كلمة المرور خاطئة.")
