import langcodes
import streamlit as st
from deep_translator import GoogleTranslator
from langdetect import DetectorFactory, LangDetectException, detect
from nltk.tokenize import TreebankWordDetokenizer, wordpunct_tokenize
from spellchecker import SpellChecker

DetectorFactory.seed = 0
MIN_INPUT_LENGTH = 3

SPELL_LANGS = {
    "en",
    "es",
    "fr",
    "pt",
    "de",
    "ru",
    "ar",
    "eu",
    "lv",
    "nl",
}

TARGET_LANGS = {
    "Vietnamese": "vi",
    "English": "en",
    "French": "fr",
    "Japanese": "ja",
    "Chinese": "zh-CN",
    "Korean": "ko",
    "Spanish": "es",
    "German": "de",
}

EXAMPLES_T = [
    "Every morning, I drink a cup of coffee.",
    "Bonjour, comment allez-vous?",
    "Xin chào, hôm nay trời đẹp quá.",
]

EXAMPLES_S = [
    "Yesturday, I recieveed a mesage from my freind.",
    "Definately a great oppurtunity.",
    "Je voudraiis allerr au marchee.",
]

@st.cache_resource(show_spinner=False)
def get_spellchecker(code: str):
    try:
        return SpellChecker(language=code)
    except Exception:
        return None


def language_name(code: str) -> str:
    try:
        return langcodes.Language.get(code).display_name()
    except Exception:
        return code or "Unknown"


def detect_language(raw: str) -> str | None:
    try:
        return detect(raw)
    except LangDetectException:
        return None
    except Exception:
        return None


def fix_typos(text: str, code: str) -> tuple[str, bool]:
    spell = get_spellchecker(code)
    if spell is None:
        return text, False

    tokens = wordpunct_tokenize(text)
    fixed = []

    for token in tokens:
        if token.isalpha() and len(token) > 1:
            suggestion = spell.correction(token.lower()) or token
            if token.istitle():
                suggestion = suggestion.title()
            elif token.isupper():
                suggestion = suggestion.upper()
            fixed.append(suggestion)
        else:
            fixed.append(token)

    return TreebankWordDetokenizer().detokenize(fixed), fixed != tokens


def run_translation(text: str, target_code: str) -> dict:
    raw = text.strip()
    if len(raw) < MIN_INPUT_LENGTH:
        return {"ok": False, "error": f"Nhập tối thiểu {MIN_INPUT_LENGTH} ký tự."}

    source = detect_language(raw)
    if source is None:
        return {"ok": False, "error": "Không nhận diện được ngôn ngữ."}

    if source == target_code:
        return {
            "ok": True,
            "source": language_name(source),
            "target": language_name(target_code),
            "translated": raw,
            "note": "Câu đã ở ngôn ngữ đích, không cần dịch.",
        }

    try:
        translated = GoogleTranslator(source=source, target=target_code).translate(raw)
    except Exception as exc:
        return {"ok": False, "error": f"Lỗi dịch: {exc}"}

    return {
        "ok": True,
        "source": language_name(source),
        "target": language_name(target_code),
        "translated": translated,
    }


def run_spellcheck(text: str) -> dict:
    raw = text.strip()
    if len(raw) < MIN_INPUT_LENGTH:
        return {"ok": False, "error": f"Nhập tối thiểu {MIN_INPUT_LENGTH} ký tự."}

    code = detect_language(raw)
    if code is None:
        return {"ok": False, "error": "Không nhận diện được ngôn ngữ."}

    if code not in SPELL_LANGS:
        return {
            "ok": False,
            "error": f"pyspellchecker chưa hỗ trợ {language_name(code)} ({code}).",
        }

    fixed, changed = fix_typos(raw, code)
    return {
        "ok": True,
        "language": language_name(code),
        "fixed": fixed,
        "changed": changed,
    }


def display_translation_result(res: dict) -> None:
    if not res:
        return

    if res.get("ok"):
        st.caption(f"Nguồn: {res['source']} -> Đích: {res['target']}")
        st.success(res["translated"])
        if res.get("note"):
            st.info(res["note"])
    else:
        st.warning(res.get("error", "Có lỗi xảy ra."))


def display_spellcheck_result(res: dict) -> None:
    if not res:
        return

    if res.get("ok"):
        st.caption(f"Ngôn ngữ: {res['language']}")
        st.success(res["fixed"])
        st.caption("Có sửa lỗi chính tả" if res.get("changed") else "Không phát hiện lỗi")
    else:
        st.warning(res.get("error", "Có lỗi xảy ra."))


def main() -> None:
    st.set_page_config(page_title="NLP Pipeline Demo", layout="centered")
    st.title("Streamlit NLP Pipeline Demo")
    st.caption("Hai ứng dụng: Dịch văn bản - Sửa lỗi chính tả")

    tab_t, tab_s = st.tabs(["Dịch văn bản", "Sửa lỗi chính tả"])

    with tab_t:
        st.session_state.setdefault("res_t", None)

        with st.expander("Ví dụ"):
            for example in EXAMPLES_T:
                st.markdown(f"- {example}")

        with st.form("form_translate"):
            text_t = st.text_area(
                "Câu cần dịch",
                height=120,
                placeholder="Nhập câu ở bất kỳ ngôn ngữ nào...",
            )
            target = st.selectbox("Dịch sang", list(TARGET_LANGS.keys()))
            submitted_t = st.form_submit_button("Dịch", type="primary")

            if submitted_t:
                st.session_state.res_t = run_translation(text_t, TARGET_LANGS[target])

        display_translation_result(st.session_state.res_t)

    with tab_s:
        st.session_state.setdefault("res_s", None)

        with st.expander("Ví dụ"):
            for example in EXAMPLES_S:
                st.markdown(f"- {example}")

        st.caption(f"Hỗ trợ: {', '.join(sorted(SPELL_LANGS))}")

        with st.form("form_spell"):
            text_s = st.text_area(
                "Câu cần kiểm tra",
                height=120,
                placeholder="Nhập câu để kiểm tra chính tả...",
            )
            submitted_s = st.form_submit_button("Kiểm tra", type="primary")

            if submitted_s:
                st.session_state.res_s = run_spellcheck(text_s)

        display_spellcheck_result(st.session_state.res_s)


if __name__ == "__main__":
    main()
