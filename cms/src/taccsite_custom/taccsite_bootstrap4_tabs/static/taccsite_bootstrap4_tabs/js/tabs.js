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

        trigger.focus();
        trigger.click();
    };

    showFromHash();
    window.addEventListener('hashchange', showFromHash);
}

/**
 * Support accessibility that Bootstrap 4 lacks:
 * - keyboard navigation (supports wraparound)
 * - roving tabindex (kept in sync with activation)
 */
function handleA11y() {
    /* To manage `tabindex` */
    /* https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/#kbd_roving_tabindex */
    function getTabs(tablist) {
        return Array.from(tablist.querySelectorAll('[role="tab"]'));
    }
    function updateTabindexes(tablist, activeTab) {
        getTabs(tablist).forEach(t => t.tabIndex = (t === activeTab ? 0 : -1));
    }
    function activateTab(tablist, tab) {
        if (!tab) return;
        try { tab.focus(); } catch (e) {}
        if (typeof tab.click === 'function') tab.click();
        updateTabindexes(tablist, tab);
    }
    function seedInitialTabindex(tablist) {
        const tabs = getTabs(tablist);
        if (!tabs.length) return;
        let initialTab = tabs.find(tab => {
            const isActive = tab.classList.contains('active');
            const isAriaSelected = (tab.getAttribute('aria-selected') === 'true');

            return isActive || isAriaSelected;
        }) || tabs[0];

    // updateTabindexes expects (tablist, activeTab)
    updateTabindexes(tablist, initialTab);
    }

    document.querySelectorAll('[role="tablist"]').forEach(tablist => {
        /* To add keyboard navigation (←,↑,→,↓,home,end) */
        tablist.addEventListener('keydown', (event) => {
            const tabs = getTabs(tablist);
            if (!tabs.length) return;

            let current = tabs.indexOf(document.activeElement);
            if (current === -1) {
                current = tabs.findIndex(t => t.classList.contains('active') || t.getAttribute('aria-selected') === 'true');
            }
            if (current === -1) current = 0;

            let nextIndex = null;
            switch (event.key) {
                case 'ArrowLeft':
                case 'ArrowUp':
                    nextIndex = (current - 1 + tabs.length) % tabs.length;
                    break;
                case 'ArrowRight':
                case 'ArrowDown':
                    nextIndex = (current + 1) % tabs.length;
                    break;
                case 'Home':
                    nextIndex = 0;
                    break;
                case 'End':
                    nextIndex = tabs.length - 1;
                    break;
                default:
                    return;
            }

            event.preventDefault();
            activateTab(tablist, tabs[nextIndex]);
        });

        tablist.addEventListener('click', (event) => {
            const tab = event.target.closest('[role="tab"]');
            if (tab) updateTabindexes(tablist, tab);
        });

        seedInitialTabindex(tablist);
    });
}

/** To enable all handling */
function handleTabLinks() {
    handleDefaultTabLinks();
    handleExtraTabLinks();
    handleTabsFromURL();
    handleA11y();
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', handleTabLinks);
} else {
    handleTabLinks();
}
