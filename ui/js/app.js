/**
 * PaperLens Mini - Frontend JavaScript
 * Simplified version without AI/ML features
 */

// Global state
let currentPapers = [];
let currentStep = 1;
let searchHistory = [];

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
    initSearchHistory();
    initExportHandlers();
    loadAppInfo();
    
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
        console.log('[Init] [OK] PaperLens Mini ready');
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
    
    // Update statistics when entering export page
    if (step === 3) {
        updateStatistics();
    }
    
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
    const searchType = document.getElementById('search-type').value;
    const maxResults = parseInt(document.getElementById('max-results').value);
    const fromYear = document.getElementById('from-year').value;
    
    // Clear previous status
    showStatus('search-status', '', '');
    
    // Validate form inputs
    if (!query) {
        showStatus('search-status', 'Please enter search keywords', 'error');
        document.getElementById('search-query').focus();
        return;
    }
    
    if (isNaN(maxResults) || maxResults < 10 || maxResults > 1000) {
        showStatus('search-status', 'Max Results must be between 10 and 1000', 'error');
        document.getElementById('max-results').focus();
        return;
    }
    
    if (fromYear && (isNaN(fromYear) || fromYear < 1900 || fromYear > 2030)) {
        showStatus('search-status', 'From Year must be between 1900 and 2030', 'error');
        document.getElementById('from-year').focus();
        return;
    }
    
    const searchBtn = document.getElementById('search-btn');
    searchBtn.disabled = true;
    searchBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Searching...';
    
    try {
        console.log('[Search] Starting search:', { query, source, searchType, maxResults, fromYear });
        
        const params = {
            query: query,
            source: source,
            search_type: searchType,
            max_results: maxResults,
            from_year: fromYear ? parseInt(fromYear) : null
        };
        
        const result = await pywebview.api.search_papers(params);
        
        if (result.success) {
            currentPapers = result.papers;
            displayPapers(result.papers);
            showStatus('search-status', `Found ${result.count} papers`, 'success');
            
            // Save to search history
            addToSearchHistory(query, source, searchType);
            
            // Enable next steps
            updateWizardSteps();
            updateFixedNavigation();
            
            console.log('[Search] [OK] Found', result.count, 'papers');
        } else {
            showStatus('search-status', `Error: ${result.error}`, 'error');
            console.error('[Search] [ERROR] Error:', result.error);
        }
    } catch (error) {
        console.error('[Search] [ERROR] Exception:', error);
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
            console.log('[Viz] [OK] Visualizations generated');
        } else {
            showStatus('viz-status', `Error: ${result.error}`, 'error');
            console.error('[Viz] [ERROR] Error:', result.error);
        }
    } catch (error) {
        console.error('[Viz] [ERROR] Exception:', error);
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
        { key: 'wordcloud', id: 'viz-wordcloud', fallback: 'Word cloud not available' },
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
            console.log('[Export] [OK] Exported to:', result.filepath);
            
            // Show confirmation dialog
            showExportConfirmation(result.filepath);
        } else {
            showStatus('export-status', `Error: ${result.error}`, 'error');
            console.error('[Export] [ERROR] Error:', result.error);
        }
    } catch (error) {
        console.error('[Export] [ERROR] Exception:', error);
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
        
        // Close search history dropdown
        const historyDropdown = document.getElementById('search-history');
        if (historyDropdown && historyDropdown.style.display !== 'none') {
            historyDropdown.style.display = 'none';
        }
    }
});

// Search History Functions
function initSearchHistory() {
    console.log('[SearchHistory] Initializing search history...');
    
    // Load search history from localStorage
    loadSearchHistory();
    
    // Add event listeners
    const searchInput = document.getElementById('search-query');
    const historyDropdown = document.getElementById('search-history');
    const clearAllBtn = document.getElementById('clear-all-history');
    
    if (searchInput) {
        searchInput.addEventListener('focus', showSearchHistory);
        searchInput.addEventListener('blur', (e) => {
            // Delay hiding to allow clicking on history items
            setTimeout(() => {
                if (!historyDropdown.contains(document.activeElement)) {
                    hideSearchHistory();
                }
            }, 200);
        });
        searchInput.addEventListener('input', filterSearchHistory);
    }
    
    if (clearAllBtn) {
        clearAllBtn.addEventListener('click', clearAllSearchHistory);
    }
    
    // Click outside to close
    document.addEventListener('click', (e) => {
        if (!searchInput.contains(e.target) && !historyDropdown.contains(e.target)) {
            hideSearchHistory();
        }
    });
}

function loadSearchHistory() {
    try {
        const saved = localStorage.getItem('paperlens_search_history');
        if (saved) {
            searchHistory = JSON.parse(saved);
            console.log(`[SearchHistory] Loaded ${searchHistory.length} history items`);
        }
    } catch (error) {
        console.error('[SearchHistory] Error loading history:', error);
        searchHistory = [];
    }
}

function saveSearchHistory() {
    try {
        localStorage.setItem('paperlens_search_history', JSON.stringify(searchHistory));
        console.log(`[SearchHistory] Saved ${searchHistory.length} history items`);
    } catch (error) {
        console.error('[SearchHistory] Error saving history:', error);
    }
}

function addToSearchHistory(query, source, searchType) {
    if (!query || query.trim().length === 0) return;
    
    const historyItem = {
        id: Date.now(),
        query: query.trim(),
        source: source || 'all',
        searchType: searchType || 'all',
        timestamp: new Date().toISOString(),
        displayTime: new Date().toLocaleString()
    };
    
    // Remove existing item with same query
    searchHistory = searchHistory.filter(item => item.query !== historyItem.query);
    
    // Add to beginning
    searchHistory.unshift(historyItem);
    
    // Limit to 20 items
    if (searchHistory.length > 20) {
        searchHistory = searchHistory.slice(0, 20);
    }
    
    saveSearchHistory();
    console.log(`[SearchHistory] Added: ${query}`);
}

function showSearchHistory() {
    const historyDropdown = document.getElementById('search-history');
    if (historyDropdown && searchHistory.length > 0) {
        renderSearchHistory();
        historyDropdown.style.display = 'block';
    }
}

function hideSearchHistory() {
    const historyDropdown = document.getElementById('search-history');
    if (historyDropdown) {
        historyDropdown.style.display = 'none';
    }
}

function filterSearchHistory() {
    const searchInput = document.getElementById('search-query');
    const query = searchInput.value.toLowerCase();
    
    if (query.length === 0) {
        renderSearchHistory();
        return;
    }
    
    const filtered = searchHistory.filter(item => 
        item.query.toLowerCase().includes(query)
    );
    
    renderSearchHistory(filtered);
}

function renderSearchHistory(items = null) {
    const historyList = document.getElementById('search-history-list');
    const historyDropdown = document.getElementById('search-history');
    
    if (!historyList || !historyDropdown) return;
    
    const itemsToRender = items || searchHistory;
    
    if (itemsToRender.length === 0) {
        historyList.innerHTML = '<div class="search-history-empty">No search history found</div>';
        historyDropdown.style.display = 'none';
        return;
    }
    
    historyList.innerHTML = itemsToRender.map(item => `
        <div class="search-history-item" data-query="${item.query}" data-source="${item.source}" data-type="${item.searchType}">
            <div class="search-history-text">${item.query}</div>
            <div class="search-history-meta">${item.displayTime}</div>
            <button class="search-history-delete" onclick="deleteSearchHistoryItem(${item.id}, event)" title="Delete this search">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `).join('');
    
    // Add click handlers for history items
    historyList.querySelectorAll('.search-history-item').forEach(item => {
        item.addEventListener('click', (e) => {
            if (!e.target.closest('.search-history-delete')) {
                const query = item.dataset.query;
                const source = item.dataset.source;
                const type = item.dataset.type;
                
                // Fill the search form
                document.getElementById('search-query').value = query;
                document.getElementById('source-select').value = source;
                document.getElementById('search-type').value = type;
                
                hideSearchHistory();
                
                // Trigger search
                handleSearch();
            }
        });
    });
}

function deleteSearchHistoryItem(id, event) {
    event.stopPropagation();
    
    searchHistory = searchHistory.filter(item => item.id !== id);
    saveSearchHistory();
    renderSearchHistory();
    
    console.log(`[SearchHistory] Deleted item with id: ${id}`);
}

function clearAllSearchHistory() {
    if (confirm('Are you sure you want to clear all search history?')) {
        searchHistory = [];
        saveSearchHistory();
        hideSearchHistory();
        console.log('[SearchHistory] Cleared all history');
    }
}

// Statistics Functions
async function updateStatistics() {
    if (!currentPapers || currentPapers.length === 0) {
        console.log('[Statistics] No papers to analyze');
        return;
    }
    
    try {
        console.log('[Statistics] Updating statistics for', currentPapers.length, 'papers');
        
        const result = await pywebview.api.get_paper_statistics(currentPapers);
        
        if (result.success) {
            displayStatistics(result.statistics);
            console.log('[Statistics] [OK] Statistics updated');
        } else {
            console.error('[Statistics] [ERROR] Error:', result.error);
        }
    } catch (error) {
        console.error('[Statistics] [ERROR] Exception:', error);
    }
}

function displayStatistics(stats) {
    // Update basic statistics
    document.getElementById('total-papers').textContent = stats.total_papers || 0;
    document.getElementById('total-authors').textContent = stats.total_authors || 0;
    document.getElementById('year-range').textContent = stats.year_range || '-';
    document.getElementById('data-sources').textContent = stats.data_sources || 0;
    
    // Update top authors
    const topAuthorsList = document.getElementById('top-authors-list');
    if (stats.top_authors && stats.top_authors.length > 0) {
        topAuthorsList.innerHTML = stats.top_authors.map((author, index) => {
            const rankClass = index < 3 ? `rank-${index + 1}` : '';
            const papersList = author.papers && author.papers.length > 0 ? 
                author.papers.slice(0, 3).map(paper => `<div class="paper-title">${escapeHtml(paper)}</div>`).join('') +
                (author.papers.length > 3 ? `<div class="paper-title more">... and ${author.papers.length - 3} more</div>` : '') :
                '<div class="paper-title no-papers">No paper titles available</div>';
            
            return `
                <div class="author-item ${rankClass}">
                    <div class="author-header">
                        <div class="author-info">
                            <div class="author-name">${author.name}</div>
                            <div class="author-affiliation">${author.affiliation || 'No affiliation'}</div>
                        </div>
                        <div class="author-stats">
                            <div class="author-paper-count">${author.paper_count}</div>
                            <div class="author-paper-label">paper${author.paper_count !== 1 ? 's' : ''}</div>
                        </div>
                    </div>
                    <div class="author-papers">
                        ${papersList}
                    </div>
                </div>
            `;
        }).join('');
    } else {
        topAuthorsList.innerHTML = '<div class="no-data">No author data available</div>';
    }
}

// Export Confirmation Functions
let currentExportedFile = null;

function showExportConfirmation(filepath) {
    currentExportedFile = filepath;
    
    // Extract filename from path for display
    const filename = filepath.split('/').pop() || filepath.split('\\').pop() || filepath;
    
    // Update modal content
    document.getElementById('exported-file-path').textContent = filename;
    
    // Show modal
    const modal = document.getElementById('export-confirmation-modal');
    modal.style.display = 'block';
    
    console.log('[Export] Showing confirmation dialog for:', filepath);
}

function closeExportConfirmation() {
    const modal = document.getElementById('export-confirmation-modal');
    modal.style.display = 'none';
    currentExportedFile = null;
    console.log('[Export] Confirmation dialog closed');
}

async function openExportedFile() {
    if (!currentExportedFile) {
        console.error('[Export] No file to open');
        return;
    }
    
    try {
        console.log('[Export] Opening file:', currentExportedFile);
        const result = await pywebview.api.open_file(currentExportedFile);
        
        if (result.success) {
            console.log('[Export] File opened successfully');
            showStatus('export-status', 'File opened successfully', 'success');
        } else {
            console.log('[Export] Failed to open file:', result.error);
            showStatus('export-status', `Failed to open file: ${result.error}`, 'error');
        }
    } catch (error) {
        console.error('[Export] Error opening file:', error);
        showStatus('export-status', `Error opening file: ${error.message}`, 'error');
    }
    
    closeExportConfirmation();
}

async function openFileManager() {
    if (!currentExportedFile) {
        console.error('[Export] No file to show in file manager');
        return;
    }
    
    try {
        console.log('[Export] Opening file manager for:', currentExportedFile);
        const result = await pywebview.api.open_file_manager(currentExportedFile);
        
        if (result.success) {
            console.log('[Export] File manager opened successfully');
            showStatus('export-status', 'File manager opened', 'success');
        } else {
            console.log('[Export] Failed to open file manager:', result.error);
            showStatus('export-status', `Failed to open file manager: ${result.error}`, 'error');
        }
    } catch (error) {
        console.error('[Export] Error opening file manager:', error);
        showStatus('export-status', `Error opening file manager: ${error.message}`, 'error');
    }
    
    closeExportConfirmation();
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('export-confirmation-modal');
    if (event.target === modal) {
        closeExportConfirmation();
    }
}

// App Info Functions
async function loadAppInfo() {
    try {
        console.log('[AppInfo] Loading application information...');
        const result = await pywebview.api.get_app_info();
        
        if (result.success) {
            const appInfo = result.app_info;
            console.log('[AppInfo] Loaded app info:', appInfo);
            
            // Update version in sidebar
            const sidebarVersion = document.getElementById('sidebar-version');
            if (sidebarVersion) {
                sidebarVersion.textContent = appInfo.version;
            }
            
            // Update version in about modal
            const aboutVersion = document.getElementById('app-version');
            if (aboutVersion) {
                aboutVersion.textContent = appInfo.version;
            }
            
            // Update page title
            document.title = `${appInfo.name} v${appInfo.version}`;
            
            console.log('[AppInfo] Version information updated successfully');
        } else {
            console.error('[AppInfo] Failed to load app info:', result.error);
        }
    } catch (error) {
        console.error('[AppInfo] Error loading app info:', error);
    }
}

// Initialize
console.log('[App] PaperLens Mini loaded');
