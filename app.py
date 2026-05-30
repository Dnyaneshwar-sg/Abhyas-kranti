import streamlit as st
from supabase import create_client, Client
import pandas as pd
import requests
import json

# --- १. Secrets मधून सुपाबेसच्या चाव्या लोड करणे ---
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    st.error("कृपया Streamlit Secrets मध्ये SUPABASE_URL आणि SUPABASE_KEY SET करा.")

# --- २. पेज कॉन्फिगरेशन ---
st.set_page_config(
    page_title="Abhyas Kranti Ultimate Portal - IIT Patna Capstone",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ३. ग्लोबल भाषा आणि राज्य मॅपिंग (सर्व ९ भाषा) ---
languages_map = {
    "मराठी (Marathi) - महाराष्ट्र": "Marathi",
    "English - Pan India": "English",
    "हिंदी (Hindi) - उत्तर प्रदेश / बिहार / दिल्ली": "Hindi",
    "Gujarati (ગુજરાતી) - ગુજરાત": "Gujarati",
    "Kannada (ಕನ್ನಡ) - ಕರ್ನಾಟಕ": "Kannada",
    "Tamil (தமிழ்) - தமிழ்நாடு": "Tamil",
    "Telugu (తెలుగు) - ఆంధ్రప్రదేశ్ / తెలంగాణ": "Telugu",
    "Punjabi (ਪੰਜਾਬੀ) - ਪੰਜਾਬ": "Punjabi",
    "Bengali (বাংলা) - পশ্চিমবঙ্গ": "Bengali"
}

# --- ४. महा-डायनॅमिक इंटरफेस ट्रान्सलेशन मॅट्रिक्स (९ प्रादेशिक भाषांचा महासंग्रह) ---
UI_LANG_MATRIX = {
    "Marathi": {
        "menu_lbl": "🌍 भाषा व राज्य निवडा (Select Language):",
        "dash_menu": "🏠 मुख्य पान (Dashboard)",
        "sandbox_menu": "⚡ ६-इन-१ AI सँडबॉक्स",
        "doubt_menu": "🧠 शंका निरसन केंद्र",
        "login_menu": "🔐 लॉगिन / प्रोफाईल",
        "tabs": ["🧠 शंका निरसन शिक्षक", "📅 अभ्यास वेळापत्रक", "🛡️ स्कॉलरशिप इंजिन", "🎯 परीक्षा केंद्र", "🏢 करिअर मार्गदर्शक", "🌐 भाषा केंद्र"],
        "q1_lbl": "तुमचा शैक्षणिक प्रश्न विचारा:",
        "btn1_lbl": "🚀 शंका निरसन करा",
        "q2_lbl": "कोणत्या परीक्षेची तयारी करत आहात?",
        "s2_lbl": "रोज अभ्यासासाठी किती तास उपलब्ध आहेत?",
        "btn2_lbl": "🚀 स्मार्ट वेळापत्रक तयार करा",
        "sel3_lbl": "विद्यार्थ्याची शैक्षणिक पातळी / इयत्ता निवडा:",
        "edu_opts": ["इयत्ता १ ली ते ४ थी (प्राथमिक शाळा)", "इयत्ता ५ वी ते ७ वी (उच्च प्राथमिक)", "इयत्ता ८ वी ते १० वी (SSC)", "इयत्ता ११ वी आणि १२ वी (HSC)", "पदवी शिक्षण (Undergraduate)", "पदव्युत्तर शिक्षण (Postgraduate)", "पीएच.डी. आणि उच्च संशोधन"],
        "inc3_lbl": "कौटुंबिक वार्षिक उत्पन्न निवडा:",
        "inc_opts": ["₹१.५ लाखांपेक्षा कमी", "₹१.५ लाख ते ₹३ लाख", "₹३ लाख ते ₹८ लाख", "₹८ लाखांपेक्षा जास्त"],
        "cat3_lbl": "प्रवर्ग / जात / आरक्षित श्रेणी (Open, OBC, SC, ST):",
        "btn3_lbl": "🚀 पात्र स्कॉलरशिप शोधा",
        "sel4_lbl": "परीक्षेची पातळी निवडा:",
        "exam_tiers": ["राज्याची राज्य पातळीवरील परीक्षा (State PSC)", "राष्ट्रीय पातळीवरील परीक्षा (UPSC, NEET, JEE, NDA)", "जागतिक /ूरराष्ट्रीय परीक्षा (GRE, IELTS)"],
        "txt4_lbl": "थेट परीक्षेचे नाव टाईप करा:",
        "btn4_lbl": "🚀 परीक्षा पॅटर्न व नमुना प्रश्न मिळवा",
        "sel5_lbl": "विद्याशाखा / प्रवाह निवडा:",
        "streams": ["कला शाखा (Arts)", "वाणिज्य शाखा (Commerce)", "विज्ञान शाखा (Pure Sciences)", "तांत्रिक व मेडिकल", "व्यावसायिक व कौशल्य विकास (Vocational/Solar)"],
        "rad5_lbl": "करिअरची व्याप्ती (Scope):",
        "scopes": ["स्थानिक आणि राष्ट्रीय संधी", "जागतिक संधी (Global & International)"],
        "txt5_lbl": "विद्यार्थ्याची वैयक्तिक आवड (उदा. डेटा सायन्स, सोलर बिझनेस):",
        "btn5_lbl": "🚀 करिअर रोडमॅप व लिंक्स मिळवा"
    },
    "English": {
        "menu_lbl": "🌍 Select Language & State:",
        "dash_menu": "🏠 Main Dashboard",
        "sandbox_menu": "⚡ 6-in-1 AI Sandbox",
        "doubt_menu": "🧠 Doubt Solver",
        "login_menu": "🔐 Login / Profile",
        "tabs": ["🧠 Doubt Solver", "📅 Study Planner", "🛡️ Scholarship Engine", "🎯 Exam Center", "🏢 Career Guide", "🌐 Language Hub"],
        "q1_lbl": "Ask your academic question here:",
        "btn1_lbl": "🚀 Solve My Doubt",
        "q2_lbl": "Which exam are you preparing for?",
        "s2_lbl": "How many hours can you study daily?",
        "btn2_lbl": "🚀 Create Smart Schedule",
        "sel3_lbl": "Select Educational Level / Grade:",
        "edu_opts": ["1st - 4th Grade", "5th - 7th Grade", "8th - 10th Grade (SSC)", "11th & 12th Grade (HSC)", "Undergraduate", "Postgraduate", "Ph.D. Research"],
        "inc3_lbl": "Select Annual Family Income:",
        "inc_opts": ["Below ₹1.5 Lakhs", "₹1.5 Lakhs to ₹3 Lakhs", "₹3 Lakhs to ₹8 Lakhs", "Above ₹8 Lakhs"],
        "cat3_lbl": "Type Category / Reservation (Open, OBC, SC, ST):",
        "btn3_lbl": "🚀 Find Eligible Scholarships",
        "sel4_lbl": "Select Examination Tier:",
        "exam_tiers": ["State Level Exams (PSC)", "National Level Exams (UPSC, NEET, JEE)", "Global Exams (GRE, IELTS)"],
        "txt4_lbl": "Type Target Exam Name:",
        "btn4_lbl": "🚀 Get Pattern & Sample Questions",
        "sel5_lbl": "Select Academic Stream:",
        "streams": ["Arts & Humanities", "Commerce & Management", "Pure & Applied Sciences", "Technical & Medical", "Vocational & Skills (Solar, Agri)"],
        "rad5_lbl": "Career Scope Level:",
        "scopes": ["Local & National Opportunities", "Global Opportunities"],
        "txt5_lbl": "Your Core Area of Interest (e.g., Solar, Data Science):",
        "btn5_lbl": "🚀 Generate Career Roadmap & Links"
    },
    "Hindi": {
        "menu_lbl": "🌍 भाषा और राज्य चुनें:",
        "dash_menu": "🏠 मुख्य डैशबोर्ड",
        "sandbox_menu": "⚡ 6-इन-1 AI सैंडबॉक्स",
        "doubt_menu": "🧠 शंका समाधान केंद्र",
        "login_menu": "🔐 लॉगिन / प्रोफाइल",
        "tabs": ["🧠 शंका समाधान", "📅 समय-सारणी", "🛡️ स्कॉलरशिप इंजन", "🎯 परीक्षा केंद्र", "🏢关रियर मार्गदर्शक", "🌐 भाषा केंद्र"],
        "q1_lbl": "अपना शैक्षणिक प्रश्न पूछें:",
        "btn1_lbl": "🚀 शंका समाधान करें",
        "q2_lbl": "आप किस परीक्षा की तैयारी कर रहे हैं?",
        "s2_lbl": "रोजाना पढ़ाई के लिए कितने घंटे उपलब्ध हैं?",
        "btn2_lbl": "🚀 स्मार्ट समय-सारणी बनाएं",
        "sel3_lbl": "शैक्षणिक स्तर / कक्षा चुनें:",
        "edu_opts": ["कक्षा 1 से 4", "कक्षा 5 से 7", "कक्षा 8 से 10 (SSC)", "कक्षा 11 और 12 (HSC)", "स्नातक (Undergraduate)", "स्नातकोत्तर (Postgraduate)", "पीएच.डी. अनुसंधान"],
        "inc3_lbl": "वार्षिक पारिवारिक आय चुनें:",
        "inc_opts": ["₹1.5 लाख से कम", "₹1.5 लाख से ₹3 लाख", "₹3 लाख से ₹8 लाख", "₹8 लाख से अधिक"],
        "cat3_lbl": "अपनी श्रेणी / जाति (Open, OBC, SC, ST):",
        "btn3_lbl": "🚀 योग्य स्कॉलरशिप खोजें",
        "sel4_lbl": "परीक्षा का स्तर चुनें:",
        "exam_tiers": ["राज्य स्तरीय परीक्षा (State PSC)", "राष्ट्रीय स्तरीय परीक्षा (UPSC, NEET, JEE)", "वैश्विक परीक्षा (GRE, IELTS)"],
        "txt4_lbl": "परीक्षा का नाम टाइप करें:",
        "btn4_lbl": "🚀 परीक्षा पैटर्न और प्रश्न प्राप्त करें",
        "sel5_lbl": "शैक्षणिक स्ट्रीम/शाखा चुनें:",
        "streams": ["कला शाखा (Arts)", "वाणिज्य शाखा (Commerce)", "विज्ञान शाखा (Pure Sciences)", "तकनीकी और मेडिकल", "व्यावसायिक और कौशल (Vocational/Solar)"],
        "rad5_lbl": "करियर का दायरा:",
        "scopes": ["स्थानीय और राष्ट्रीय अवसर", "वैश्विक अवसर"],
        "txt5_lbl": "अपनी व्यक्तिगत रुचि (जैसे सोलर, डेटा साइंस):",
        "btn5_lbl": "🚀 करियर रोडमॅप और लिंक्स प्राप्त करें"
    },
    "Gujarati": {
        "menu_lbl": "🌍 ભાષા અને રાજ્ય પસંદ કરો:",
        "dash_menu": "🏠 મુખ્ય પૃષ્ઠ (Dashboard)",
        "sandbox_menu": "⚡ 6-ઇન-1 AI સેન્ડબોક્સ",
        "doubt_menu": "🧠 શંકા નિવારણ કેન્દ્ર",
        "login_menu": "🔐 લોગિન / પ્રોફાઇલ",
        "tabs": ["🧠 શંકા નિવારણ શિક્ષક", "📅 અભ્યાસ સમયપત્રક", "🛡️ સ્કોલરશિપ એન્જિન", "🎯 પરીક્ષા કેન્દ્ર", "🏢 કરિયર માર્ગદર્શક", "🌐 ભાષા કેન્દ્ર"],
        "q1_lbl": "તમારો શૈક્ષણિક પ્રશ્ન અહીં પૂછો:",
        "btn1_lbl": "🚀 શંકાનું સમાધાન કરો",
        "q2_lbl": "તમે કઈ પરીક્ષાની તૈયારી કરી રહ્યા છો?",
        "s2_lbl": "રોજ અભ્યાસ માટે કેટલા કલાક ઉપલબ્ધ છે?",
        "btn2_lbl": "🚀 સ્માર્ટ સમયપત્રક બનાવો",
        "sel3_lbl": "વિદ્યાર્થીનું શૈક્ષણિક સ્તર પસંદ કરો:",
        "edu_opts": ["ધોરણ 1 થી 4 (પ્રાથમિક)", "ધોરણ 5 થી 7 (ઉચ્ચ પ્રાથમિક)", "ધોરણ 8 થી 10 (SSC)", "ધોરણ 11 અને 12 (HSC)", "સ્નાતક (Undergraduate)", "અનુસ્નાતક (Postgraduate)", "પીએચ.ડી. અને સંશોધન"],
        "inc3_lbl": "કૌટુંબિક વાર્ષિક આવક પસંદ કરો:",
        "inc_opts": ["₹1.5 લાખથી ઓછી", "₹1.5 લાખથી ₹3 લાખ", "₹3 લાખથી ₹8 લાખ", "₹8 લાખથી વધુ"],
        "cat3_lbl": "કેટેગરી / જાતિ ટાઈપ કરો (Open, OBC, SC, ST):",
        "btn3_lbl": "🚀 યોગ્ય સ્કોલરશિપ શોધો",
        "sel4_lbl": "પરીક્ષાનું સ્તર પસંદ કરો:",
        "exam_tiers": ["રાજ્ય સ્તરની સરકારી પરીક્ષા (State PSC)", "રાષ્ટ્રીય સ્તરની પરીક્ષા (UPSC, NEET, JEE)", "વૈશ્વિક પરીક્ષા (GRE, IELTS)"],
        "txt4_lbl": "પરીક્ષાનું નામ ટાઈપ કરો:",
        "btn4_lbl": "🚀 પરીક્ષા પેટર્ન અને પ્રશ્નો મેળવો",
        "sel5_lbl": "શૈક્ષણિક પ્રવાહ પસંદ કરો:",
        "streams": ["આર્ટસ પ્રવાહ (Arts)", "કોમર્સ પ્રવાહ (Commerce)", "સાયન્સ પ્રવાહ (Pure Sciences)", "ટેકનિકલ અને મેડિકલ", "વ્યવસાયિક અને કૌશલ્ય (Vocational/Solar)"],
        "rad5_lbl": "કરિયર ક્ષેત્ર (Scope):",
        "scopes": ["સ્થાનિક અને રાષ્ટ્રીય તકો", "વૈશ્વિક તકો"],
        "txt5_lbl": "વિદ્યાર્થીની વ્યક્તિગત રુચિ (જેમ કે સોલર, ડેટา સાયન્સ):",
        "btn5_lbl": "🚀 કરિયર રોડમેપ અને લિંક્સ મેળવો"
    },
    "Kannada": {
        "menu_lbl": "🌍 ಭಾಷೆ ಮತ್ತು ರಾಜ್ಯವನ್ನು ಆಯ್ಕೆಮಾಡಿ:",
        "dash_menu": "🏠 ಮುಖ್ಯ ಪುಟ (Dashboard)",
        "sandbox_menu": "⚡ 6-ಇನ್-1 AI ಸ್ಯಾಂಡ್‌ಬಾಕ್ಸ್",
        "doubt_menu": "🧠 ಶಂಕೆ ಪರಿಹಾರ ಕೇಂದ್ರ",
        "login_menu": "🔐 ಲಾಗಿನ್ / ಪ್ರೊಫೈಲ್",
        "tabs": ["🧠 ಶಂಕೆ ಪರಿಹಾರ ಶಿಕ್ಷಕ", "📅 ಅಧ್ಯಯನ ವೇಳಾಪಟ್ಟಿ", "🛡️ ಸ್ಕಾಲರ್‌ಶಿಪ್ ಇಂಜಿನ್", "🎯 ಪರೀಕ್ಷಾ ಕೇಂದ್ರ", "🏢 ವೃತ್ತಿ ಮಾರ್ಗದರ್ಶಕ", "🌐 ಭಾಷಾ ಕೇಂದ್ರ"],
        "q1_lbl": "ನಿಮ್ಮ ಶೈಕ್ಷಣಿಕ ಪ್ರಶ್ನೆಯನ್ನು ಕೇಳಿ:",
        "btn1_lbl": "🚀 ಶಂಕೆ ಪರಿಹರಿಸಿ",
        "q2_lbl": "ನೀವು ಯಾವ ಪರೀಕ್ಷೆಗೆ ತಯಾರಿ ನಡೆಸುತ್ತಿದ್ದೀರಿ?",
        "s2_lbl": "ದಿನಕ್ಕೆ ಎಷ್ಟು ಗಂಟೆ ಓದಲು ಲಭ್ಯವಿದೆ?",
        "btn2_lbl": "🚀 ಸ್ಮಾರ್ಟ್ ವೇಳಾಪಟ್ಟಿ ರಚಿಸಿ",
        "sel3_lbl": "ವಿದ್ಯಾರ್ಥಿಯ ಶೈಕ್ಷಣಿಕ ಮಟ್ಟವನ್ನು ಆರಿಸಿ:",
        "edu_opts": ["ತರಗತಿ 1 ರಿಂದ 4", "ತರಗತಿ 5 ರಿಂದ 7", "ತರಗತಿ 8 ರಿಂದ 10 (SSC)", "ತರಗತಿ 11 ಮತ್ತು 12 (HSC)", "ಪದವಿ (Undergraduate)", "ಸ್ನಾತಕೋತ್ತರ (Postgraduate)", "ಪಿಎಚ್.ಡಿ. ಸಂಶೋಧನೆ"],
        "inc3_lbl": "ಕುಟುಂಬದ ವಾರ್ಷಿಕ ಆದಾಯವನ್ನು ಆರಿಸಿ:",
        "inc_opts": ["₹1.5 ಲಕ್ಷಕ್ಕಿಂತ ಕಡಿಮೆ", "₹1.5 ಲಕ್ಷದಿಂದ ₹3 ಲಕ್ಷ", "₹3 ಲಕ್ಷದಿಂದ ₹8 ಲಕ್ಷ", "₹8 ಲಕ್ಷಕ್ಕಿಂತ ಹೆಚ್ಚು"],
        "cat3_lbl": "ವರ್ಗ / ಜಾತಿ ನಮೂದಿಸಿ (Open, OBC, SC, ST):",
        "btn3_lbl": "🚀 ಅರ್ಹ ಸ್ಕಾಲರ್‌ಶಿಪ್ ಹುಡುಕಿ",
        "sel4_lbl": "ಪರೀಕ್ಷೆಯ ಮಟ್ಟವನ್ನು ಆಯ್ಕೆಮಾಡಿ:",
        "exam_tiers": ["ರಾಜ್ಯ ಮಟ್ಟದ ಪರೀಕ್ಷೆ (State PSC)", "ರಾಷ್ಟ್ರೀಯ ಮಟ್ಟದ ಪರೀಕ್ಷೆ (UPSC, NEET, JEE)", "ಜಾಗತಿಕ ಪರೀಕ್ಷೆ (GRE, IELTS)"],
        "txt4_lbl": "ಪರೀಕ್ಷೆಯ ಹೆಸರನ್ನು ಟೈಪ್ ಮಾಡಿ:",
        "btn4_lbl": "🚀 ಪರೀಕ್ಷಾ ಮಾದರಿ ಮತ್ತು ಪ್ರಶ್ನೆಗಳನ್ನು ಪಡೆಯಿರಿ",
        "sel5_lbl": "ಶೈಕ್ಷಣಿಕ ವಿಭಾಗವನ್ನು ಆಯ್ಕೆಮಾಡಿ:",
        "streams": ["ಕಲಾ ವಿಭಾಗ (Arts)", "ವಾಣಿಜ್ಯ ವಿಭಾಗ (Commerce)", "ವಿಜ್ಞಾನ ವಿಭಾಗ (Pure Sciences)", "ತಾಂತ್ರಿಕ ಮತ್ತು ವೈದ್ಯಕೀಯ", "ವೃತ್ತಿಪರ ಮತ್ತು ಕೌಶಲ್ಯ (Vocational/Solar)"],
        "rad5_lbl": "ವೃತ್ತಿ ಅವಕಾಶದ ಮಟ್ಟ (Scope):",
        "scopes": ["ಸ್ಥಳೀಯ ಮತ್ತು ರಾಷ್ಟ್ರೀಯ ಅವಕಾಶಗಳು", "ಜಾಗತಿಕ ಅವಕಾಶಗಳು"],
        "txt5_lbl": "ವಿದ್ಯಾರ್ಥಿಯ ವೈಯಕ್ತಿಕ ಆಸಕ್ತಿ (ಉದಾ. ಸೋಲಾರ್, ಡೇಟಾ ಸೈನ್ಸ್):",
        "btn5_lbl": "🚀 ವೃತ್ತಿ ಮಾರ್ಗಸೂಚಿ ಮತ್ತು ಲಿಂಕ್‌ಗಳನ್ನು ಪಡೆಯಿರಿ"
    },
    "Tamil": {
        "menu_lbl": "🌍 மொழி மற்றும் மாநிலத்தைத் தேர்ந்தெடுக்கவும்:",
        "dash_menu": "🏠 முதன்மை ಡ್ಯಾಶ್‌ಬೋರ್ಡ್",
        "sandbox_menu": "⚡ 6-இன்-1 AI சாண்ட்பாக்ஸ்",
        "doubt_menu": "🧠 சந்தேகத் தீர்வு மையம்",
        "login_menu": "🔐 உள்நுழைவு / சுயவிவரம்",
        "tabs": ["🧠 சந்தேகத் தீர்வு ஆசிரியர்", "📅 படிப்பு கால அட்டவணை", "🛡️ உதவித்தொகை எஞ்சின்", "🎯 தேர்வு மையம்", "🏢 தொழில் வழிகாட்டி", "🌐 மொழி மையம்"],
        "q1_lbl": "உங்கள் கல்விဆိုင်ရာ கேள்வியைக் கேளுங்கள்:",
        "btn1_lbl": "🚀 சந்தேகத்தைத் தீர்க்கவும்",
        "q2_lbl": "நீங்கள் எந்தத் தேர்வுக்குத் தயாராகிறீர்கள்?",
        "s2_lbl": "தினமும் படிக்க எத்தனை மணி நேரம் உள்ளது?",
        "btn2_lbl": "🚀 ஸ்மார்ட் கால அட்டவணையை உருவாக்குங்கள்",
        "sel3_lbl": "மாணவரின் கல்வி நிலையைத் தேர்ந்தெடுக்கவும்:",
        "edu_opts": ["வகுப்பு 1 முதல் 4", "வகுப்பு 5 முதல் 7", "வகுப்பு 8 முதல் 10 (SSC)", "வகுப்பு 11 மற்றும் 12 (HSC)", "பட்டப்படிப்பு (Undergraduate)", "முதுகலை (Postgraduate)", "ಪಿಎಚ್.ಡಿ. ಸಂಶೋಧನೆ"],
        "inc3_lbl": "குடும்ப வருமானத்தைத் தேர்ந்தெடுக்கவும்:",
        "inc_opts": ["₹1.5 லட்சத்திற்கும் கீழ்", "₹1.5 லட்சம் முதல் ₹3 லட்சம்", "₹3 லட்சம் முதல் ₹8 லட்சம்", "₹8 லட்சத்திற்கும் மேல்"],
        "cat3_lbl": "பிரிவு / சாதியை உள்ளிடவும் (Open, OBC, SC, ST):",
        "btn3_lbl": "🚀 தகுதியான உதவித்தொகையைக் கண்டறியவும்",
        "sel4_lbl": "தேர்வு நிலையைத் தேர்ந்தெடுக்கவும்:",
        "exam_tiers": ["மாநில அரசுத் தேர்வு (State PSC)", "தேசிய அளவிலான தேர்வு (UPSC, NEET, JEE)", "சர்வதேச தேர்வு (GRE, IELTS)"],
        "txt4_lbl": "தேர்வின் பெயரை உள்ளிடவும்:",
        "btn4_lbl": "🚀 தேர்வு மாதிரி மற்றும் வினாக்களைப் பெறுக",
        "sel5_lbl": "கல்விப் பிரிவைத் தேர்ந்தெடுக்கவும்:",
        "streams": ["கலைப்பிரிவு (Arts)", "வணிகவியல் (Commerce)", "அறிவியல் பிரிவு (Pure Sciences)", "தொழில்நுட்பம் மற்றும் மருத்துவம்", "தொழில்சார் கல்வி (Vocational/Solar)"],
        "rad5_lbl": "வேலைவாய்ப்பு எல்லை (Scope):",
        "scopes": ["உள்நாட்டு மற்றும் தேசிய வாய்ப்புகள்", "உலகளாவிய வாய்ப்புகள்"],
        "txt5_lbl": "மாணவரின் தனிப்பட்ட ஆர்வம் (ಉದಾ. சோலார், டேಟಾ ಸೈನ್ಸ್):",
        "btn5_lbl": "🚀 தொழில் வழிகாட்டி மற்றும் இணைப்புகளைப் பெறுக"
    },
    "Telugu": {
        "menu_lbl": "🌍 భాష మరియు రాష్ట్రాన్ని ఎంచుకోండి:",
        "dash_menu": "🏠 ప్రధాన డాష్‌బోర్డ్",
        "sandbox_menu": "⚡ 6-ఇన్-1 AI శాండ్‌బాక్స్",
        "doubt_menu": "🧠 సందేహ నివృత్తి కేంద్రం",
        "login_menu": "🔐 లాగిన్ / ప్రొఫైల్",
        "tabs": ["🧠 సందేహ నివృత్తి ఉపాధ్యాయుడు", "📅 అధ్యయన ప్రణాళిక", "🛡️ స్కాలర్‌షిప్ ఇంజిన్", "🎯 పరీక్షా కేంద్రం", "🏢 కెరీర్ మార్గదర్శి", "🌐 భాషా కేంద్రం"],
        "q1_lbl": "మీ విద్యా సంబంధిత ప్రశ్నను అడగండి:",
        "btn1_lbl": "🚀 సందేహాన్ని నివృత్తి చేయండి",
        "q2_lbl": "మీరు ఏ పరీక్షకు సిద్ధమవుతున్నారు?",
        "s2_lbl": "రోజుకు ఎన్ని గంటలు చదవగలరు?",
        "btn2_lbl": "🚀 స్మార్ట్ టైమ్ టేబుల్ సృష్టించండి",
        "sel3_lbl": "విద్యార్థి విద్యా స్థాయిని ఎంచుకోండి:",
        "edu_opts": ["1 నుండి 4 వ తరగతి", "5 నుండి 7 వ తరగతి", "8 నుండి 10 వ తరగతి (SSC)", "11 మరియు 12 వ తరగతి (HSC)", "డిగ్రీ (Undergraduate)", "పీజీ (Postgraduate)", "Ph.D. రీసెర్చ్"],
        "inc3_lbl": "కుటుంబ వార్షిక ఆదాయాన్ని ఎంచుకోండి:",
        "inc_opts": ["₹1.5 లక్షల కంటే తక్కువ", "₹1.5 లక్షల నుండి ₹3 లక్షలు", "₹3 లక్షల నుండి ₹8 లక్షలు", "₹8 లక్షల కంటే ఎక్కువ"],
        "cat3_lbl": "కేటగిరీ / కులం టైప్ చేయండి (Open, OBC, SC, ST):",
        "btn3_lbl": "🚀 అర్హత గల స్కాలర్‌షిప్‌లను కనుగొనండి",
        "sel4_lbl": "పరీక్ష స్థాయిని ఎంచుకోండి:",
        "exam_tiers": ["రాష్ట్ర స్థాయి పరీక్ష (State PSC)", "జాతీయ స్థాయి పరీక్ష (UPSC, NEET, JEE)", "అంతర్జాతీయ పరీక్ష (GRE, IELTS)"],
        "txt4_lbl": "పరీక్ష పేరు టైప్ చేయండి:",
        "btn4_lbl": "🚀 పరీక్షా సరళి & ప్రశ్నలను పొందండి",
        "sel5_lbl": "విద్యా విభాగాన్ని ఎంచుకోండి:",
        "streams": ["ఆర్ట్స్ (Arts)", "కామర్స్ (Commerce)", "సైన్స్ (Pure Sciences)", "టెక్నికల్ & మెడికల్", "ఒకేషనల్ & స్కిల్స్ (Vocational/Solar)"],
        "rad5_lbl": "కెరీర్ పరిధి (Scope):",
        "scopes": ["స్థానిక మరియు జాతీయ అవకాశాలు", "ప్రపంచవ్యాప్త అవకాశాలు"],
        "txt5_lbl": "విద్యార్థి వ్యక్తిగత ఆసక్తి (ఉదా. సోలార్, డేటా సైన్స్):",
        "btn5_lbl": "🚀 కెరీర్ రోడ్‌మ్యాప్ & లింక్‌లను పొందండి"
    },
    "Punjabi": {
        "menu_lbl": "🌍 ਭਾਸ਼ਾ ਅਤੇ ਰਾਜ ਚੁਣੋ:",
        "dash_menu": "🏠 ਮੁੱਖ ਡੈਸ਼ਬੋਰਡ",
        "sandbox_menu": "⚡ 6-ਇਨ-1 AI ਸੈਂਡਬੌਕਸ",
        "doubt_menu": "🧠 ਸ਼ੰਕਾ ਨਿਵਾਰਨ ਕੇਂਦਰ",
        "login_menu": "🔐 ਲੌਗਇਨ / ਪ੍ਰੋਫਾਈਲ",
        "tabs": ["🧠 ਸ਼ੰਕਾ ਨਿਵਾਰਨ ਅਧਿਆਪਕ", "📅 ਪੜ੍ਹਾਈ ਦਾ ਸਮਾਂ-ਸਾਰਣੀ", "🛡️ ਸਕਾਲਰਸ਼ਿਪ ਇੰਜਣ", "🎯 ਪ੍ਰੀਖਿਆ ਕੇਂਦਰ", "🏢 ਕਰੀਅਰ ਮਾਰਗਦਰਸ਼ਕ", "🌐 ਭਾਸ਼ਾ ਕੇਂਦਰ"],
        "q1_lbl": "ਆਪਣਾ ਵਿਦਿਅਕ ਸਵਾਲ ਪੁੱਛੋ:",
        "btn1_lbl": "🚀 ਸ਼ੰਕਾ ਦਾ ਹੱਲ ਕਰੋ",
        "q2_lbl": "ਤੁਸੀਂ ਕਿਸ ਪ੍ਰੀਖਿਆ ਦੀ ਤਿਆਰੀ ਕਰ ਰਹੇ ਹੋ?",
        "s2_lbl": "ਰੋਜ਼ਾਨਾ ਪੜ੍ਹਨ ਲਈ ਕਿੰਨੇ ਘੰਟੇ ਉਪਲਬਧ ਹਨ?",
        "btn2_lbl": "🚀 ਸਮਾਰਟ ਸਮਾਂ-ਸਾਰਣੀ ਬਣਾਓ",
        "sel3_lbl": "ਵਿਦਿਆਰਥੀ ਦਾ ਵਿਦਿਅਕ ਪੱਧਰ ਚੁਣੋ:",
        "edu_opts": ["ਕਲਾਸ 1 ਤੋਂ 4", "ਕਲਾਸ 5 ਤੋਂ 7", "ਕਲਾਸ 8 ਤੋਂ 10 (SSC)", "ਕਲਾਸ 11 ਅਤੇ 12 (HSC)", "ਗ੍ਰੈਜੂਏਸ਼ਨ (Undergraduate)", "ਪੋਸਟ ਗ੍ਰੈਜੂਏਸ਼ਨ (Postgraduate)", "ਪੀਐਚ.ਡੀ. ਖੋਜ"],
        "inc3_lbl": "ਸਾਲਾਨਾ ਪਰਿਵਾਰਕ ਆਮਦਨ ਚੁਣੋ:",
        "inc_opts": ["₹1.5 ਲੱਖ ਤੋਂ ਘੱਟ", "₹1.5 ਲੱਖ ਤੋਂ ₹3 ਲੱਖ", "₹3 ਲੱਖ ਤੋਂ ₹8 ਲੱਖ", "₹8 ਲੱਖ ਤੋਂ ਵੱਧ"],
        "cat3_lbl": "ਆਪਣੀ ਸ਼੍ਰੇਣੀ / ਜਾਤੀ ਲਿਖੋ (Open, OBC, SC, ST):",
        "btn3_lbl": "🚀 ਯੋਗ ਸਕਾਲਰਸ਼ਿਪ ਲੱਭੋ",
        "sel4_lbl": "ਪ੍ਰੀਖਿਆ ਦਾ ਪੱਧਰ ਚੁਣੋ:",
        "exam_tiers": ["ਰਾਜ ਪੱਧਰੀ ਪ੍ਰੀਖਿਆ (State PSC)", "ਰਾਸ਼ਟਰੀ ਪੱਧਰੀ ਪ੍ਰੀਖਿਆ (UPSC, NEET, JEE)", "ਗਲੋਬਲ ਪ੍ਰੀਖਿਆ (GRE, IELTS)"],
        "txt4_lbl": "ਪ੍ਰੀਖਿਆ ਦਾ ਨਾਮ ਲਿਖੋ:",
        "btn4_lbl": "🚀 ਪ੍ਰੀਖਿਆ ਪੈਟਰਨ ਅਤੇ ਪ੍ਰਸ਼ਨ ਪ੍ਰਾਪਤ ਕਰੋ",
        "sel5_lbl": "ਪੜ੍ਹਾਈ ਦੀ ਸਟ੍ਰੀਮ ਚੁਣੋ:",
        "streams": ["ਆਰਟਸ (Arts)", "ਕਾਮਰਸ (Commerce)", "ਸਾਇੰਸ (Pure Sciences)", "ਤਕਨੀਕੀ ਅਤੇ ਮੈਡੀਕਲ", "ਵੋਕੇਸ਼ਨਲ ਅਤੇ ਹੁਨਰ (Vocational/Solar)"],
        "rad5_lbl": "ਕਰੀਅਰ ਦਾ ਦਾਇਰਾ (Scope):",
        "scopes": ["ਸਥਾਨਕ ਅਤੇ ਰਾਸ਼ਟਰੀ ਮੌਕੇ", "ਗਲੋਬਲ ਮੌਕੇ"],
        "txt5_lbl": "ਵਿਦਿਆਰਥੀ ਦੀ ਨਿੱਜੀ ਰੁਚੀ (ਜਿਵੇਂ ਸੋਲਰ, ਡੇਟਾ ਸਾਇੰਸ):",
        "btn5_lbl": "🚀 ਕਰੀਅਰ ਰੋਡਮੈਪ ਅਤੇ ਲਿੰਕ ਪ੍ਰਾਪਤ ਕਰੋ"
    },
    "Bengali": {
        "menu_lbl": "🌍 ভাষা এবং রাজ্য চয়ন করুন:",
        "dash_menu": "🏠 প্রধান ড্যাশবোর্ড",
        "sandbox_menu": "⚡ ৬-ইন-১ AI স্যান্ডবক্স",
        "doubt_menu": "🧠 সন্দেহ নিরসন কেন্দ্র",
        "login_menu": "🔐 লগইন / প্রোফাইল",
        "tabs": ["🧠 সন্দেহ নিরসন শিক্ষক", "📅 অধ্যয়নের সময়সূচী", "🛡️ স্কলারশিপ ইঞ্জিন", "🎯 পরীক্ষা কেন্দ্র", "🏢 ক্যারিয়ার নির্দেশিকা", "🌐 ভাষা কেন্দ্র"],
        "q1_lbl": "আপনার শিক্ষাগত প্রশ্ন জিজ্ঞাসা করুন:",
        "btn1_lbl": "🚀 সন্দেহ নিরসন করুন",
        "q2_lbl": "আপনি কোন পরীক্ষার প্রস্তুতি নিচ্ছেন?",
        "s2_lbl": "প্রতিদিন পড়ার জন্য কত ঘন্টা সময় আছে?",
        "btn2_lbl": "🚀 স্মার্ট সময়সূচী তৈরি করুন",
        "sel3_lbl": "শিক্ষার্থীর শিক্ষাগত স্তর নির্বাচন করুন:",
        "edu_opts": ["প্রথম থেকে চতুর্থ শ্রেণী", "পঞ্চম থেকে সপ্তম শ্রেণী", "অষ্টম থেকে দশম শ্রেণী (SSC)", "একাদশ ও দ্বাদশ শ্রেণী (HSC)", "স্নাতক (Undergraduate)", "স্নাতকোত্তর (Postgraduate)", "পিএইচডি গবেষণা"],
        "inc3_lbl": "পারিবারিক বার্ষিক আয় নির্বাচন করুন:",
        "inc_opts": ["₹১.৫ লক্ষের কম", "₹১.৫ লক্ষ থেকে ₹৩ লক্ষ", "₹৩ লক্ষ থেকে ₹৮ লক্ষ", "₹৮ লক্ষের বেশি"],
        "cat3_lbl": "আপনার বিভাগ / জাতি লিখুন (Open, OBC, SC, ST):",
        "btn3_lbl": "🚀 যোগ্য স্কলারশিপ খুঁজুন",
        "sel4_lbl": "পরীক্ষার স্তর নির্বাচন করুন:",
        "exam_tiers": ["রাজ্য স্তরের পরীক্ষা (State PSC)", "জাতীয় স্তরের পরীক্ষা (UPSC, NEET, JEE)", "আন্তর্জাতিক পরীক্ষা (GRE, IELTS)"],
        "txt4_lbl": "পরীক্ষার নাম টাইপ করুন:",
        "btn4_lbl": "🚀 পরীক্ষার প্যাটার্ন ও নমুনা প্রশ্ন পান",
        "sel5_lbl": "শিক্ষাগত স্ট্রিম নির্বাচন করুন:",
        "streams": ["কলা শাখা (Arts)", "বাণিজ্য শাখা (Commerce)", "বিজ্ঞান শাখা (Pure Sciences)", "কারিগরি ও চিকিৎসা", "বৃত্তিমূলক ও দক্ষতা (Vocational/Solar)"],
        "rad5_lbl": "ক্যারিয়ারের সুযোগ (Scope):",
        "scopes": ["স্থানীয় এবং জাতীয় সুযোগ", "বৈশ্বিক সুযোগ"],
        "txt5_lbl": "শিক্ষার্থীর ব্যক্তিগত আগ্রহ (যেমন সোলার, ডাটা সায়েন্স):",
        "btn5_lbl": "🚀 ক্যারিয়ার রোডম্যাপ এবং লিঙ্ক পান"
    }
}

# --- ५. प्रगत हाय-कॉन्ट्रास्ट विजिबिलिटी स्टायलिंग (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght=400;600;700;800&family=Inter:wght=400;600;700&display=swap');
    * { font-family: 'Noto Sans Devanagari', 'Inter', sans-serif; }
    
    .stApp { background: #0d1117; color: #f0f6fc !important; }
    
    /* --- डाव्या बाजूचा प्रीमियम विजिबिलिटी साईडबार --- */
    [data-testid="stSidebar"] {
        background-color: #070a0e !important; 
        border-right: 3px solid #FFD700 !important;
        padding-top: 30px;
    }
    [data-testid="stSidebar"] label {
        color: #FFD700 !important;
        font-size: 1.2rem !important;
        font-weight: 800 !important;
    }
    
    /* मुख्य शिर्षक डिझाईन */
    .main-title {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800; font-size: 3rem; display: block;
        margin-bottom: 5px;
    }
    
    /* आडव्या नेव्हिगेशन बारमधील रेडिओ बटन्सचे सुशोभीकरण */
    div[data-testid="stRadio"] > div[role="radiogroup"] {
        flex-direction: row !important;
        justify-content: flex-start !important;
        gap: 15px !important;
    }
    div[data-testid="stRadio"] > div[role="radiogroup"] > div {
        background-color: #161b22 !important;
        border: 2px solid #30363d !important;
        padding: 10px 20px !important;
        border-radius: 8px !important;
    }
    div[data-testid="stRadio"] > div[role="radiogroup"] label {
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
    }
    
    /* टॅब सुशोभीकरण (सर्व भारतीय भाषांमध्ये मोठे आणि स्पष्ट दिसण्यासाठी) */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; background-color: #161b22; padding: 10px; border-radius: 12px; }
    .stTabs [data-baseweb="tab"] {
        height: 52px; background-color: #21262d; border-radius: 8px;
        color: #ffffff !important; font-weight: 700 !important; font-size: 1.15rem !important;
    }
    .stTabs [aria-selected="true"] { background-color: #FFD700 !important; color: #0d1117 !important; }
    
    .glass-card { background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 25px; margin-bottom: 20px; }
    .footer-container { border-top: 1px solid #30363d; padding-top: 25px; margin-top: 60px; text-align: center; color: #8b949e; }
    </style>
""", unsafe_allow_html=True)

# --- ६. पहिली सुरक्षित भाषा निवड लोड करणे ---
if "global_language_selector" in st.session_state:
    selected_lang_key = st.session_state["global_language_selector"]
else:
    selected_lang_key = "मराठी (Marathi) - Maharashtra"

target_lang = languages_map.get(selected_lang_key, "Marathi")
current_ui = UI_LANG_MATRIX.get(target_lang, UI_LANG_MATRIX["English"])

# --- ७. डाव्या बाजूचा साईडबार (फक्त भाषा निवडण्यासाठी) ---
selected_display_lang = st.sidebar.selectbox(
    "🌍 भाषा निवडा / Select Language:",
    list(languages_map.keys()),
    index=list(languages_map.keys()).index(selected_lang_key) if selected_lang_key in languages_map else 0,
    key="global_language_selector"
)

# भाषा निवड बदलल्यास डिक्शनरी पुन्हा सिंक करणे
target_lang = languages_map[selected_display_lang]
current_ui = UI_LANG_MATRIX.get(target_lang, UI_LANG_MATRIX["English"])

# =========================================================================
# 🔥 मुख्य स्क्रीनच्या अगदी वरती 'आडवा रिअल टाइम वर्किंग नेव्हिगेशन बार'
# =========================================================================
app_mode = st.radio(
    "", 
    [current_ui["dash_menu"], current_ui["sandbox_menu"], current_ui["doubt_menu"], current_ui["login_menu"]],
    horizontal=True,
    key="top_navigation_bar_matrix"
)

st.markdown("---")

# --- ८. AI कॉल फंक्शन (Groq API) ---
def fetch_ai_response(prompt_text, system_setting):
    try:
        groq_api_key = st.secrets["GROQ_API_KEY"]
        groq_url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {groq_api_key}", "Content-Type": "application/json"}
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "system", "content": system_setting}, {"role": "user", "content": prompt_text}],
            "temperature": 0.4, "max_tokens": 1500
        }
        response = requests.post(groq_url, headers=headers, data=json.dumps(payload))
        return response.json()["choices"][0]["message"]["content"] if response.status_code == 200 else f"Error: {response.status_code}"
    except Exception as e: return f"Error: {e}"

base_ai_instruction = f"""
You are the elite AI Engine of 'Abhyas Kranti' App, completely customized for {target_lang}.
1. Respond ONLY and strictly in '{target_lang}'.
2. Automatically adapt context, schemes, rules, and logic for the state mentioned in '{selected_display_lang}'.
"""

# ==========================================
# विभाग १: Dashboard
# ==========================================
if app_mode == current_ui["dash_menu"]:
    st.markdown('<span class="main-title">Abhyas Kranti National Portal</span>', unsafe_allow_html=True)
    st.markdown('### AI Powered Educational Ecosystem for Rural India')
    st.markdown(f"**🌍 Active Language Context:** `{selected_display_lang}`")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="glass-card"><h3>Dynamic Localization</h3><p style="color:#c9d1d9;">System automatically maps Central and State education rules synchronously upon language toggle.</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="glass-card"><h3>IIT Patna Capstone</h3><p style="color:#c9d1d9;">Tailored for high-contrast accessibility in rural ecosystems.</p></div>', unsafe_allow_html=True)

# ==========================================
# विभाग २: ६-इन-१ AI सँडबॉक्स (आता ९ ही भाषांमध्ये चालेल!)
# ==========================================
elif app_mode == current_ui["sandbox_menu"]:
    st.markdown(f'<span class="main-title">{current_ui["sandbox_menu"]}</span>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(current_ui["tabs"])

    with tab1:
        st.markdown(f"### {current_ui['tabs'][0]}")
        user_query = st.text_input(current_ui["q1_lbl"], key="q1_sandbox")
        if st.button(current_ui["btn1_lbl"], key="btn1_sandbox"):
            with st.spinner("Processing..."):
                st.write(fetch_ai_response(user_query, base_ai_instruction + "Give detailed answer in bullet points."))

    with tab2:
        st.markdown(f"### {current_ui['tabs'][1]}")
        exam_target = st.text_input(current_ui["q2_lbl"], "Board Exam", key="q2")
        hours = st.slider(current_ui["s2_lbl"], 1, 12, 5, key="s2")
        if st.button(current_ui["btn2_lbl"], key="btn2"):
            with st.spinner("Planning..."):
                st.write(fetch_ai_response(f"Exam: {exam_target}, Hours: {hours}", base_ai_instruction + "Create 7 day schedule."))

    with tab3:
        st.markdown(f"### {current_ui['tabs'][2]}")
        edu = st.selectbox(current_ui["sel3_lbl"], current_ui["edu_opts"], key="edu_lvl")
        inc = st.selectbox(current_ui["inc3_lbl"], current_ui["inc_opts"], key="inc_lvl")
        cat = st.text_input(current_ui["cat3_lbl"], "OBC", key="cat")
        if st.button(current_ui["btn3_lbl"], key="btn3"):
            with st.spinner("Searching..."):
                st.write(fetch_ai_response(f"Edu: {edu}, Income: {inc}, Cat: {cat}", base_ai_instruction + "Suggest 3 state scholarships."))

    with tab4:
        st.markdown(f"### {current_ui['tabs'][3]}")
        tier = st.selectbox(current_ui["sel4_lbl"], current_ui["exam_tiers"], key="ex_lvl")
        ex_name = st.text_input(current_ui["txt4_lbl"], "Exam", key="ex_name")
        if st.button(current_ui["btn4_lbl"], key="btn4"):
            with st.spinner("Analyzing..."):
                st.write(fetch_ai_response(f"Tier: {tier}, Exam: {ex_name}", base_ai_instruction + "Give latest exam structure and 1 sample MCQ."))

    with tab5:
        st.markdown(f"### {current_ui['tabs'][4]}")
        stream = st.selectbox(current_ui["sel5_lbl"], current_ui["streams"], key="stream")
        scope = st.radio(current_ui["rad5_lbl"], current_ui["scopes"], key="scope")
        interest = st.text_input(current_ui["txt5_lbl"], "Solar Energy", key="interest")
        if st.button(current_ui["btn5_lbl"], key="btn5"):
            with st.spinner("Mapping..."):
                st.write(fetch_ai_response(f"Stream: {stream}, Scope: {scope}, Interest: {interest}", base_ai_instruction + "Provide 3 career roadmaps with links."))

    with tab6:
        st.markdown(f"### {current_ui['tabs'][5]}")
        st.success(f"✔️ Multilingual Synchronization Active for: {selected_display_lang}")

# ==========================================
# विभाग ३: स्वतंत्र शंका निरसन केंद्र
# ==========================================
elif app_mode == current_ui["doubt_menu"]:
    st.markdown(f'<span class="main-title">{current_ui["doubt_menu"]}</span>', unsafe_allow_html=True)
    user_query = st.text_input(current_ui["q1_lbl"], key="q1_direct")
    if st.button(current_ui["btn1_lbl"], key="btn1_direct"):
        with st.spinner("AI Mentor is thinking..."):
            st.write(fetch_ai_response(user_query, base_ai_instruction + "Give direct and clean solutions."))

# ==========================================
# विभाग ४: लॉगिन / प्रोफाईल
# ==========================================
elif app_mode == current_ui["login_menu"]:
    st.markdown(f'<span class="main-title">{current_ui["login_menu"]}</span>', unsafe_allow_html=True)
    with st.form("login_form"):
        st.text_input("Username / Email:")
        st.text_input("Password:", type="password")
        st.form_submit_button("Submit")

# --- ९. एकत्रित फायनल फुटर ---
st.markdown("""
    <div class="footer-container">
        <p style="font-size: 1.1rem; color: #ffffff; font-weight: 700; margin-bottom: 2px;">Developed by Dnyaneshwar Gawalikar</p>
        <p style="color: #FFD700; font-weight: 600; margin-bottom: 15px; font-size: 0.9rem;">Professor & Head of Department</p>
        <p style="font-size: 0.8rem; color: #8b949e;">Capstone Project — IIT Patna Generative AI Sprint 2026</p>
    </div>
""", unsafe_allow_html=True)
