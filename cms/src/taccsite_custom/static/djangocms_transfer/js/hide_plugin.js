/** To hide PluginImporter plugin from list for admins editing page */

const itemQuery = '[href="PluginImporter"]';
const cmsUiWrap = document.getElementById('cms-top');

function disableItem(item) {
    item.classList.add('js-disabled');
}

// Hide current items
const utilPluginMenuItem = (cmsUiWrap) && cmsUiWrap.querySelector(itemQuery);
if (utilPluginMenuItem) disableItem(utilPluginMenuItem);

// Hide future items
const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
        mutation.addedNodes.forEach((node) => {
            const isElement = node.nodeType === Node.ELEMENT_NODE;
            const item = (isElement) && node.querySelector(itemQuery);
            if (item) disableItem(item);
        });
    });
});
observer.observe(cmsUiWrap, { childList: true, subtree: true });
