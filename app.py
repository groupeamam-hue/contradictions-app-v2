# contradictions_app.py - APPLICATION COMPLÈTE AVEC FONCTIONNALITÉS PORTABLES

import streamlit as st
import json
import random
import time
import pandas as pd
import base64
import os
import sys
from pathlib import Path
import socket

# =============================================
# FONCTION POUR PORTS AUTOMATIQUES (NOUVEAU)
# =============================================

def find_available_port(start_port=8501):
    """Trouve un port disponible automatiquement"""
    port = start_port
    max_port = start_port + 100
    while port <= max_port:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            port += 1
    return start_port  # Retourne le port par défaut si aucun trouvé

# =============================================
# CONFIGURATION DE LA PAGE
# =============================================

st.set_page_config(
    page_title="Contradictions Coran-Boukhari",
    page_icon="📖",
    layout="wide"
)

# =============================================
# TRADUCTIONS COMPLÈTES
# =============================================

translations = {
    "fr": {
        "title": "📖 Contradictions Coran-Boukhari",
        "subtitle": "Le Coran dit une chose... Boukhari dit le contraire",
        "cta": "**À qui tu crois ?**",
        "navigation": "🎯 Navigation",
        "menu_options": ["🏠 Accueil", "📚 Parcourir par Thème", "🧠 Quiz des Contradictions", "🔍 Recherche Avancée", "⚠️ Hadiths Faibles", "🎥 Vidéos Éducatives"],
        "stats_contradictions": "Contradictions",
        "stats_themes": "Thèmes",
        "stats_hadiths": "Hadiths analysés",
        "quick_nav": "🚀 Navigation Rapide",
        "bukhari_hadith": "📜 Hadith de Boukhari",
        "quran_verse": "🕌 Verset Coranique",
        "contradiction": "💥 Contradiction",
        "previous": "⏮️ Précédent",
        "random": "🔄 Aléatoire",
        "next": "Suivant ⏭️",
        "browse_by_theme": "📚 Contradictions par Thème",
        "select_theme": "Choisissez un thème:",
        "contradictions_in_theme": "contradictions dans ce thème",
        "see_contradiction": "Voir cette contradiction",
        "quiz_title": "🧠 Quiz des Contradictions",
        "quiz_description": "Testez vos connaissances sur les contradictions entre le Coran et les hadiths de Boukhari",
        "start_quiz": "🎯 Démarrer le Quiz",
        "question": "Question:",
        "answer_in": "⏳ La réponse dans...",
        "answer": "📖 Réponse:",
        "new_question": "🔁 Nouvelle Question",
        "back_home": "🏠 Retour à l'accueil",
        "search_title": "🔍 Recherche Avancée",
        "search_term": "Rechercher par mot-clé:",
        "filter_theme": "Filtrer par thème:",
        "search_in": "Rechercher dans:",
        "search_options": ["Tout le texte", "Hadiths seulement", "Coran seulement"],
        "results_found": "contradiction(s) trouvée(s)",
        "no_results": "Aucune contradiction trouvée avec ces critères.",
        "about_title": "ℹ️ À propos",
        "about_text": "Cette application présente des contradictions apparentes entre les hadiths de Sahih al-Bukhari et le texte coranique.",
        "goal": "**Objectif:** Inviter à la réflexion personnelle et à l'étude critique des sources islamiques.",
        "audience": "**Public:** Jeunes musulmans cherchant à comprendre leur religion au-delà des interprétations traditionnelles.",
        "statistics": "**📊 Statistiques:**",
        "footer_text": "Application Contradictions Coran-Boukhari - Pour la réflexion et l'étude critique",
        "weak_hadiths_title": "⚠️ Hadiths Faibles (Daïfs)",
        "weak_hadiths_description": "Cette section présente des hadiths considérés comme faibles ou non authentiques selon les critères scientifiques du hadith",
        "video_title": "🎥 Vidéos Éducatives",
        "video_description": "Regardez ces vidéos pour mieux comprendre les enjeux des contradictions entre le Coran et les hadiths",
        "french_video": "🇫🇷 Vidéo en Français",
        "arabic_video": "🇸🇦 Vidéo en Arabe",
        "watch_video": "🎬 Regarder la vidéo",
        "direct_link": "🔗 Lien direct YouTube",
        "portable_feature": "🚀 Version Portable",
        "portable_description": "Cette application peut fonctionner sans installation - version .exe disponible"
    },
    "ar": {
        "title": "📖 التناقضات بين القرآن والبخاري",
        "subtitle": "القرآن يقول شيئاً... والبخاري يقول العكس",
        "cta": "**لمن تصدق؟**",
        "navigation": "🎯 التنقل",
        "menu_options": ["🏠 الرئيسية", "📚 التصفح حسب الموضوع", "🧠 اختبار التناقضات", "🔍 بحث متقدم", "⚠️ الأحاديث الضعيفة", "🎥 فيديوهات تعليمية"],
        "stats_contradictions": "تناقضات",
        "stats_themes": "موضوعات",
        "stats_hadiths": "أحاديث تم تحليلها",
        "quick_nav": "🚀 تنقل سريع",
        "bukhari_hadith": "📜 حديث البخاري",
        "quran_verse": "🕌 آية قرآنية",
        "contradiction": "💥 التناقض",
        "previous": "⏮️ السابق",
        "random": "🔄 عشوائي",
        "next": "⏭️ التالي",
        "browse_by_theme": "📚 التناقضات حسب الموضوع",
        "select_theme": "اختر موضوعاً:",
        "contradictions_in_theme": "تناقض في هذا الموضوع",
        "see_contradiction": "عرض هذا التناقض",
        "quiz_title": "🧠 اختبار التناقضات",
        "quiz_description": "اختبر معرفتك حول التناقضات بين القرآن وأحاديث البخاري",
        "start_quiz": "🎯 بدء الاختبار",
        "question": "سؤال:",
        "answer_in": "⏳ الإجابة بعد...",
        "answer": "📖 الإجابة:",
        "new_question": "🔁 سؤال جديد",
        "back_home": "🏠 العودة للرئيسية",
        "search_title": "🔍 بحث متقدم",
        "search_term": "البحث بكلمة مفتاحية:",
        "filter_theme": "تصفية حسب الموضوع:",
        "search_in": "البحث في:",
        "search_options": ["كل النص", "الأحاديث فقط", "القرآن فقط"],
        "results_found": "تناقض(ات) تم العثور عليها",
        "no_results": "لم يتم العثور على أي تناقضات بهذه المعايير.",
        "about_title": "ℹ️ حول التطبيق",
        "about_text": "يعرض هذا التطبيق التناقضات الظاهرة بين أحاديث صحيح البخاري والنص القرآني.",
        "goal": "**الهدف:** تشجيع التفكير الشخصي والدراسة النقدية للمصادر الإسلامية.",
        "audience": "**الجمهور:** الشباب المسلم الذي يسعى لفهم دينه beyond التفسيرات التقليدية.",
        "statistics": "**📊 الإحصائيات:**",
        "footer_text": "تطبيق التناقضات بين القرآن والبخاري - للتفكير والدراسة النقدية",
        "weak_hadiths_title": "⚠️ الأحاديث الضعيفة (الدايفة)",
        "weak_hadiths_description": "هذا القسم يعرض أحاديث تعتبر ضعيفة أو غير صحيحة حسب المعايير العلمية للحديث",
        "video_title": "🎥 فيديوهات تعليمية",
        "video_description": "شاهد هذه الفيديوهات لفهم أفضل لإشكاليات التناقضات بين القرآن والأحاديث",
        "french_video": "🇫🇷 فيديو بالفرنسية",
        "arabic_video": "🇸🇦 فيديو بالعربية",
        "watch_video": "🎬 مشاهدة الفيديو",
        "direct_link": "🔗 رابط مباشر على يوتيوب",
        "portable_feature": "🚀 نسخة محمولة",
        "portable_description": "هذا التطبيق يمكن أن يعمل بدون تثبيت - نسخة .exe متاحة"
    }
}

# =============================================
# CONFIGURATION DES VIDÉOS YOUTUBE
# =============================================

YOUTUBE_CONFIG = {
    "french": {
        "title_fr": "🎥 Vidéo en Français - Explication des Contradictions",
        "title_ar": "🎥 فيديو بالفرنسية - شرح التناقضات",
        "description_fr": "Explication détaillée en français des contradictions entre le Coran et les hadiths de Boukhari",
        "description_ar": "شرح مفصل بالفرنسية للتناقضات بين القرآن وأحاديث البخاري",
        "youtube_id": "9cI3DXVox1Y",
        "youtube_url": "https://youtu.be/9cI3DXVox1Y",
        "embed_url": "https://www.youtube.com/embed/9cI3DXVox1Y"
    },
    "arabic": {
        "title_fr": "🎥 Vidéo en Arabe - Analyse des Contradictions", 
        "title_ar": "🎥 فيديو بالعربية - تحليل التناقضات",
        "description_fr": "Analyse approfondie en arabe des contradictions majeures avec exemples concrets",
        "description_ar": "تحليل متعمق بالعربية للتناقضات الرئيسية مع أمثلة عملية",
        "youtube_id": "Pz0KcVI05r8",
        "youtube_url": "https://youtu.be/Pz0KcVI05r8",
        "embed_url": "https://www.youtube.com/embed/Pz0KcVI05r8"
    }
}

# =============================================
# DONNÉES DES HADITHS FAIBLES
# =============================================

weak_hadiths_data = {
    "1. Prophète - Exagérations": [
        {
            "francais": "Faites recours à mon rang, car mon rang auprès d'Allah est grand.",
            "arabe": "توسلوا بجاهي ، فإن جاهي عند الله عظيم"
        },
        {
            "francais": "Le bien réside en moi et dans ma communauté jusqu'au Jour de la Résurrection.",
            "arabe": "الخير فيَّ وفي أمتي إلى يوم القيامة"
        }
    ],
    "2. Coran - Récompenses": [
        {
            "francais": "Toute chose a un cœur, et le cœur du Coran est Yâ-Sîn. Quiconque le récite, c'est comme s'il avait récité le Coran dix fois.",
            "arabe": "إن لكل شيء قلباً، وإن قلب القرآن (يس) من قرأها، فكأنما قرأ القرآن عشر مرات"
        }
    ]
}

# =============================================
# DONNÉES DES CONTRADICTIONS
# =============================================

contradictions_data = {
    "fr": {
        "RELIGION ET LIBERTÉ": [
            {
                "titre": "Liberté religieuse vs Mort",
                "boukhari": "« Le Prophète a dit: 'Celui qui change de religion, tuez-le.' » (Sahih al-Bukhari 6922)",
                "coran": "« Nulle contrainte en religion! » (Sourate 2, Verset 256)",
                "choc": "Le Coran garantit la liberté religieuse, Boukhari impose la peine de mort pour apostasie"
            }
        ],
        "FEMMES ET MARIAGE": [
            {
                "titre": "Statut des femmes",
                "boukhari": "« Le Prophète a dit: 'Je n'ai laissé après moi aucune tentation plus nuisible pour les hommes que les femmes.' » (Sahih al-Bukhari 5096)",
                "coran": "« Et parmi Ses signes Il a créé de vous, pour vous, des épouses pour que vous viviez en tranquillité avec elles et Il a mis entre vous de l'affection et de la bonté. » (Sourate 30, Verset 21)",
                "choc": "Le Coran valorise les femmes comme source de tranquillité, Boukhari les présente comme une tentation nuisible"
            }
        ],
        "SCIENCE ET RAISON": [
            {
                "titre": "Approche scientifique",
                "boukhari": "« Le Prophète a dit: 'La fièvre provient de la chaleur de l'Enfer.' » (Sahih al-Bukhari 3263)",
                "coran": "« En vérité, dans la création des cieux et de la terre, et dans l'alternance de la nuit et du jour, il y a des signes pour les doués d'intelligence. » (Sourate 3, Verset 190)",
                "choc": "Le Coran encourage la réflexion scientifique, Boukhari donne des explications non scientifiques"
            }
        ]
    },
    "ar": {
        "الدين والحرية": [
            {
                "titre": "الحرية الدينية مقابل الموت",
                "boukhari": "قال النبي: 'من بدل دينه فاقتلوه' (صحيح البخاري 6922)",
                "coran": "لا إكراه في الدين (سورة البقرة، الآية 256)",
                "choc": "القرآن يضمن الحرية الدينية، البخاري يفرض عقوبة الإعدام للردة"
            }
        ],
        "النساء والزواج": [
            {
                "titre": "مكانة المرأة",
                "boukhari": "قال النبي: 'ما تركت بعدي فتنة أضر على الرجال من النساء' (صحيح البخاري 5096)",
                "coran": "ومن آياته أن خلق لكم من أنفسكم أزواجاً لتسكنوا إليها وجعل بينكم مودة ورحمة (سورة الروم، الآية 21)",
                "choc": "القرآن يقدر النساء كمصدر للسكن، البخاري يقدمهن كفتنة مضرة"
            }
        ],
        "العلم والعقل": [
            {
                "titre": "المنهج العلمي",
                "boukhari": "قال النبي: 'الحمى من فيح جهنم' (صحيح البخاري 3263)",
                "coran": "إن في خلق السماوات والأرض واختلاف الليل والنهار لآيات لأولي الألباب (سورة آل عمران، الآية 190)",
                "choc": "القرآن يشجع التفكير العلمي، البخاري يقدم تفسيرات غير علمية"
            }
        ]
    }
}

# =============================================
# CSS PERSONNALISÉ
# =============================================

st.markdown("""
<style>
    .stInfo, .stSuccess, .stWarning, .stError { 
        border: 2px solid !important; 
        color: #FFFFFF !important; 
        font-weight: bold !important; 
        font-size: 16px !important; 
        padding: 20px !important; 
        border-radius: 10px !important; 
    }
    .stInfo { background-color: #1E90FF !important; border-color: #0066CC !important; }
    .stSuccess { background-color: #32CD32 !important; border-color: #228B22 !important; }
    .stWarning { background-color: #FF8C00 !important; border-color: #FF4500 !important; }
    .stError { background-color: #8A2BE2 !important; border-color: #4B0082 !important; }
    .stApp { background-color: #0e1117; }
    .stMarkdown, .stTitle, .stHeader, .stSubheader, p, div, span { color: #ffffff !important; }
    .arabic-text { direction: rtl; text-align: right; font-family: 'Arial', 'Segoe UI', Tahoma, sans-serif; font-size: 18px; line-height: 1.6; color: #ffffff !important; }
    .french-text { direction: ltr; text-align: left; font-family: 'Arial', 'Segoe UI', Tahoma, sans-serif; font-size: 16px; line-height: 1.6; color: #ffffff !important; }
    .video-container { display: flex; justify-content: center; margin: 20px 0; }
    .youtube-container { position: relative; width: 100%; height: 0; padding-bottom: 56.25%; margin: 20px 0; }
    .youtube-iframe { position: absolute; top: 0; left: 0; width: 100%; height: 100%; border-radius: 10px; }
    [data-testid="stMetricValue"] { font-size: 24px !important; font-weight: bold !important; color: #1E90FF !important; }
    [data-testid="stMetricLabel"] { font-size: 14px !important; font-weight: bold !important; color: #ffffff !important; }
    .download-btn { background-color: #4CAF50; color: white; padding: 12px 24px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; font-weight: bold; margin: 10px 0; border: none; cursor: pointer; }
    .download-btn:hover { background-color: #45a049; }
    .video-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 15px; margin: 15px 0; border: 2px solid #4A5568; }
    .portable-feature { background: linear-gradient(135deg, #FF8C00 0%, #FF4500 100%); padding: 15px; border-radius: 10px; margin: 10px 0; border: 2px solid #FF6347; }
</style>
""", unsafe_allow_html=True)

# =============================================
# FONCTIONS UTILITAIRES
# =============================================

def display_youtube_video(video_config, lang):
    """Affiche une vidéo YouTube avec son lecteur intégré"""
    st.markdown(f"""
    <div class="video-card">
        <h3>{"🇫🇷 " + video_config['title_fr'] if lang == 'fr' else "🇫🇷 " + video_config['title_ar']}</h3>
        <p>{video_config['description_fr'] if lang == 'fr' else video_config['description_ar']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Lecteur YouTube intégré
    st.markdown(f"""
    <div class="youtube-container">
        <iframe 
            class="youtube-iframe"
            src="{video_config['embed_url']}?rel=0&modestbranding=1"
            frameborder="0" 
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
            allowfullscreen>
        </iframe>
    </div>
    """, unsafe_allow_html=True)
    
    # Lien direct vers YouTube
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"**{translations[lang]['direct_link']}:** {video_config['youtube_url']}")
    with col2:
        st.markdown(f"""
        <a href="{video_config['youtube_url']}" target="_blank" style="text-decoration: none;">
            <button style="background-color: #FF0000; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; font-weight: bold;">
                ▶️ {translations[lang]['watch_video']}
            </button>
        </a>
        """, unsafe_allow_html=True)

def display_video_section(t, lang):
    st.markdown(f"### {t['video_title']}")
    st.markdown(t['video_description'])
    
    st.markdown("---")
    
    # Afficher seulement la vidéo française si langue = fr
    if lang == "fr":
        display_youtube_video(YOUTUBE_CONFIG["french"], lang)
        st.markdown("---")
    
    # Afficher seulement la vidéo arabe si langue = ar
    if lang == "ar":
        display_youtube_video(YOUTUBE_CONFIG["arabic"], lang)
        st.markdown("---")
    
    # Informations supplémentaires
    if lang == "fr":
        st.info("""
        **💡 Avantages de l'intégration YouTube :**
        - ✅ Lecture fluide sans délai de chargement
        - ✅ Qualité adaptative selon la connexion
        - ✅ Interface de lecture professionnelle
        - ✅ Pas de limite de bande passante
        - ✅ Compatible avec tous les appareils
        - ✅ Lecture hors ligne possible (via l'app YouTube)
        """)
    else:
        st.info("""
        **💡 مزايا التكامل مع يوتيوب:**
        - ✅ تشغيل سلس بدون تأخير في التحميل
        - ✅ جودة متكيفة حسب سرعة الاتصال
        - ✅ واجهة تشغيل احترافية
        - ✅ لا توجد حدود لاستهلاك البيانات
        - ✅ متوافق مع جميع الأجهزة
        - ✅ إمكانية المشاهدة بدون اتصال (عبر تطبيق يوتيوب)
        """)

def user_guide(t, lang):
    st.sidebar.markdown("---")
    st.sidebar.subheader("📖 Guide Utilisateur" if lang == "fr" else "📖 دليل المستخدم")
    
    with st.sidebar.expander("🎯 Comment utiliser" if lang == "fr" else "🎯 كيفية الاستخدام"):
        if lang == "fr":
            st.markdown("""
            **Navigation :**
            - 🏠 Accueil : Vue d'ensemble
            - 📚 Par thème : Par catégorie
            - 🧠 Quiz : Testez-vous
            - 🔍 Recherche : Trouvez rapidement
            - ⚠️ Hadiths faibles : Documentation
            - 🎥 Vidéos : Contenu multimédia
            
            **Fonctionnalités :**
            - Interface bilingue
            - Recherche avancée
            - Quiz interactif
            - Vidéos YouTube intégrées
            - Lecture fluide
            - Version portable (.exe)
            """)
        else:
            st.markdown("""
            **التنقل:**
            - 🏠 الرئيسية : نظرة عامة
            - 📚 حسب الموضوع : حسب التصنيف
            - 🧠 اختبار : اختبر نفسك
            - 🔍 بحث : ابحث بسرعة
            - ⚠️ أحاديث ضعيفة : توثيق
            - 🎥 فيديوهات : محتوى وسائط
            
            **الميزات:**
            - واجهة ثنائية اللغة
            - بحث متقدم
            - اختبار تفاعلي
            - فيديوهات يوتيوب مدمجة
            - تشغيل سلس
            - نسخة محمولة (.exe)
            """)

def create_executable_version(t, lang):
    st.sidebar.markdown("---")
    st.sidebar.subheader("📦 Version Portable" if lang == "fr" else "📦 نسخة محمولة")
    
    with st.sidebar.expander("🚀 Créer version .exe" if lang == "fr" else "🚀 إنشاء نسخة .exe"):
        if lang == "fr":
            st.markdown("""
            **Pour créer le .exe :**
            
            ```bash
            pip install pyinstaller
            pyinstaller --onefile --name "ContradictionsApp" contradictions_app.py
            ```
            
            **Le .exe sera créé dans le dossier 'dist/'**
            
            **Fonctionnalités portables :**
            - ✅ Lancement automatique
            - ✅ Ports automatiques
            - ✅ Interface complète
            - ✅ Sans installation
            """)
        else:
            st.markdown("""
            **لإنشاء ملف .exe:**
            
            ```bash
            pip install pyinstaller
            pyinstaller --onefile --name "ContradictionsApp" contradictions_app.py
            ```
            
            **سيتم إنشاء الملف في مجلد 'dist/'**
            
            **ميزات النسخة المحمولة:**
            - ✅ تشغيل تلقائي
            - ✅ منافذ تلقائية
            - ✅ واجهة كاملة
            - ✅ بدون تثبيت
            """)

# =============================================
# INTERFACE PRINCIPALE
# =============================================

# Menu sidebar
st.sidebar.title("🎯 Navigation")
lang = st.sidebar.radio("🌍 Langue", ["fr", "ar"], format_func=lambda x: "Français" if x == "fr" else "العربية")
t = translations[lang]

# Obtenir les données dans la langue sélectionnée
contradictions_par_themes = contradictions_data[lang]
theme_names = list(contradictions_par_themes.keys())

menu_option = st.sidebar.radio(t["navigation"], t["menu_options"])

# Gestion de l'état de session
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0
if 'quiz_active' not in st.session_state:
    st.session_state.quiz_active = False
if 'quiz_question' not in st.session_state:
    st.session_state.quiz_question = None
if 'show_answer' not in st.session_state:
    st.session_state.show_answer = False
if 'countdown' not in st.session_state:
    st.session_state.countdown = 20

# Flatten toutes les contradictions pour la navigation
all_contradictions = []
for theme, contras in contradictions_par_themes.items():
    for contra in contras:
        contra['theme'] = theme
        all_contradictions.append(contra)

def next_contradiction():
    if st.session_state.current_index < len(all_contradictions) - 1:
        st.session_state.current_index += 1

def prev_contradiction():
    if st.session_state.current_index > 0:
        st.session_state.current_index -= 1

def random_contradiction():
    st.session_state.current_index = random.randint(0, len(all_contradictions) - 1)

def start_quiz():
    st.session_state.quiz_active = True
    st.session_state.quiz_question = random.choice(all_contradictions)
    st.session_state.show_answer = False
    st.session_state.countdown = 20

# Interface principale
st.title(t["title"])
st.subheader(t["subtitle"])
st.markdown(t["cta"])

# Nouvelle fonctionnalité : Version portable
st.markdown(f"""
<div class="portable-feature">
    <h4>🚀 {t['portable_feature']}</h4>
    <p>{t['portable_description']}</p>
</div>
""", unsafe_allow_html=True)

# Appliquer la direction du texte selon la langue
text_direction = "arabic-text" if lang == "ar" else "french-text"
st.markdown(f'<div class="{text_direction}">', unsafe_allow_html=True)

# =============================================
# SECTIONS DE L'APPLICATION
# =============================================

# ACCUEIL
if menu_option == t["menu_options"][0]:
    st.markdown("---")
    
    # Statistiques
    total_contradictions = len(all_contradictions)
    total_themes = len(contradictions_par_themes)
    total_weak_hadiths = sum(len(hadiths) for hadiths in weak_hadiths_data.values())
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(t["stats_contradictions"], total_contradictions)
    with col2:
        st.metric(t["stats_themes"], total_themes)
    with col3:
        st.metric(t["stats_hadiths"], "50+")
    with col4:
        st.metric("⚠️ Hadiths Faibles", total_weak_hadiths)
    
    st.markdown("---")
    
    # Navigation rapide
    st.subheader(t["quick_nav"])
    
    if all_contradictions:
        current = all_contradictions[st.session_state.current_index]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"### {t['bukhari_hadith']}")
            st.info(current["boukhari"])
        
        with col2:
            st.markdown(f"### {t['quran_verse']}")
            st.success(current["coran"])
        
        st.markdown("---")
        st.markdown(f"### {t['contradiction']}")
        st.warning(current["choc"])
        st.markdown(f"**{current['titre']}** • **{t['stats_themes']}:** {current['theme']}")
        
        # Navigation
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button(t["previous"]):
                prev_contradiction()
                st.rerun()
        
        with col2:
            if st.button(t["random"]):
                random_contradiction()
                st.rerun()
        
        with col3:
            if st.button(t["next"]):
                next_contradiction()
                st.rerun()
        
        with col4:
            st.markdown(f"**{st.session_state.current_index + 1} / {len(all_contradictions)}**")
    else:
        st.warning("Aucune contradiction disponible.")

# PARCOURIR PAR THÈME
elif menu_option == t["menu_options"][1]:
    st.subheader(t["browse_by_theme"])
    
    selected_theme = st.selectbox(t["select_theme"], theme_names)
    
    if selected_theme:
        st.markdown(f"### {selected_theme}")
        st.markdown(f"**{len(contradictions_par_themes[selected_theme])} {t['contradictions_in_theme']}**")
        
        for i, contradiction in enumerate(contradictions_par_themes[selected_theme]):
            with st.expander(f"📌 {contradiction['titre']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**{t['bukhari_hadith']}**")
                    st.info(contradiction["boukhari"])
                
                with col2:
                    st.markdown(f"**{t['quran_verse']}**")
                    st.success(contradiction["coran"])
                
                st.markdown(f"**{t['contradiction']}**")
                st.warning(contradiction["choc"])
                
                if st.button(t["see_contradiction"], key=f"view_{selected_theme}_{i}"):
                    for idx, cont in enumerate(all_contradictions):
                        if cont['titre'] == contradiction['titre']:
                            st.session_state.current_index = idx
                            break
                    st.rerun()

# QUIZ
elif menu_option == t["menu_options"][2]:
    st.subheader(t["quiz_title"])
    st.markdown(t["quiz_description"])
    
    if not st.session_state.quiz_active:
        if st.button(t["start_quiz"]):
            start_quiz()
            st.rerun()
    else:
        if st.session_state.quiz_question:
            st.markdown(f"### {t['question']}")
            st.info(f"**{t['bukhari_hadith']}:**\n\n{st.session_state.quiz_question['boukhari']}")
            
            if not st.session_state.show_answer:
                placeholder = st.empty()
                for i in range(st.session_state.countdown, 0, -1):
                    placeholder.markdown(f"### {t['answer_in']} {i}")
                    time.sleep(1)
                
                st.session_state.show_answer = True
                st.rerun()
            else:
                st.markdown(f"### {t['answer']}")
                st.success(f"**{t['quran_verse']}:**\n\n{st.session_state.quiz_question['coran']}")
                st.warning(f"**{t['contradiction']}:**\n\n{st.session_state.quiz_question['choc']}")
                st.markdown(f"**{t['stats_themes']}:** {st.session_state.quiz_question['titre']}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(t["new_question"]):
                        start_quiz()
                        st.rerun()
                with col2:
                    if st.button(t["back_home"]):
                        st.session_state.quiz_active = False
                        st.rerun()

# RECHERCHE AVANCÉE
elif menu_option == t["menu_options"][3]:
    st.subheader(t["search_title"])
    
    col1, col2 = st.columns(2)
    
    with col1:
        search_term = st.text_input(t["search_term"])
        search_themes = st.multiselect(t["filter_theme"], theme_names)
    
    with col2:
        search_type = st.radio(t["search_in"], t["search_options"])
    
    if search_term:
        results = []
        for contra in all_contradictions:
            if search_themes and contra['theme'] not in search_themes:
                continue
                
            search_text = ""
            if search_type == t["search_options"][0]:
                search_text = str(contra).lower()
            elif search_type == t["search_options"][1]:
                search_text = contra['boukhari'].lower()
            elif search_type == t["search_options"][2]:
                search_text = contra['coran'].lower()
            
            if search_term.lower() in search_text:
                results.append(contra)
        
        if results:
            st.write(f"**{len(results)} {t['results_found']}:**")
            
            for i, result in enumerate(results):
                with st.expander(f"{result['titre']} ({result['theme']})"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"**{t['bukhari_hadith']}**")
                        st.info(result["boukhari"])
                    
                    with col2:
                        st.markdown(f"**{t['quran_verse']}**")
                        st.success(result["coran"])
                    
                    st.markdown(f"**{t['contradiction']}**")
                    st.warning(result["choc"])
                    
                    if st.button(t["see_contradiction"], key=f"search_{i}"):
                        st.session_state.current_index = all_contradictions.index(result)
                        st.rerun()
        else:
            st.warning(t["no_results"])

# HADITHS FAIBLES
elif menu_option == t["menu_options"][4]:
    st.subheader(t["weak_hadiths_title"])
    st.markdown(t["weak_hadiths_description"])
    
    if weak_hadiths_data:
        st.success(f"✅ **{sum(len(hadiths) for hadiths in weak_hadiths_data.values())} hadiths faibles chargés avec succès !**")
        
        for theme, hadiths in weak_hadiths_data.items():
            with st.expander(f"📂 {theme} ({len(hadiths)} hadiths)"):
                for i, hadith in enumerate(hadiths):
                    st.markdown(f"**Hadith {i+1}:**")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**Français:**")
                        st.error(hadith['francais'])
                    
                    with col2:
                        st.markdown("**العربية:**")
                        st.markdown(f'<div class="arabic-text">{hadith["arabe"]}</div>', unsafe_allow_html=True)
                    
                    st.markdown("---")
    else:
        st.error("❌ Aucun hadith faible n'a pu être chargé.")

# VIDÉO ÉDUCATIVE
elif menu_option == t["menu_options"][5]:
    display_video_section(t, lang)

# Fermer la div de direction de texte
st.markdown('</div>', unsafe_allow_html=True)

# =============================================
# FONCTIONNALITÉS UTILISATEUR
# =============================================

user_guide(t, lang)
create_executable_version(t, lang)

# Informations
st.sidebar.markdown("---")
st.sidebar.title(t["about_title"])
st.sidebar.markdown(t["about_text"])
st.sidebar.markdown(t["goal"])
st.sidebar.markdown(t["audience"])

st.sidebar.markdown(t["statistics"])
st.sidebar.markdown(f"- {len(all_contradictions)} {t['stats_contradictions'].lower()}")
st.sidebar.markdown(f"- {len(contradictions_par_themes)} {t['stats_themes'].lower()}")
st.sidebar.markdown(f"- 50+ {t['stats_hadiths'].lower()}")
st.sidebar.markdown(f"- {sum(len(hadiths) for hadiths in weak_hadiths_data.values())} hadiths faibles")

# Footer
st.markdown("---")
st.markdown(
    f"""
    <style>
    .footer {{
        position: relative;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #2C3E50;
        color: white;
        text-align: center;
        padding: 15px;
        margin-top: 30px;
        border-radius: 10px;
        font-weight: bold;
    }}
    </style>
    <div class="footer">
    <p>{t['footer_text']}</p>
    </div>
    """,
    unsafe_allow_html=True
)

# =============================================
# LANCEMENT PORTABLE (NOUVEAU)
# =============================================

if __name__ == "__main__":
    # Cette partie s'exécute seulement quand le script est lancé directement
    # et non quand il est importé comme module
    
    # Afficher des informations de débogage
    import subprocess
    import sys
    
    # Trouver un port disponible
    port = find_available_port(8501)
    
    st.sidebar.markdown("---")
    st.sidebar.info(f"**🌐 Port utilisé:** {port}")
    st.sidebar.info(f"**🚀 Mode:** {'Portable' if hasattr(sys, '_MEIPASS') else 'Développement'}")
    
    # Si nous sommes dans un exe PyInstaller
    if hasattr(sys, '_MEIPASS'):
        st.sidebar.success("✅ **Application portable active**")
    else:
        st.sidebar.warning("🛠️ **Mode développement**")