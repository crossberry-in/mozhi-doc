// ============================================================
// Mozhi Dev Server — Frontend JavaScript
// Loads .mz components and renders them into #app
// ============================================================

// Load a component from the server
async function loadComponent(name) {
    try {
        const res = await fetch('/components/' + name + '.mz');
        if (res.ok) {
            return await res.text();
        }
        return '<div class="card"><p>Component "' + name + '" not found</p></div>';
    } catch (e) {
        return '<div class="card"><p>Error loading ' + name + ': ' + e.message + '</p></div>';
    }
}

// Render all components
async function render() {
    const app = document.getElementById('app');

    // Show loading state
    app.innerHTML = '<p style="text-align:center;padding:2rem;">Loading...</p>';

    // Load components in parallel
    const [header, card, counter, footer] = await Promise.all([
        loadComponent('header'),
        loadComponent('card'),
        loadComponent('counter'),
        loadComponent('footer')
    ]);

    // Render to DOM
    app.innerHTML = header + card + counter + footer;

    console.log('[mozhi-dev] Components rendered');
}

// Initial render
render();

// Listen for live reload events (injected by dev_server.mz)
// The EventSource connection is created by the injected script
console.log('[mozhi-dev] App loaded');
