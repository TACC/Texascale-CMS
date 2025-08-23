/** To make tab click change URL */
function handleDefaultTabLinks() {
    document.querySelectorAll('[id^="tab-label"]').forEach(tabLink => {
        tabLink.addEventListener('click', () => {
            history.replaceState(null, null, tabLink.hash);
        });
    });
}

/** To allow custom links to toggle Bootstrap tabs */
function handleExtraTabLinks() {
    document.querySelectorAll('[data-toggle-target]').forEach(tabLink => {
        tabLink.addEventListener('click', () => {
            const tabId = tabLink.hasAttribute('href')
                        ? tabLink.href.split('#')[1]
                        : tabLink.dataset.toggleTarget;
            const tabTrigger = document.querySelector(`[href="#${tabId}"]`);

            if (!tabTrigger) return console.info('Tab trigger not found:', tabId);

            tabTrigger.click();
        });
    });
}

/** To show correct tab when URL has/changes hash */
function handleTabsFromURL() {
    function showFromHash() {
        const id = (window.location.hash || '').replace(/^#tab-/, '');
        if (!id) return;

        const trigger = document.getElementById(`tab-label-${id}`);
        if (!trigger) return console.info('Tab trigger not found:', id);

        trigger.click();
    };

    showFromHash();
    window.addEventListener('hashchange', showFromHash);
}

/** To add keyboard navigation (←,↑,→,↓,home,end) */
function handleTabKeyboardNavigation() {
    document.querySelectorAll('[role="tablist"]').forEach(tablist => {
        tablist.addEventListener('keydown', (event) => {
            const key = event.key;
            const tabs = Array.from(tablist.querySelectorAll('[role="tab"]'));
            if (!tabs.length) return;

            // Try to determine currently focused/active tab
            let currentIndex = tabs.indexOf(document.activeElement);
            if (currentIndex === -1) {
                currentIndex = tabs.findIndex(t => t.getAttribute('aria-selected') === 'true' || t.classList.contains('active'));
            }
            if (currentIndex === -1) currentIndex = 0;

            let newIndex = -1;
            if (key === 'ArrowLeft' || key === 'ArrowUp') {
                newIndex = (currentIndex > 0) ? currentIndex - 1 : tabs.length - 1;
            } else if (key === 'ArrowRight' || key === 'ArrowDown') {
                newIndex = (currentIndex + 1) % tabs.length;
            } else if (key === 'Home') {
                newIndex = 0;
            } else if (key === 'End') {
                newIndex = tabs.length - 1;
            } else {
                return; // ignore other keys
            }

            event.preventDefault();
            const next = tabs[newIndex];
            if (!next) return;

            // Focus and activate the tab. Using click() keeps behavior consistent with existing handlers.
            try { next.focus(); } catch (e) { /* ignore focus failures */ }
            if (typeof next.click === 'function') next.click();
        });
    });
}

/** To support "roving tabindex" (manage `tabindex` attribute) */
/* https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/#kbd_roving_tabindex */
function handleRovingTabindex() {
    document.querySelectorAll('[role="tablist"]').forEach(tablist => {
        function updateTabindexes(activeTab) {
            const tabs = Array.from(tablist.querySelectorAll('[role="tab"]'));
            tabs.forEach(tab => {
                try {
                    tab.setAttribute('tabindex', tab === activeTab ? '0' : '-1');
                } catch (e) { /* ignore */ }
            });
        }

        // initialize based on currently active tab (by class or aria-selected)
        const tabs = Array.from(tablist.querySelectorAll('[role="tab"]'));
        let active = tabs.find(t => t.classList.contains('active') || t.getAttribute('aria-selected') === 'true');
        if (!active && tabs.length) active = tabs[0];
        if (active) updateTabindexes(active);

        // update roving tabindex when a tab is clicked/activated
        tabs.forEach(tab => {
            tab.addEventListener('click', () => updateTabindexes(tab));
        });
    });
}

/** To enable all handling */
function handleTabLinks() {
    handleDefaultTabLinks();
    handleExtraTabLinks();
    handleTabsFromURL();
    handleTabKeyboardNavigation();
    handleRovingTabindex();
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', handleTabLinks);
} else {
    handleTabLinks();
}
