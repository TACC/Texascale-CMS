/** To hide PluginImporter plugin from list for admins editing page */

const itemQuery = '[href="PluginImporter"]';
const cmsUiWrapper = document.getElementById('cms-top');

function disableItem(item) {
    item.classList.add('js-disabled');
}

// Hide current items
const utilPluginMenuItem = cmsUiWrapper.querySelector(itemQuery);
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
observer.observe(cmsUiWrapper, { childList: true, subtree: true });
