export function showToast(message, severity = "info", duration = 4000) {
    let container = document.getElementById("toast-container");
    if (!container) {
        container = document.createElement("div");
        container.id = "toast-container";
        document.body.appendChild(container);
    }

    const icons = {
        info: "fa-circle-info",
        warning: "fa-triangle-exclamation",
        error: "fa-circle-xmark",
        success: "fa-circle-check"
    };

    const toast = document.createElement("div");
    toast.className = `toast toast-${severity}`;
    toast.setAttribute("role", "alert");
    toast.innerHTML = `<i class="fas ${icons[severity] || icons.info}"></i><span>${message}</span>`;
    container.appendChild(toast);

    requestAnimationFrame(() => toast.classList.add("show"));

    setTimeout(() => {
        toast.classList.remove("show");
        setTimeout(() => toast.remove(), 300);
    }, duration);
}

export function highlightInput(inputTextbox) {
    const container = inputTextbox.closest(".text-area-container") || inputTextbox;
    inputTextbox.scrollIntoView({ behavior: "smooth", block: "center" });
    inputTextbox.focus({ preventScroll: true });

    container.classList.remove("input-attention");
    void container.offsetWidth; // Force reflow
    container.classList.add("input-attention");
    setTimeout(() => container.classList.remove("input-attention"), 1900);
}
