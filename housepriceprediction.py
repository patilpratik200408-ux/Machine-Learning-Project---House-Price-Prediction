import streamlit as st
import pandas as pd
import pickle
import base64
import os


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Pune Property Valuation",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# LOAD MODEL
# =========================================================

@st.cache_resource
def load_model():

    with open("house_model.pkl", "rb") as f:
        model = pickle.load(f)

    with open("scaler.pkl", "rb") as f:
        scaler = pickle.load(f)

    return model, scaler


try:

    model, scaler = load_model()
    model_loaded = True

except Exception:

    model = None
    scaler = None
    model_loaded = False


# =========================================================
# FEATURES
# =========================================================

FEATURES = [
    "area_sqft",
    "bedrooms",
    "bathrooms",
    "age_years",
    "floor",
    "total_floors",
    "parking",

    "location_Aundh",
    "location_Baner",
    "location_Chinchwad",
    "location_Hadapsar",
    "location_Hinjewadi",
    "location_Kharadi",
    "location_Kondhwa",
    "location_Kothrud",
    "location_Pimpri",
    "location_Viman Nagar",
    "location_Wagholi",
    "location_Wakad",

    "property_type_Apartment",
    "property_type_Independent House",
    "property_type_Row House",
    "property_type_Villa",

    "furnishing_Fully Furnished",
    "furnishing_Semi-Furnished",
    "furnishing_Unfurnished"
]


locations = [
    "Aundh",
    "Baner",
    "Chinchwad",
    "Hadapsar",
    "Hinjewadi",
    "Kharadi",
    "Kondhwa",
    "Kothrud",
    "Pimpri",
    "Viman Nagar",
    "Wagholi",
    "Wakad"
]


property_types = [
    "Apartment",
    "Independent House",
    "Row House",
    "Villa"
]


furnishing_types = [
    "Fully Furnished",
    "Semi-Furnished",
    "Unfurnished"
]


# =========================================================
# PUNE BACKGROUND IMAGE
# =========================================================

if os.path.exists("pune.jpg"):

    with open("pune.jpg", "rb") as f:
        encoded_image = base64.b64encode(f.read()).decode()

    background_css = f"""
    .stApp {{
        background-image:
        linear-gradient(
            rgba(245, 250, 247, 0.25),
            rgba(245, 250, 247, 0.30)
        ),
        url("data:image/jpeg;base64,{encoded_image}");

        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    """

else:

    background_css = """
    .stApp {
        background:
        linear-gradient(
            135deg,
            #eef8f3,
            #f8faf9
        );
    }
    """


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    f"""
<style>

{background_css}


/* =====================================================
   MAIN PAGE
   ===================================================== */

.block-container {{
    max-width: 1000px;
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}}


/* =====================================================
   HERO
   ===================================================== */

.house-logo {{
    width: 68px;
    height: 68px;

    margin: 8px auto 12px;

    display: flex;
    align-items: center;
    justify-content: center;

    background: #123d30;

    border-radius: 19px;

    font-size: 34px;

    box-shadow:
        0 12px 30px rgba(18,61,48,0.25);
}}


.eyebrow {{
    text-align: center;

    color: #087f5b;

    font-size: 10px;

    font-weight: 850;

    letter-spacing: 2.8px;

    margin-bottom: 6px;
}}


.hero-title {{
    text-align: center;

    color: #102d24;

    font-size: 40px;

    font-weight: 900;

    letter-spacing: -1px;

    margin-bottom: 5px;
}}


.hero-subtitle {{
    text-align: center;

    color: #52665e;

    font-size: 13px;

    margin-bottom: 12px;
}}


.model-status {{
    width: fit-content;

    margin: 0 auto 20px;

    padding: 6px 15px;

    border-radius: 30px;

    background: rgba(236,253,245,0.96);

    border: 1px solid #a7f3d0;

    color: #047857;

    font-size: 10px;

    font-weight: 800;
}}


/* =====================================================
   MAIN CARD
   ===================================================== */

[data-testid="stVerticalBlockBorderWrapper"] {{
    border-radius: 22px !important;

    border: 1px solid rgba(210,225,217,0.95) !important;

    background: rgba(255,255,255,0.95) !important;

    box-shadow:
        0 20px 50px rgba(20,60,45,0.14) !important;

    backdrop-filter: blur(5px);
}}


/* =====================================================
   SECTION TITLE
   ===================================================== */

.section-title {{
    color: #173d30;

    font-size: 21px;

    font-weight: 850;

    margin-bottom: 3px;
}}


.section-description {{
    color: #71817b;

    font-size: 11px;

    margin-bottom: 17px;
}}


/* =====================================================
   LABELS
   ===================================================== */

div[data-testid="stWidgetLabel"] p {{
    color: #29463b !important;

    font-size: 12px !important;

    font-weight: 700 !important;
}}


/* =====================================================
   INPUTS
   ===================================================== */

div[data-baseweb="input"] {{
    background: #f9fbfa !important;

    border: 1px solid #d5e0da !important;

    border-radius: 10px !important;
}}


div[data-baseweb="input"]:focus-within {{
    border-color: #059669 !important;

    box-shadow:
        0 0 0 3px rgba(5,150,105,0.08);
}}


input {{
    color: #19382d !important;

    font-weight: 600 !important;
}}


/* =====================================================
   SELECTBOX
   ===================================================== */

div[data-baseweb="select"] > div {{
    background: #f9fbfa !important;

    border: 1px solid #d5e0da !important;

    border-radius: 10px !important;
}}


div[data-baseweb="select"] span {{
    color: #19382d !important;

    font-weight: 600 !important;
}}


/* =====================================================
   BUTTON
   ===================================================== */

div.stButton > button {{

    width: 100%;

    height: 52px;

    margin-top: 12px;

    border: none;

    border-radius: 11px;

    background:
        linear-gradient(
            90deg,
            #087f5b,
            #0b9b70
        );

    color: white !important;

    font-size: 14px;

    font-weight: 850;

    box-shadow:
        0 9px 22px rgba(8,127,91,0.23);

    transition: all 0.2s ease;
}}


div.stButton > button:hover {{

    transform: translateY(-2px);

    background:
        linear-gradient(
            90deg,
            #066b4c,
            #087f5b
        );

    box-shadow:
        0 13px 27px rgba(8,127,91,0.30);
}}


div.stButton > button p {{
    color: white !important;

    font-weight: 850 !important;
}}


/* =====================================================
   RESULT HEADING
   ===================================================== */

.result-heading {{
    text-align: center;

    color: #71817b;

    font-size: 9px;

    font-weight: 850;

    letter-spacing: 2.5px;

    margin-top: 22px;

    margin-bottom: 7px;
}}


/* =====================================================
   RESULT CARD
   ===================================================== */

div[data-testid="stMetric"] {{

    background:
        linear-gradient(
            135deg,
            #103b2e,
            #174f3e
        );

    padding: 24px;

    border-radius: 19px;

    border: 1px solid #245d4b;

    box-shadow:
        0 18px 38px rgba(18,61,48,0.25);
}}


div[data-testid="stMetricLabel"] p {{

    color: #a7f3d0 !important;

    font-size: 10px !important;

    font-weight: 800 !important;

    letter-spacing: 1.5px;
}}


div[data-testid="stMetricValue"] {{

    color: white !important;

    font-size: 35px !important;

    font-weight: 900 !important;
}}


/* =====================================================
   FOOTER
   ===================================================== */

.footer {{
    text-align: center;

    color: #91a19a;

    font-size: 10px;

    margin-top: 20px;
}}


/* =====================================================
   MOBILE
   ===================================================== */

@media(max-width: 700px) {{

    .block-container {{
        padding-top: 1rem;
    }}

    .hero-title {{
        font-size: 31px;
    }}

    .hero-subtitle {{
        font-size: 12px;
    }}

    div[data-testid="stMetricValue"] {{
        font-size: 28px !important;
    }}

}}

</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# HERO
# =========================================================

st.markdown(
    '<div class="house-logo">🏠</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="eyebrow">REAL ESTATE • MACHINE LEARNING</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero-title">Pune Property Valuation</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero-subtitle">Estimate the value of a property using location, size, amenities and property characteristics.</div>',
    unsafe_allow_html=True
)


# =========================================================
# MODEL STATUS
# =========================================================

if model_loaded:

    st.markdown(
        '<div class="model-status">● Gradient Boosting Model Ready</div>',
        unsafe_allow_html=True
    )

else:

    st.error(
        "Model files could not be loaded. "
        "Keep house_model.pkl and scaler.pkl in the same folder."
    )


# =========================================================
# PROPERTY INFORMATION
# =========================================================

with st.container(border=True):

    st.markdown(
        '<div class="section-title">🏡 Property Information</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">Enter the property details below to generate an estimated valuation.</div>',
        unsafe_allow_html=True
    )


    col1, col2 = st.columns(2, gap="large")


    # =====================================================
    # LEFT COLUMN
    # =====================================================

    with col1:

        location = st.selectbox(
            "📍 Location",
            locations
        )

        property_type = st.selectbox(
            "🏠 Property Type",
            property_types
        )

        area_sqft = st.number_input(
            "📐 Area (sq.ft.)",
            min_value=100.0,
            max_value=20000.0,
            value=1000.0,
            step=50.0
        )

        bedrooms = st.number_input(
            "🛏️ Bedrooms",
            min_value=1,
            max_value=20,
            value=2,
            step=1
        )

        bathrooms = st.number_input(
            "🚿 Bathrooms",
            min_value=1,
            max_value=20,
            value=2,
            step=1
        )


    # =====================================================
    # RIGHT COLUMN
    # =====================================================

    with col2:

        furnishing = st.selectbox(
            "🛋️ Furnishing",
            furnishing_types
        )

        age_years = st.number_input(
            "📅 Property Age (Years)",
            min_value=0,
            max_value=100,
            value=5,
            step=1
        )

        floor = st.number_input(
            "🏢 Floor",
            min_value=0,
            max_value=100,
            value=2,
            step=1
        )

        total_floors = st.number_input(
            "🏙️ Total Floors",
            min_value=1,
            max_value=100,
            value=5,
            step=1
        )

        parking = st.number_input(
            "🚗 Parking Spaces",
            min_value=0,
            max_value=10,
            value=1,
            step=1
        )


    # =====================================================
    # BUTTON
    # =====================================================

    predict_button = st.button(
        "✨ Estimate Property Value"
    )


# =========================================================
# PREDICTION
# =========================================================

if predict_button and model_loaded:

    if floor > total_floors:

        st.warning(
            "⚠️ Floor cannot be greater than total floors."
        )

    else:

        try:

            # -------------------------------------------------
            # CREATE INPUT DICTIONARY
            # -------------------------------------------------

            input_data = {
                feature: 0
                for feature in FEATURES
            }


            # -------------------------------------------------
            # NUMERICAL FEATURES
            # -------------------------------------------------

            input_data["area_sqft"] = area_sqft
            input_data["bedrooms"] = bedrooms
            input_data["bathrooms"] = bathrooms
            input_data["age_years"] = age_years
            input_data["floor"] = floor
            input_data["total_floors"] = total_floors
            input_data["parking"] = parking


            # -------------------------------------------------
            # ONE-HOT ENCODING
            # -------------------------------------------------

            input_data[f"location_{location}"] = 1

            input_data[f"property_type_{property_type}"] = 1

            input_data[f"furnishing_{furnishing}"] = 1


            # -------------------------------------------------
            # DATAFRAME
            # -------------------------------------------------

            input_df = pd.DataFrame(
                [input_data],
                columns=FEATURES
            )


            # -------------------------------------------------
            # SCALING
            # -------------------------------------------------

            input_scaled = scaler.transform(
                input_df
            )


            # -------------------------------------------------
            # PREDICTION
            # -------------------------------------------------

            prediction = float(
                model.predict(input_scaled)[0]
            )


            # =================================================
            # RESULT
            # =================================================

            st.markdown(
                '<div class="result-heading">PROPERTY VALUATION RESULT</div>',
                unsafe_allow_html=True
            )


            st.metric(
                label="🏠 Estimated Property Price",
                value=f"₹ {prediction:,.2f} Lakhs"
            )


            # =================================================
            # PROPERTY SUMMARY
            # Native Streamlit - NO HTML
            # =================================================

            st.markdown("")

            s1, s2, s3, s4 = st.columns(4)

            with s1:

                st.caption("📍 Location")
                st.write(location)

            with s2:

                st.caption("🏠 Property")
                st.write(property_type)

            with s3:

                st.caption("📐 Area")
                st.write(f"{area_sqft:,.0f} sq.ft.")

            with s4:

                st.caption("🛏️ Bedrooms")
                st.write(f"{bedrooms} BHK")


        except Exception as e:

            st.error(
                "Prediction failed. Please check that "
                "the model, scaler and feature order "
                "match the training pipeline."
            )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    '<div class="footer" style="text-align: center; padding: 20px; background-color: #f0f0f0; border-top: 1px solid #ddd;">Built with ❤️ using Python • Streamlit • Gradient Boosting</div>',
    unsafe_allow_html=True
)