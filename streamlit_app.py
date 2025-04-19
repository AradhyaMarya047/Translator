# --- Required Libraries ---
import streamlit as st
import requests
import streamlit.components.v1 as components

# --- Streamlit Page Setup ---
st.set_page_config(
    page_title="French Translator",
    page_icon="🈺",
    layout="wide"
)

# --- Marquee Banner (Scrolling Header) ---
st.markdown("""
<marquee behavior="scroll" direction="left" scrollamount="8" style="
    background-color: #FBCEB1; 
    color: black; 
    padding: 10px 0; 
    font-weight: bold;
    font-size: 22px;
">
🔥 More language options in future 🔤
</marquee>
""", unsafe_allow_html=True)

# --- Gradient Background Animation ---
page_bg_style = """
<style>
    .stApp {
        background: linear-gradient(135deg, #a2d5f2, #f4c4f3, #fef6e4);
        background-size: 400% 400%;
        animation: gradientShift 20s ease infinite;
    }
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    html, body, [class*="css"] {
        color: #222222 !important;
    }
</style>
"""
st.markdown(page_bg_style, unsafe_allow_html=True)

# --- Title Header ---
st.markdown("<h1 style='text-align: center; color: #002244;'>🌍 Real-Time English ➜ French Translator</h1>", unsafe_allow_html=True)
st.divider()

# --- Text Input ---
st.markdown("<h3 style='text-align: center; color: #002244;'>📝 Enter your text:</h3>", unsafe_allow_html=True)
user_input = st.text_area(" ", placeholder="Type a sentence in English to translate into French...", height=150)

# --- Translate Button Centered ---
btn_col1, btn_col2, btn_col3 = st.columns([1, 2, 1])
with btn_col2:
    translate_clicked = st.button("🔄 Translate", key="translate_btn", use_container_width=True)

# --- On Button Click ---
if translate_clicked:
    if not user_input.strip():
        st.error("Please enter some text to translate.")
    else:
        # 🚨 Call Validation API
        validation_response = requests.post("http://127.0.0.1:8000/validate", json={"text": user_input})

        if validation_response.status_code == 200:
            val_data = validation_response.json()

            if not val_data["success"]:
                # Show validation errors
                st.error("❌ Input validation failed. Please fix the following:")
                for issue in val_data["details"]:
                    st.markdown(f"- {issue}")
            else:
                # Proceed with translation
                st.success("✅ Input is valid. Proceeding with translation...")
                with st.spinner("Translating... Please wait."):
                    try:
                        response = requests.post("http://127.0.0.1:8000/translate", json={"text": user_input})
                        if response.status_code == 200:
                            result = response.json()
                            translated_text = result["translated_text"]

                            # --- Translated Output Display ---
                            st.success("✅ Translation Successful!")
                            st.markdown("<h3 style='text-align: center; color: #002244;'>🔤 Translated Text (French):</h3>", unsafe_allow_html=True)
                            st.markdown(
                                f"<div style='background-color:#ccf5ff;padding:18px;border-radius:10px;font-size:22px;color:#002244;text-align:center;'>{translated_text}</div>",
                                unsafe_allow_html=True
                            )

                            # --- Auto-Speak (Text to Speech) ---
                            components.html(
                                f"""
                                <script>
                                var utterance = new SpeechSynthesisUtterance("{translated_text}");
                                utterance.lang = "fr-FR";
                                speechSynthesis.speak(utterance);
                                </script>
                                """,
                                height=0
                            )

                            # --- Speak Again Button ---
                            st.markdown("<h4 style='text-align: center; color: #002244;'>🔊 Hear it Again:</h4>", unsafe_allow_html=True)
                            components.html(
                                f"""
                                <script>
                                function speakText() {{
                                    var utterance = new SpeechSynthesisUtterance("{translated_text}");
                                    utterance.lang = "fr-FR";
                                    speechSynthesis.speak(utterance);
                                }}
                                </script>
                                <div style='text-align:center;'>
                                    <button onclick="speakText()" style="padding:12px 24px;font-size:16px;background-color:#005a9c;color:white;border:none;border-radius:8px;cursor:pointer;">
                                        ▶ Speak Again
                                    </button>
                                </div>
                                """,
                                height=100,
                            )

                            # --- Display BLEU & Perplexity Scores ---
                            st.markdown(f"<p style='text-align: center; font-size: 20px; color: #002244;'><strong>📊 BLEU Score:</strong> {round(result['bleu_score'], 4)} &nbsp; | &nbsp; <strong>📈 Perplexity:</strong> {round(result['perplexity'], 2)}</p>", unsafe_allow_html=True)

                            # --- Performance Metrics ---
                            st.markdown("<h4 style='text-align: center; color: #002244;'>📟 System Performance</h4>", unsafe_allow_html=True)
                            st.markdown(f"<p style='text-align: center; color: #222222;'>🕒 Response Time: <strong>{result['response_time']}s</strong><br>💾 Memory Usage: <strong>{result['memory_usage_MB']} MB</strong><br>📥 Total Requests: <strong>{result['total_requests']}</strong></p>", unsafe_allow_html=True)

                            if result["memory_usage_MB"] > 200:
                                st.warning("⚠️ High memory usage detected!")

                            # 🎉 Confetti Celebration
                            components.html(
                                """
                                <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
                                <script>
                                var end = Date.now() + 1000;
                                (function frame() {
                                    confetti({ particleCount: 4, angle: 60, spread: 60, origin: { x: 0 } });
                                    confetti({ particleCount: 4, angle: 120, spread: 60, origin: { x: 1 } });
                                    if (Date.now() < end) requestAnimationFrame(frame);
                                }());
                                </script>
                                """,
                                height=0
                            )
                        else:
                            st.error(f"API Error: {response.status_code}")
                    except Exception as e:
                        st.exception(f"Translation failed: {e}")
        else:
            st.error("🚫 Could not connect to validation endpoint.")

# --- Footer ---
st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 14px; color: #002244;'>Made by <strong>Aradhya Marya</strong></p>", unsafe_allow_html=True)
