document.addEventListener('DOMContentLoaded', () => {
    // --- CONFIGURATION ---
    // Make sure this URL points to your deployed FastAPI backend
    const API_BASE_URL = 'http://127.0.0.1:8000'; 

    // --- DOM ELEMENT REFERENCES ---
    const leadForm = document.getElementById('lead-form');
    const leadsTableBody = document.getElementById('leads-table-body');
    const noLeadsMessage = document.getElementById('no-leads-message');
    const submitBtn = document.getElementById('submit-btn');
    const btnText = submitBtn.querySelector('.btn-text');
    const spinner = submitBtn.querySelector('.spinner');
    const refreshLeadsBtn = document.getElementById('refresh-leads-btn');

    // --- FUNCTIONS ---

    /**
     * Toggles the loading state of the submit button.
     * @param {boolean} isLoading - True to show spinner, false to show text.
     */
    const toggleLoading = (isLoading) => {
        if (isLoading) {
            submitBtn.disabled = true;
            btnText.style.display = 'none';
            spinner.style.display = 'inline-block';
        } else {
            submitBtn.disabled = false;
            btnText.style.display = 'inline-block';
            spinner.style.display = 'none';
        }
    };

    /**
     * Creates a score badge with color based on the score value.
     * @param {number} score - The score value (0-100).
     * @returns {string} - HTML string for the badge.
     */
    const createScoreBadge = (score) => {
        let colorClass = '';
        if (score >= 75) colorClass = 'high-intent';
        else if (score >= 40) colorClass = 'medium-intent';
        else colorClass = 'low-intent';
        
        // Inline styles for simplicity, could be moved to CSS
        const styles = {
            'high-intent': 'background-color: #10b981;',
            'medium-intent': 'background-color: #f59e0b;',
            'low-intent': 'background-color: #ef4444;'
        };

        return `<span class="score-badge" style="${styles[colorClass]}">${score}</span>`;
    };

    /**
     * Renders a list of leads into the table.
     * @param {Array<Object>} leads - An array of lead objects.
     */
    const renderLeads = (leads) => {
        leadsTableBody.innerHTML = ''; // Clear existing rows

        if (leads.length === 0) {
            noLeadsMessage.style.display = 'block';
        } else {
            noLeadsMessage.style.display = 'none';
            leads.forEach(lead => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${lead.Email}</td>
                    <td>${createScoreBadge(lead.InitialScore)}</td>
                    <td>${createScoreBadge(lead.RerankedScore)}</td>
                    <td>${lead.Comments || 'N/A'}</td>
                `;
                leadsTableBody.appendChild(row);
            });
        }
    };

    /**
     * Fetches all scored leads from the backend and renders them.
     */
    const fetchAndRenderLeads = async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/v1/leads`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const leads = await response.json();
            // Sort leads by Reranked Score in descending order
            leads.sort((a, b) => b.RerankedScore - a.RerankedScore);
            renderLeads(leads);
        } catch (error) {
            console.error('Failed to fetch leads:', error);
            alert('Could not fetch leads from the server.');
        }
    };


    // --- EVENT LISTENERS ---

    /**
     * Handles the form submission event.
     */
    leadForm.addEventListener('submit', async (event) => {
        event.preventDefault(); // Prevent default browser submission
        
        toggleLoading(true);

        const formData = new FormData(leadForm);
        const leadData = Object.fromEntries(formData.entries());

        // Convert string numbers to actual numbers
        leadData.CreditScore = parseInt(leadData.CreditScore, 10);
        leadData.Income = parseInt(leadData.Income, 10);
        leadData.TimeOnPage = parseInt(leadData.TimeOnPage, 10);
        leadData.PagesVisited = parseInt(leadData.PagesVisited, 10);

        try {
            const response = await fetch(`${API_BASE_URL}/api/v1/score`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(leadData),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'An unknown error occurred.');
            }

            // After successful submission, refresh the leads list
            await fetchAndRenderLeads();
            leadForm.reset(); // Clear the form for the next entry

        } catch (error) {
            console.error('Error submitting lead:', error);
            alert(`Failed to score lead: ${error.message}`);
        } finally {
            toggleLoading(false);
        }
    });

    /**
     * Handles the click event for the refresh button.
     */
    refreshLeadsBtn.addEventListener('click', fetchAndRenderLeads);

    // --- INITIALIZATION ---
    // Fetch and display any existing leads when the page loads
    fetchAndRenderLeads();
});