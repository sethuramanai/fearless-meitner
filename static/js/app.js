document.addEventListener('DOMContentLoaded', () => {
    // -------------------------------------------------------------
    // Theme Switcher
    // -------------------------------------------------------------
    const themeToggleBtn = document.getElementById('theme-toggle');
    const themeIcon = themeToggleBtn ? themeToggleBtn.querySelector('.theme-icon') : null;
    
    // Check local storage or system preferences
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    let currentTheme = savedTheme || (prefersDark ? 'dark' : 'light');
    document.documentElement.setAttribute('data-theme', currentTheme);
    updateThemeIcon(currentTheme);

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            currentTheme = currentTheme === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', currentTheme);
            localStorage.setItem('theme', currentTheme);
            updateThemeIcon(currentTheme);
        });
    }

    function updateThemeIcon(theme) {
        if (!themeIcon) return;
        if (theme === 'dark') {
            themeIcon.textContent = '☀️'; // Show sun to switch to light
            themeToggleBtn.setAttribute('title', 'Switch to Light Mode');
        } else {
            themeIcon.textContent = '🌙'; // Show moon to switch to dark
            themeToggleBtn.setAttribute('title', 'Switch to Dark Mode');
        }
    }

    // -------------------------------------------------------------
    // Circular Progress Ring Update
    // -------------------------------------------------------------
    const circle = document.querySelector('.progress-ring-circle');
    if (circle) {
        const radius = circle.r.baseVal.value;
        const circumference = radius * 2 * Math.PI;
        
        circle.style.strokeDasharray = `${circumference} ${circumference}`;
        
        window.setProgress = function(percent) {
            const offset = circumference - (percent / 100 * circumference);
            circle.style.strokeDashoffset = offset;
        }

        // Initialize progress
        const initialRate = parseInt(document.getElementById('completion-rate-text')?.textContent || '0');
        setProgress(initialRate);
    }

    // -------------------------------------------------------------
    // AJAX Task Status Toggling
    // -------------------------------------------------------------
    const taskList = document.querySelector('.tasks-list');
    
    if (taskList) {
        taskList.addEventListener('change', async (e) => {
            if (e.target.classList.contains('task-toggle-checkbox')) {
                const checkbox = e.target;
                const taskId = checkbox.dataset.taskId;
                const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
                const taskCard = document.getElementById(`task-card-${taskId}`);

                checkbox.disabled = true;

                try {
                    const response = await fetch(`/toggle/${taskId}/`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': csrfToken,
                            'X-Requested-With': 'XMLHttpRequest'
                        }
                    });

                    if (response.ok) {
                        const data = await response.json();
                        if (data.success) {
                            // Toggle card visual representation
                            if (data.completed) {
                                taskCard.classList.add('completed');
                            } else {
                                taskCard.classList.remove('completed');
                            }

                            // Update stats counters
                            const completedCountEl = document.getElementById('completed-count');
                            const activeCountEl = document.getElementById('active-count');
                            const rateTextEl = document.getElementById('completion-rate-text');

                            if (completedCountEl) completedCountEl.textContent = data.completed_count;
                            if (activeCountEl) activeCountEl.textContent = data.active_count;
                            if (rateTextEl) rateTextEl.textContent = `${data.completion_rate}%`;

                            // Update progress ring
                            if (window.setProgress) {
                                setProgress(data.completion_rate);
                            }

                            // Create a temporary beautiful micro-toast to confirm action
                            showMiniToast(data.completed ? 'Task completed! 🎉' : 'Task marked active.');
                        }
                    } else {
                        console.error('Failed to toggle task status.');
                        checkbox.checked = !checkbox.checked; // Revert checkbox
                    }
                } catch (err) {
                    console.error('Error toggling task:', err);
                    checkbox.checked = !checkbox.checked; // Revert checkbox
                } finally {
                    checkbox.disabled = false;
                }
            }
        });
    }

    // -------------------------------------------------------------
    // Toast Auto-Dismissal
    // -------------------------------------------------------------
    const toasts = document.querySelectorAll('.toast-message');
    toasts.forEach(toast => {
        // Dismiss after 4 seconds
        setTimeout(() => {
            dismissToast(toast);
        }, 4000);
        
        // Manual close
        const closeBtn = toast.querySelector('.toast-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                dismissToast(toast);
            });
        }
    });

    function dismissToast(toast) {
        if (!toast || toast.classList.contains('slide-out')) return;
        toast.classList.add('slide-out');
        toast.addEventListener('animationend', () => {
            toast.remove();
        });
    }

    // Dynamic mini toast notification function
    function showMiniToast(message) {
        let container = document.querySelector('.messages-container');
        if (!container) {
            container = document.createElement('div');
            container.className = 'messages-container';
            document.body.appendChild(container);
        }

        const toast = document.createElement('div');
        toast.className = 'toast-message toast-success';
        toast.innerHTML = `
            <span>${message}</span>
            <button class="toast-close">&times;</button>
        `;

        container.appendChild(toast);

        toast.querySelector('.toast-close').addEventListener('click', () => {
            dismissToast(toast);
        });

        setTimeout(() => {
            dismissToast(toast);
        }, 3000);
    }
});
