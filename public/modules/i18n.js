import translations from '../translations.js';
import { state } from './state.js';

export function getTranslation(key) {
    const dict = translations[state.page_language] || translations["pt-BR"];
    return dict[key];
}

export function setLanguage(lang, onLanguageChanged) {
    state.page_language = lang;
    document.documentElement.lang = lang;

    const dict = translations[lang] || translations["pt-BR"];

    if (dict.page_title) {
        document.title = dict.page_title;
    }
    const metaDesc = document.querySelector('meta[name="description"]');
    if (metaDesc && dict.meta_description) {
        metaDesc.setAttribute("content", dict.meta_description);
    }

    document.querySelectorAll("[data-i18n]").forEach(elem => {
        const key = elem.getAttribute("data-i18n");
        if (dict[key] !== undefined) {
            elem.textContent = dict[key];
        }
    });

    document.querySelectorAll("[data-i18n-placeholder]").forEach(elem => {
        const key = elem.getAttribute("data-i18n-placeholder");
        if (dict[key] !== undefined) {
            elem.setAttribute("placeholder", dict[key]);
        }
    });
    updateLangMenu(lang);
    if (onLanguageChanged) {
        onLanguageChanged();
    }
}

function updateLangMenu(lang) {
    const labelElem = document.querySelector("#current-lang-label");
    if (!labelElem) return;

    if (lang === "pt-BR") {
        labelElem.innerHTML = "🇧🇷 Português";
    } else if (lang === "en") {
        labelElem.innerHTML = "🇺🇸 English";
    } else if (lang === "zh") {
        labelElem.innerHTML = "🇨🇳 中文";
    }

    const buttons = document.querySelectorAll("#lang_dropdown button[data-lang]");
    buttons.forEach(btn => {
        if (btn.getAttribute("data-lang") === lang) {
            btn.className = "w-full text-left flex items-center gap-3 px-4 py-2 bg-blue-50 text-blue-600 font-semibold";
        } else {
            btn.className = "w-full text-left flex items-center gap-3 px-4 py-2 text-gray-700 hover:bg-gray-50";
        }
    });

    const details = document.querySelector("#lang_dropdown");
    if (details) {
        details.removeAttribute("open");
    }
}
