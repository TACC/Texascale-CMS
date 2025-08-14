let _ignoreNextHashChange = false;

/** To custom handle default tab links such that tab click changes URL */
function handleDefaultTabLinks() {
    document.querySelectorAll('[id^="tab-label"]').forEach(tabLink => {
        tabLink.addEventListener('click', (event) => {
            // To prevent handleTabsFromURL from reacting to the hashchange that a genuine user click will cause. Only set the flag for trusted (user) clicks, so programmatic activations aren't treated the same.
            if (event && event.isTrusted) {
                _ignoreNextHashChange = true;
            }

            $(tabLink).tab('show');
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
        if (_ignoreNextHashChange) {
            _ignoreNextHashChange = false;
            console.info('Ignoring hash change');
            return;
        }

        const id = (window.location.hash || '').replace(/^#tab-/, '');
        if (!id) return;

        const trigger = document.getElementById(`tab-label-${id}`);
        if (!trigger) return console.info('Tab trigger not found:', id);

        trigger.click();
    };

    showFromHash();
    window.addEventListener('hashchange', showFromHash);
}

/** To call all handling */
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
