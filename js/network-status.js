// Network Status Indicator
(function() {
    // Create network status element
    function createNetworkIndicator() {
        const indicator = document.createElement('div');
        indicator.id = 'network-status';
        indicator.className = 'network-indicator offline';
        indicator.innerHTML = `
            <span class="network-icon">📡</span>
            <span class="network-text">Offline - Using cached data</span>
        `;
        document.body.appendChild(indicator);
        return indicator;
    }

    // Initialize indicator
    const indicator = createNetworkIndicator();

    // Update status function
    function updateNetworkStatus() {
        if (navigator.onLine) {
            indicator.className = 'network-indicator online';
            indicator.innerHTML = `
                <span class="network-icon">📶</span>
                <span class="network-text">Online</span>
            `;
            // Hide after 2 seconds when online
            setTimeout(() => {
                indicator.classList.add('hide');
            }, 2000);
        } else {
            indicator.className = 'network-indicator offline';
            indicator.innerHTML = `
                <span class="network-icon">📡</span>
                <span class="network-text">Offline - Using cached data</span>
            `;
            indicator.classList.remove('hide');
        }
    }

    // Event listeners
    window.addEventListener('online', updateNetworkStatus);
    window.addEventListener('offline', updateNetworkStatus);

    // Initial check
    updateNetworkStatus();

    // Register service worker
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', function() {
            navigator.serviceWorker.register('/sw.js')
                .then(function(registration) {
                    console.log('ServiceWorker registered: ', registration.scope);
                })
                .catch(function(error) {
                    console.log('ServiceWorker registration failed: ', error);
                });
        });
    }

    // Add PWA install prompt
    let deferredPrompt;
    const installBanner = document.createElement('div');
    installBanner.id = 'install-banner';
    installBanner.className = 'install-banner';
    installBanner.innerHTML = `
        <span>📱 Install SGAC App for better experience</span>
        <button id="install-btn">Install</button>
        <button id="dismiss-btn">✕</button>
    `;

    window.addEventListener('beforeinstallprompt', (e) => {
        e.preventDefault();
        deferredPrompt = e;
        document.body.appendChild(installBanner);
        
        document.getElementById('install-btn').addEventListener('click', async () => {
            deferredPrompt.prompt();
            const { outcome } = await deferredPrompt.userChoice;
            if (outcome === 'accepted') {
                installBanner.remove();
            }
            deferredPrompt = null;
        });

        document.getElementById('dismiss-btn').addEventListener('click', () => {
            installBanner.remove();
        });
    });

    window.addEventListener('appinstalled', () => {
        installBanner.remove();
        console.log('PWA installed');
    });
})();
