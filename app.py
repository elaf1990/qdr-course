import streamlit as st
st.set_page_config(page_title="اختبار تحديد مستوى القدرات - كمي", layout="centered")
st.title(" اختبار تحديد مستوى القدرات - كمي")
import matplotlib.pyplot as plt
import json
from datetime import datetime
from fpdf import FPDF



PASSWORD = "qdr2025"  


password = st.text_input("أدخل كلمة المرور للدخول إلى الاختبار", type="password")

if password != PASSWORD:
    st.warning("كلمة المرور غير صحيحة أو لم تُدخل بعد.")
    st.stop()  


st.set_page_config(page_title="اختبار تحديد مستوى القدرات - كمي", layout="centered")
st.title(" اختبار تحديد مستوى القدرات - كمي")

# إدخال اسم الطالب
student_name = st.text_input("👤 أدخل اسمك الكامل (مطلوب لحفظ نتيجتك):")

questions = {
    "النسب": [
        {"question": "إذا كانت النسبة بين س وص هي 2:3، وكان س = 4، فما قيمة ص؟", "options": ["6", "3", "8", "5"], "answer": "6"},
        {"question": "إذا كانت النسبة بين أ إلى ب هي 5:2، وب = 8، فما قيمة أ؟", "options": ["20", "16", "10", "12"], "answer": "20"},
        {"question": "نسبة النجاح 80% من 250 طالب، كم عدد الناجحين؟", "options": ["200", "180", "220", "210"], "answer": "200"},
        {"question": "إذا كان ثمن سلعة بعد الخصم 75 ريال، والخصم 25%، فما الثمن الأصلي؟", "options": ["100", "95", "90", "110"], "answer": "100"},
        {"question": "إذا كان س:ص = 4:7، وس + ص = 66، فما قيمة س؟", "options": ["24", "28", "30", "22"], "answer": "24"},
    ],
    "الجبر": [
        {"question": "إذا كان 3س = 12، فما قيمة س؟", "options": ["4", "3", "5", "6"], "answer": "4"},
        {"question": "حل المعادلة: س + 5 = 9", "options": ["4", "5", "6", "3"], "answer": "4"},
        {"question": "إذا كان 2س - 3 = 7، فما قيمة س؟", "options": ["5", "4", "6", "3"], "answer": "5"},
        {"question": "إذا كان س² = 36، فما قيمة س؟ (الموجب فقط)", "options": ["6", "5", "4", "3"], "answer": "6"},
        {"question": "إذا كان (س + 2)(س - 3) = 0، فما أحد حلول س؟", "options": ["3", "-2", "0", "1"], "answer": "3"},
    ],
    "الهندسة": [
        {"question": "محيط مربع طول ضلعه 5 سم، ما المحيط؟", "options": ["20", "25", "15", "10"], "answer": "20"},
        {"question": "مساحة دائرة نصف قطرها 7 سم تقريبًا؟ (π ≈ 3.14)", "options": ["153.86", "49", "44", "38.5"], "answer": "153.86"},
        {"question": "زاوية قائمة قياسها؟", "options": ["90", "45", "60", "180"], "answer": "90"},
        {"question": "مجموع زوايا مثلث؟", "options": ["180", "90", "360", "270"], "answer": "180"},
        {"question": "إذا كان المستطيل طوله 8 وعرضه 3، فما مساحته؟", "options": ["24", "22", "11", "18"], "answer": "24"},
    ],
    "التحليل": [
        {"question": "إذا كان المتوسط الحسابي لـ (4, 6, 8)؟", "options": ["6", "5", "7", "8"], "answer": "6"},
        {"question": "إذا كان المدى بين 2 و 10؟", "options": ["8", "12", "5", "6"], "answer": "8"},
        {"question": "ما الوسيط في الأعداد (3, 7, 9)؟", "options": ["7", "6", "9", "3"], "answer": "7"},
        {"question": "إذا كانت البيانات 5, 10, 15, 20، المتوسط؟", "options": ["12.5", "10", "15", "17.5"], "answer": "12.5"},
        {"question": "ما الفرق بين القيمة العظمى والصغرى؟", "options": ["النطاق", "الوسيط", "المتوسط", "المدى"], "answer": "المدى"},
    ],
    "الاحتمالات": [
        {"question": "احتمال ظهور وجه معين في رمية نرد عادلة؟", "options": ["1/6", "1/4", "1/2", "1/3"], "answer": "1/6"},
        {"question": "احتمال سحب ورقة قلب من أوراق اللعب (52 ورقة)؟", "options": ["1/4", "1/2", "1/3", "1/13"], "answer": "1/4"},
        {"question": "إذا كانت احتمال نجاح اختبار 0.7، احتمال الفشل؟", "options": ["0.3", "0.7", "0.5", "0.2"], "answer": "0.3"},
        {"question": "احتمال الحصول على عدد زوجي في رمية نرد؟", "options": ["1/2", "1/3", "1/4", "2/3"], "answer": "1/2"},
        {"question": "احتمال سحب بطاقة حمراء من أوراق اللعب؟", "options": ["1/2", "1/4", "1/3", "1/5"], "answer": "1/2"},
    ],
    "المتتاليات": [
        {"question": "المصطلح الخامس في المتتالية 2، 4، 6، 8، ...؟", "options": ["10", "12", "14", "8"], "answer": "10"},
        {"question": "المصطلح الثالث في متتالية 3، 6، 9، 12، ...؟", "options": ["9", "6", "12", "15"], "answer": "9"},
        {"question": "المصطلح الأول في متتالية 5، 10، 15، ...؟", "options": ["5", "10", "15", "20"], "answer": "5"},
        {"question": "المصطلح السابع في 1، 3، 5، 7، ...؟", "options": ["13", "15", "17", "19"], "answer": "13"},
        {"question": "المصطلح الرابع في 10، 20، 30، 40، ...؟", "options": ["40", "30", "20", "50"], "answer": "40"},
    ],
}

section_colors = {
    "النسب": "#3498db",
    "الجبر": "#e67e22",
    "الهندسة": "#2ecc71",
    "التحليل": "#9b59b6",
    "الاحتمالات": "#f1c40f",
    "المتتاليات": "#e74c3c",
}

user_answers = {}
st.markdown("###  الأسئلة")
for section, qs in questions.items():
    st.subheader(f"📘 قسم: {section}")
    for i, q in enumerate(qs):
        user_answers[q["question"]] = st.radio(q["question"], q["options"], key=f"q_{section}_{i}", index=None)

if st.button(" عرض النتيجة والتحليل"):
    section_scores = {}
    for section, qs in questions.items():
        correct = sum(user_answers.get(q["question"]) == q["answer"] for q in qs)
        score = round((correct / len(qs)) * 100) if len(qs) > 0 else 0
        section_scores[section] = score
        st.markdown(f"📌 نتيجتك في قسم **{section}**: {score}%")

    labels = list(section_scores.keys())
    values = list(section_scores.values())
    colors = [section_colors.get(s, "#95a5a6") for s in labels]

    if all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in values) and sum(values) > 0:
        st.markdown("###  توزيع مستواك بالرسم البياني:")
        fig, ax = plt.subplots(figsize=(6, 6), facecolor='none')
        wedges, texts, autotexts = ax.pie(
            values,
            labels=labels,
            colors=colors,
            startangle=90,
            autopct="%1.0f%%",
            wedgeprops={'linewidth': 1, 'edgecolor': 'white'},
            textprops={'color': "black", 'fontsize': 10}
        )
        ax.axis("equal")
        fig.patch.set_alpha(0.0)
        st.pyplot(fig)
    else:
        st.warning("⚠️ لم يتم إدخال نتائج كافية لرسم الرسم البياني. تأكد من الإجابة على بعض الأسئلة أولًا.")

    # تحليل المستويات
    weak = [s for s, v in section_scores.items() if v < 50]
    medium = [s for s, v in section_scores.items() if 50 <= v < 75]
    strong = [s for s, v in section_scores.items() if v >= 75]

    st.markdown("###  التحليل النهائي لمستواك:")

    if not any([weak, medium, strong]):
        st.info("❗ لم يتم الإجابة على أي سؤال.")
    else:
        if weak:
            st.error("❗ الأقسام الضعيفة:\n" + "\n".join(
                f"- {s}:  مستواك ضعيف في هذا القسم، أنصحك تبدأ بمقاطع التأسيس والمفاهيم الأساسية." for s in weak
            ))
        if medium:
            st.warning("⚠️ الأقسام التي تحتاج تطوير:\n" + "\n".join(
                f"- {s}: تحتاج تطوير بسيط، جرب تراجع طرق الحل السريع وتدرب أكثر على الأسئلة." for s in medium
            ))
        if strong:
            st.success("✅ الأقسام القوية لديك:\n" + "\n".join(
                f"- {s}: مبروك يا وحش! أداؤك ممتاز، استمر بالتدرب لاحتراف القدرات." for s in strong
            ))

    # ✅ حفظ النتيجة في ملف JSON
    if student_name:
        result = {
            "name": student_name,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "section_scores": section_scores
        }
        file_name = f"student_{student_name.strip().replace(' ', '_')}.json"
        with open(file_name, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
        st.success(f"✅ تم حفظ نتيجتك في الملف: {file_name}")
    else:
        st.warning("⚠️ لم يتم حفظ النتيجة. الرجاء إدخال اسمك بالأعلى.")
