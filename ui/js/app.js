/**
 * PaperLens Mini - Frontend JavaScript
 * Simplified version without AI/ML features
 */

// Global state
let currentPapers = [];
let currentStep = 1;

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    console.log('[Init] PaperLens Mini loading...');
    
    // Show loading screen
    showLoadingScreen();
    updateLoadingStatus('Initializing components...');
    
    // Set default from year (current year - 3)
    const currentYear = new Date().getFullYear();
    const defaultFromYear = currentYear - 3;
    const fromYearInput = document.getElementById('from-year');
    if (fromYearInput) {
        fromYearInput.value = defaultFromYear;
        console.log(`[Init] Default from year set to: ${defaultFromYear}`);
    }
    
    // Initialize components
    initWizard();
    initSearchHandlers();
    initVisualizationHandlers();
    initExportHandlers();
    
    // Load dark mode preference
    loadDarkMode();
    
    // Setup scroll listener
    const mainContent = document.querySelector('.main-content');
    if (mainContent) {
        mainContent.addEventListener('scroll', updateScrollButton);
    }
    
    updateLoadingStatus('Loading interface...');
    
    // Hide loading screen after short delay
    setTimeout(() => {
        hideLoadingScreen();
        console.log('[Init] ✓ PaperLens Mini ready');
        console.log(`[Init] Max results: 300, From year: ${defaultFromYear}`);
    }, 500);
});

// Loading Screen
function showLoadingScreen() {
    const loadingScreen = document.getElementById('loading-screen');
    const mainContainer = document.getElementById('main-container');
    if (loadingScreen) {
        loadingScreen.style.display = 'flex';
        loadingScreen.classList.remove('fade-out');
    }
    if (mainContainer) {
        mainContainer.style.display = 'none';
    }
}

function hideLoadingScreen() {
    const loadingScreen = document.getElementById('loading-screen');
    const mainContainer = document.getElementById('main-container');
    
    if (loadingScreen) {
        loadingScreen.classList.add('fade-out');
        setTimeout(() => {
            loadingScreen.style.display = 'none';
            if (mainContainer) {
                mainContainer.style.display = 'flex';
            }
        }, 500);
    }
}

function updateLoadingStatus(text) {
    const statusElement = document.getElementById('loading-status');
    if (statusElement) {
        statusElement.textContent = text;
    }
}

// Wizard Functions
function initWizard() {
    updateWizardSteps();
    
    const wizardSteps = document.querySelectorAll('.wizard-step');
    wizardSteps.forEach(step => {
        step.addEventListener('click', () => {
            const stepNumber = parseInt(step.dataset.step);
            if (!step.classList.contains('disabled')) {
                goToStep(stepNumber);
            }
        });
    });
}

function goToStep(step) {
    currentStep = step;
    
    // Show corresponding page
    const pages = ['search', 'visualization', 'export'];
    const pageName = pages[step - 1];
    showPage(pageName);
    
    updateWizardSteps();
    updateFixedNavigation();
    
    // Scroll to top
    document.querySelector('.main-content').scrollTop = 0;
}

function updateWizardSteps() {
    const wizardSteps = document.querySelectorAll('.wizard-step');
    wizardSteps.forEach((step, index) => {
        step.classList.remove('active', 'completed');
        if (index + 1 === currentStep) {
            step.classList.add('active');
        } else if (index + 1 < currentStep) {
            step.classList.add('completed');
        }
    });
}

function showPage(pageName) {
    const pages = document.querySelectorAll('.page');
    pages.forEach(page => page.classList.remove('active'));
    
    const targetPage = document.getElementById(`${pageName}-page`);
    if (targetPage) {
        targetPage.classList.add('active');
    }
}

function updateFixedNavigation() {
    const fixedNav = document.getElementById('fixed-nav');
    const backBtn = document.getElementById('back-btn');
    const nextBtn = document.getElementById('next-btn');
    
    if (!fixedNav) return;
    
    if (currentPapers.length > 0 || currentStep > 1) {
        fixedNav.style.display = 'flex';
        
        // Update back button
        backBtn.style.display = currentStep === 1 ? 'none' : 'flex';
        
        // Update next button
        if (currentStep === 3) {
            nextBtn.innerHTML = '<i class="fas fa-redo"></i> Restart';
            nextBtn.onclick = () => goToStep(1);
        } else {
            nextBtn.innerHTML = 'Next <i class="fas fa-arrow-right"></i>';
            nextBtn.onclick = goToNextStep;
        }
    } else {
        fixedNav.style.display = 'none';
    }
}

function goToPreviousStep() {
    if (currentStep > 1) {
        goToStep(currentStep - 1);
    }
}

function goToNextStep() {
    if (currentStep < 3) {
        goToStep(currentStep + 1);
    }
}

// Search Handlers
function initSearchHandlers() {
    const searchBtn = document.getElementById('search-btn');
    const searchQuery = document.getElementById('search-query');
    
    searchBtn.addEventListener('click', handleSearch);
    searchQuery.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleSearch();
        }
    });
}

async function handleSearch() {
    const query = document.getElementById('search-query').value.trim();
    const source = document.getElementById('source-select').value;
    const maxResults = parseInt(document.getElementById('max-results').value);
    const fromYear = document.getElementById('from-year').value;
    
    if (!query) {
        showStatus('search-status', 'Please enter search keywords', 'error');
        return;
    }
    
    const searchBtn = document.getElementById('search-btn');
    searchBtn.disabled = true;
    searchBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Searching...';
    
    try {
        console.log('[Search] Starting search:', { query, source, maxResults, fromYear });
        
        const params = {
            query: query,
            source: source,
            max_results: maxResults,
            from_year: fromYear ? parseInt(fromYear) : null
        };
        
        const result = await pywebview.api.search_papers(params);
        
        if (result.success) {
            currentPapers = result.papers;
            displayPapers(result.papers);
            showStatus('search-status', `Found ${result.count} papers`, 'success');
            
            // Enable next steps
            updateWizardSteps();
            updateFixedNavigation();
            
            console.log('[Search] ✓ Found', result.count, 'papers');
        } else {
            showStatus('search-status', `Error: ${result.error}`, 'error');
            console.error('[Search] ✗ Error:', result.error);
        }
    } catch (error) {
        console.error('[Search] ✗ Exception:', error);
        showStatus('search-status', `Error: ${error.message}`, 'error');
    } finally {
        searchBtn.disabled = false;
        searchBtn.innerHTML = '<i class="fas fa-search"></i> Search';
    }
}

function displayPapers(papers) {
    const papersList = document.getElementById('papers-list');
    const placeholder = document.getElementById('search-placeholder');
    
    if (placeholder) {
        placeholder.style.display = 'none';
    }
    
    if (papers.length === 0) {
        papersList.innerHTML = '<div class="search-placeholder"><p>No papers found</p></div>';
        return;
    }
    
    const papersHTML = papers.map(paper => `
        <div class="paper-item">
            <div class="paper-title">
                ${paper.url ? `<a href="${paper.url}" target="_blank">${escapeHtml(paper.title)}</a>` : escapeHtml(paper.title)}
            </div>
            ${paper.authors && paper.authors.length > 0 ? `
                <div class="paper-authors">
                    ${paper.authors.slice(0, 3).join(', ')}${paper.authors.length > 3 ? ' et al.' : ''}
                </div>
            ` : ''}
            <div class="paper-meta">
                <span><i class="fas fa-calendar"></i> ${paper.publication_date || 'N/A'}</span>
                <span><i class="fas fa-book"></i> ${paper.journal || 'N/A'}</span>
                <span><i class="fas fa-quote-right"></i> ${paper.citations || 0} citations</span>
                <span><i class="fas fa-database"></i> ${paper.source}</span>
                ${paper.doi ? `<span><i class="fas fa-link"></i> ${paper.doi}</span>` : ''}
            </div>
            ${paper.abstract ? `
                <div class="paper-abstract">
                    ${truncateText(escapeHtml(paper.abstract), 300)}
                </div>
            ` : ''}
        </div>
    `).join('');
    
    papersList.innerHTML = papersHTML;
}

// Visualization Handlers
function initVisualizationHandlers() {
    const generateBtn = document.getElementById('generate-viz');
    generateBtn.addEventListener('click', handleVisualization);
}

async function handleVisualization() {
    if (currentPapers.length === 0) {
        showStatus('viz-status', 'No papers to visualize', 'error');
        return;
    }
    
    // Check if Plotly is loaded
    if (typeof Plotly === 'undefined') {
        showStatus('viz-status', 'Plotly.js not loaded. Please check your internet connection.', 'error');
        console.error('[Viz] Plotly.js is not loaded!');
        return;
    }
    
    console.log('[Viz] Plotly.js available:', typeof Plotly);
    
    const generateBtn = document.getElementById('generate-viz');
    generateBtn.disabled = true;
    generateBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating...';
    
    try {
        console.log('[Viz] Generating visualizations for', currentPapers.length, 'papers');
        console.log('[Viz] Sample paper:', currentPapers[0]);
        
        const result = await pywebview.api.generate_visualizations(currentPapers);
        
        console.log('[Viz] API Response:', result);
        
        if (result.success) {
            console.log('[Viz] Visualizations received:');
            Object.keys(result.visualizations).forEach(key => {
                const htmlLength = result.visualizations[key] ? result.visualizations[key].length : 0;
                console.log(`  - ${key}: ${htmlLength} chars`);
            });
            
            displayVisualizations(result.visualizations);
            showStatus('viz-status', 'Visualizations generated successfully', 'success');
            console.log('[Viz] ✓ Visualizations generated');
        } else {
            showStatus('viz-status', `Error: ${result.error}`, 'error');
            console.error('[Viz] ✗ Error:', result.error);
        }
    } catch (error) {
        console.error('[Viz] ✗ Exception:', error);
        showStatus('viz-status', `Error: ${error.message}`, 'error');
    } finally {
        generateBtn.disabled = false;
        generateBtn.innerHTML = '<i class="fas fa-chart-pie"></i> Generate All Visualizations';
    }
}

function displayVisualizations(vizData) {
    console.log('[Viz] Displaying visualizations:', vizData);
    console.log('[Viz] Available keys:', Object.keys(vizData));
    
    // Helper function to properly render Plotly charts
    function updateVizElement(elementId, content, fallbackMessage) {
        const element = document.getElementById(elementId);
        if (!element) {
            console.error(`[Viz] Container not found: ${elementId}`);
            return false;
        }
        
        // Clear existing content
        element.innerHTML = '';
        
        if (content && content.length > 100) {
            console.log(`[Viz] Rendering ${elementId}: ${content.length} chars`);
            
            // Create temp div to parse HTML
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = content;
            
            // Extract and execute scripts separately
            const scripts = tempDiv.querySelectorAll('script');
            const scriptContents = [];
            
            scripts.forEach(script => {
                const scriptText = script.textContent || script.innerText;
                if (scriptText.trim()) {
                    scriptContents.push(scriptText);
                }
                script.remove(); // Remove from temp div
            });
            
            // Insert HTML (without scripts)
            element.innerHTML = tempDiv.innerHTML;
            
            // Execute scripts after DOM update
            setTimeout(() => {
                scriptContents.forEach((scriptContent, index) => {
                    try {
                        console.log(`[Viz] Executing script ${index + 1} for ${elementId}`);
                        
                        // Check if Plotly is available
                        if (scriptContent.includes('Plotly.newPlot') && typeof Plotly === 'undefined') {
                            console.error('[Viz] Plotly.js not loaded!');
                            element.innerHTML = '<p style="text-align: center; padding: 40px; color: #e74c3c;">Plotly.js not loaded. Check internet connection.</p>';
                            return;
                        }
                        
                        // Execute script
                        const scriptElement = document.createElement('script');
                        scriptElement.type = 'text/javascript';
                        scriptElement.text = scriptContent;
                        document.head.appendChild(scriptElement);
                        
                        // Remove script after execution
                        setTimeout(() => {
                            if (scriptElement.parentNode) {
                                scriptElement.parentNode.removeChild(scriptElement);
                            }
                        }, 1000);
                        
                        console.log(`[Viz] SUCCESS: Script ${index + 1} executed for ${elementId}`);
                        
                    } catch (error) {
                        console.error(`[Viz] ERROR executing script for ${elementId}:`, error);
                        element.innerHTML = `<p style="text-align: center; padding: 40px; color: #e74c3c;">Visualization error: ${error.message}</p>`;
                    }
                });
            }, 100); // Increased delay to ensure DOM is ready
            
            return true;
        } else {
            element.innerHTML = `<p style="text-align: center; padding: 40px; color: #999;">${fallbackMessage}</p>`;
            return false;
        }
    }
    
    const vizTypes = [
        { key: 'network', id: 'viz-network', fallback: 'Keyword network not available' },
        { key: 'years', id: 'viz-years', fallback: 'No year data available' },
        { key: 'citations', id: 'viz-citations', fallback: 'No citation data available' },
        { key: 'timeline', id: 'viz-timeline', fallback: 'No timeline data available' },
        { key: 'sources', id: 'viz-sources', fallback: 'No source data available' }
    ];
    
    let successCount = 0;
    
    vizTypes.forEach(viz => {
        const success = updateVizElement(viz.id, vizData[viz.key], viz.fallback);
        if (success) successCount++;
    });
    
    console.log(`[Viz] COMPLETE: ${successCount}/${vizTypes.length} visualizations rendered`);
}

// Export Handlers
function initExportHandlers() {
    const exportButtons = document.querySelectorAll('.export-btn');
    exportButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const format = btn.getAttribute('data-format');
            handleExport(format);
        });
    });
}

async function handleExport(format) {
    if (currentPapers.length === 0) {
        showStatus('export-status', 'No papers to export', 'error');
        return;
    }
    
    try {
        console.log('[Export] Exporting to', format);
        
        const result = await pywebview.api.export_data(format, currentPapers);
        
        if (result.success) {
            showStatus('export-status', `Successfully exported to: ${result.filepath}`, 'success');
            console.log('[Export] ✓ Exported to:', result.filepath);
        } else {
            showStatus('export-status', `Error: ${result.error}`, 'error');
            console.error('[Export] ✗ Error:', result.error);
        }
    } catch (error) {
        console.error('[Export] ✗ Exception:', error);
        showStatus('export-status', `Error: ${error.message}`, 'error');
    }
}

// Utility Functions
function showStatus(elementId, message, type) {
    const statusElement = document.getElementById(elementId);
    if (statusElement) {
        statusElement.textContent = message;
        statusElement.className = `status-message ${type}`;
        statusElement.style.display = 'block';
        
        // Auto-hide after 5 seconds for success messages
        if (type === 'success') {
            setTimeout(() => {
                statusElement.style.display = 'none';
            }, 5000);
        }
    }
}

function truncateText(text, maxLength) {
    if (text.length <= maxLength) {
        return text;
    }
    return text.substring(0, maxLength) + '...';
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Modal Functions
function showHelp() {
    openModal('help-modal');
}

function showAbout() {
    openModal('about-modal');
}

function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('show');
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('show');
    }
}

// Close modal when clicking outside
window.addEventListener('click', (event) => {
    if (event.target.classList.contains('modal')) {
        event.target.classList.remove('show');
    }
});

// Dark Mode
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    const isDark = document.body.classList.contains('dark-mode');
    
    // Update icon
    const icon = document.getElementById('darkmode-icon');
    if (icon) {
        icon.className = isDark ? 'fas fa-sun' : 'fas fa-moon';
    }
    
    // Save preference
    localStorage.setItem('darkMode', isDark ? 'enabled' : 'disabled');
    
    console.log('[DarkMode]', isDark ? 'Enabled' : 'Disabled');
}

// Load dark mode preference
function loadDarkMode() {
    const darkMode = localStorage.getItem('darkMode');
    if (darkMode === 'enabled') {
        document.body.classList.add('dark-mode');
        const icon = document.getElementById('darkmode-icon');
        if (icon) {
            icon.className = 'fas fa-sun';
        }
    }
}

// Scroll to Top
function scrollToTop() {
    const mainContent = document.querySelector('.main-content');
    if (mainContent) {
        mainContent.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    }
}

// Show/hide scroll to top button
function updateScrollButton() {
    const scrollBtn = document.getElementById('scroll-to-top');
    const mainContent = document.querySelector('.main-content');
    
    if (scrollBtn && mainContent) {
        if (mainContent.scrollTop > 300) {
            scrollBtn.classList.add('show');
        } else {
            scrollBtn.classList.remove('show');
        }
    }
}

// Keyboard Shortcuts
document.addEventListener('keydown', (e) => {
    // F1 - Help
    if (e.key === 'F1') {
        e.preventDefault();
        showHelp();
    }
    
    // Ctrl+D - Dark Mode
    if (e.ctrlKey && e.key === 'd') {
        e.preventDefault();
        toggleDarkMode();
    }
    
    // Escape - Close modals
    if (e.key === 'Escape') {
        document.querySelectorAll('.modal.show').forEach(modal => {
            modal.classList.remove('show');
        });
    }
});

// Initialize
console.log('[App] PaperLens Mini loaded');
