// Global Theme Manager for AI Facial Beauty Analyzer
(function () {
    const DEFAULT_THEME = "theme-glass";
    const savedTheme = localStorage.getItem("beautyTheme") || DEFAULT_THEME;

    // Apply theme immediately to prevent FOUC (Flash of Unstyled Content)
    document.documentElement.className = savedTheme;
    document.addEventListener("DOMContentLoaded", () => {
        document.body.className = savedTheme;
        
        // Setup dropdown theme selector if it exists
        const themeSelector = document.getElementById("themeSelector");
        if (themeSelector) {
            themeSelector.value = savedTheme;
            themeSelector.addEventListener("change", (e) => {
                const newTheme = e.target.value;
                localStorage.setItem("beautyTheme", newTheme);
                document.documentElement.className = newTheme;
                document.body.className = newTheme;
            });
        }
    });
})();
