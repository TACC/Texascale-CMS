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

/** To enable all handling */
function handleTabLinks() {
    handleDefaultTabLinks();
    handleExtraTabLinks();
    handleTabsFromURL();
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', handleTabLinks);
} else {
    handleTabLinks();
}
