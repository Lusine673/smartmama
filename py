import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import base64

# =============================
# SmartMama: Ваш личный диет-ассистент при беременности
# =============================

st.set_page_config(page_title="SmartMama", page_icon="🤰", layout="centered")
st.title("🤰 SmartMama: ваш личный диет-ассистент при беременности")
st.markdown("Отслеживайте прибавку веса и получайте персонализированные рекомендации по питанию")

# --- Нормы прибавки по ИМТ ---
norms = {
    "ИМТ < 18.5": {"total_kg": "12.5–18", "weekly_kg": (0.44, 0.58)},
    "ИМТ 18.5–24.9": {"total_kg": "11.5–16", "weekly_kg": (0.35, 0.50)},
    "ИМТ 25.0–29.9": {"total_kg": "7–11", "weekly_kg": (0.23, 0.33)},
    "ИМТ ≥ 30.0": {"total_kg": "5–9", "weekly_kg": (0.17, 0.27)}
}

# --- Меню на 3 дня (низкоГИ, высокобелковое) ---
sample_menus = [
    """
    🍽️ *Меню на день 1*
    Завтрак: Омлет из 2 яиц с шпинатом + гречневая каша (50 г сух.) + зелёный чай
    Перекус: Натуральный йогурт 200 мл + горсть черники
    Обед: Куриная грудка на пару (120 г) + брокколи/цветная капуста (150 г) + киноа (40 г сух.)
    Перекус: Творог 5% (100 г) + 1 ст.л. льняного семени
    Ужин: Запечённая треска (100 г) + салат из огурцов, помидоров, зелени с 1 ч.л. оливкового масла
    Перед сном: Стакан кефира 1% (200 мл)
    """,
    """
    🍽️ *Меню на день 2*
    Завтрак: Творожная запеканка (творог 150 г, яйцо, яблоко) + чай без сахара
    Перекус: Горсть миндаля (20 г) + яблоко
    Обед: Индейка отварная (100 г) + тушеные кабачки и морковь (200 г) + бурый рис (40 г сух.)
    Перекус: Протеиновый коктейль на воде или кефире (без сахара)
    Ужин: Запечённые овощи (баклажан, цуккини, перец) с фетой (30 г)
    Перед сном: Ряженка 2.5% (200 мл)
    """,
    """
    🍽️ *Меню на день 3*
    Завтрак: Овсянка на воде (40 г сух.) с тыквой и корицей + 1 варёное яйцо
    Перекус: Кефир 1% (200 мл) + 1 груша
    Обед: Говядина тушёная (100 г) + стручковая фасоль (150 г) + гречка (40 г сух.)
    Перекус: Смузи: шпинат, огурец, сельдерей, лимонный сок, вода
    Ужин: Лосось на пару (100 г) + салат из рукколы, авокадо, оливковое масло
    Перед сном: Натуральный йогурт (150 мл)
    """
]

# --- Интерфейс ввода ---
st.header("📝 Введите ваши данные")

col1, col2 = st.columns(2)

with col1:
    weight_before = st.number_input("Вес до беременности (кг)", min_value=30.0, max_value=150.0, value=60.0, step=0.1)
    height = st.number_input("Рост (см)", min_value=120, max_value=220, value=165, step=1)

with col2:
    current_weight = st.number_input("Текущий вес (кг)", min_value=30.0, max_value=200.0, value=65.0, step=0.1)
    gest_weeks = st.number_input("Срок беременности (недель)", min_value=1, max_value=42, value=12, step=1)

# --- Расчёт ИМТ ---
bmi = weight_before / ((height / 100) ** 2)
if bmi < 18.5:
    bmi_category = "ИМТ < 18.5"
elif 18.5 <= bmi < 25:
    bmi_category = "ИМТ 18.5–24.9"
elif 25 <= bmi < 30:
    bmi_category = "ИМТ 25.0–29.9"
else:
    bmi_category = "ИМТ ≥ 30.0"

st.info(f"🔹 Ваш ИМТ до беременности: **{bmi:.1f}** → категория: **{bmi_category}**")

# --- Предыдущий вес (опционально) ---
prev_weight = st.number_input("Предыдущий вес (кг, опционально)", min_value=30.0, max_value=200.0, value=0.0, step=0.1, help="Оставьте 0, если это первое измерение")
prev_weeks = st.number_input("Срок на момент предыдущего взвешивания (недель, опционально)", min_value=1, max_value=42, value=gest_weeks-1 if prev_weight > 0 else 1, step=1)

# --- Расчёт прибавки ---
if prev_weight > 0 and prev_weeks < gest_weeks:
    weeks_passed = gest_weeks - prev_weeks
    weight_gain = current_weight - prev_weight
    weekly_gain = weight_gain / weeks_passed if weeks_passed > 0 else 0

    st.subheader("📊 Анализ прибавки веса")
    st.write(f"🔸 Прибавка за {weeks_passed} нед.: **{weight_gain:.2f} кг**")
    st.write(f"🔸 Средняя прибавка в неделю: **{weekly_gain:.2f} кг/нед**")

    # Получаем норму
    min_norm, max_norm = norms[bmi_category]["weekly_kg"]

    if weekly_gain > max_norm:
        st.error(f"⚠️ Прибавка выше нормы ({max_norm} кг/нед)! Рекомендуем скорректировать питание.")
        # Генерируем случайное меню
        import random
        menu_text = random.choice(sample_menus)
        st.markdown("### 📋 Ваше персонализированное меню на день:")
        st.text(menu_text)

        # Функция для создания PDF
        def create_pdf(menu):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="SmartMama: Ваше персонализированное меню", ln=True, align='C')
            pdf.ln(10)
            pdf.multi_cell(0, 10, txt=menu)
            return pdf.output(dest='S').encode('latin1')

        pdf_bytes = create_pdf(menu_text)
        b64 = base64.b64encode(pdf_bytes).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="SmartMama_меню.pdf">📥 Скачать меню в PDF</a>'
        st.markdown(href, unsafe_allow_html=True)

    elif weekly_gain < min_norm:
        st.warning(f"🔸 Прибавка ниже нормы ({min_norm} кг/нед). Убедитесь, что питаетесь достаточно!")
    else:
        st.success(f"✅ Прибавка в пределах нормы ({min_norm}–{max_norm} кг/нед). Отличная работа!")

else:
    st.info("ℹ️ Введите предыдущий вес и срок, чтобы рассчитать динамику прибавки.")

# --- Информация о нормах ---
st.header("📚 Рекомендуемые нормы прибавки веса")
df_norms = pd.DataFrame({
    "Категория ИМТ": list(norms.keys()),
    "За всю беременность (кг)": [v["total_kg"] for v in norms.values()],
    "Еженедельно (кг/нед)": [f"{v['weekly_kg'][0]}–{v['weekly_kg'][1]}" for v in norms.values()]
})
st.table(df_norms)

st.markdown("""
---
💡 **Рекомендации:**
- Ограничьте быстрые углеводы: сладости, белый хлеб, картофель, газировку.
- Ешьте больше овощей, нежирного мяса, рыбы, бобовых, цельнозерновых.
- Пейте воду 
