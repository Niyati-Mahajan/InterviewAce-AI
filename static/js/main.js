document.querySelectorAll("[data-demo-action]").forEach((button) => {
  button.addEventListener("click", () => {
    button.blur();
  });
});

// Theme preference is shared across all pages that include this file.
const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const savedTheme = localStorage.getItem("interviewace-theme") || "light";
document.documentElement.dataset.theme = savedTheme;

document.querySelectorAll("[data-theme-toggle]").forEach((toggle) => {
  const syncLabel = () => {
    const isDark = document.documentElement.dataset.theme === "dark";
    toggle.textContent = isDark ? "Light" : "Dark";
    toggle.setAttribute("aria-pressed", String(isDark));
  };

  syncLabel();
  toggle.addEventListener("click", () => {
    const nextTheme = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
    document.documentElement.dataset.theme = nextTheme;
    localStorage.setItem("interviewace-theme", nextTheme);
    document.querySelectorAll("[data-theme-toggle]").forEach((button) => {
      button.textContent = nextTheme === "dark" ? "Light" : "Dark";
      button.setAttribute("aria-pressed", String(nextTheme === "dark"));
    });
  });
});

const interviewForm = document.querySelector("[data-interview-form]");
const timerDisplay = document.querySelector("[data-countdown-timer]");

if (interviewForm && timerDisplay) {
  let remainingSeconds = Number(interviewForm.dataset.remainingSeconds || 0);
  const timeUpField = interviewForm.querySelector("[data-time-up-field]");
  const answerBox = interviewForm.querySelector("textarea[name='student_answer']");
  const loader = interviewForm.querySelector("[data-ai-loader]");

  const showEvaluationLoader = () => {
    if (loader) {
      loader.hidden = false;
    }

    interviewForm.querySelectorAll("button, a, textarea, select").forEach((control) => {
      control.setAttribute("aria-disabled", "true");

      if (control.tagName === "TEXTAREA") {
        control.readOnly = true;
      } else if (control.tagName !== "A") {
        control.disabled = true;
      }
    });
  };

  // Show a loading state and prevent duplicate clicks while Gemini evaluates.
  interviewForm.addEventListener("submit", () => {
    showEvaluationLoader();
  });

  const formatTimer = (seconds) => {
    const minutes = Math.floor(seconds / 60);
    const remaining = seconds % 60;
    return `${String(minutes).padStart(2, "0")}:${String(remaining).padStart(2, "0")}`;
  };

  const submitOnTimeout = () => {
    if (timeUpField) {
      timeUpField.value = "1";
    }

    if (answerBox) {
      answerBox.removeAttribute("required");
    }

    showEvaluationLoader();
    interviewForm.submit();
  };

  timerDisplay.textContent = formatTimer(remainingSeconds);

  const countdown = window.setInterval(() => {
    remainingSeconds -= 1;
    timerDisplay.textContent = formatTimer(Math.max(remainingSeconds, 0));

    if (remainingSeconds <= 60) {
      timerDisplay.classList.add("is-warning");
    }

    if (remainingSeconds <= 0) {
      window.clearInterval(countdown);
      submitOnTimeout();
    }
  }, 1000);
}

// ChatGPT-style progressive reveal for AI-generated feedback sections.
document.querySelectorAll("[data-typewriter]").forEach((node) => {
  const text = node.textContent.trim();

  if (!text || prefersReducedMotion) {
    node.textContent = text;
    return;
  }

  node.textContent = "";
  node.classList.add("typing-text");

  let index = 0;
  const type = () => {
    node.textContent = text.slice(0, index);
    index += 1;

    if (index <= text.length) {
      window.setTimeout(type, 12);
    } else {
      node.classList.remove("typing-text");
    }
  };

  type();
});
