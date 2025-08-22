// Main JavaScript functionality for Career Insights Platform

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initializeDragAndDrop();
    initializeFormValidation();
    initializeTooltips();
    initializeProgressBars();
    initializeAnimations();
});

// Drag and Drop functionality
function initializeDragAndDrop() {
    const dropAreas = document.querySelectorAll('[id$="drop-area"]');
    
    dropAreas.forEach(dropArea => {
        const fileInput = dropArea.querySelector('input[type="file"]');
        
        if (!fileInput) return;
        
        // Prevent default drag behaviors
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropArea.addEventListener(eventName, preventDefaults, false);
            document.body.addEventListener(eventName, preventDefaults, false);
        });

        // Highlight drop area when item is dragged over it
        ['dragenter', 'dragover'].forEach(eventName => {
            dropArea.addEventListener(eventName, () => highlight(dropArea), false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropArea.addEventListener(eventName, () => unhighlight(dropArea), false);
        });

        // Handle dropped files
        dropArea.addEventListener('drop', (e) => handleDrop(e, fileInput), false);
        
        // Handle file input change
        fileInput.addEventListener('change', function() {
            if (this.files.length > 0) {
                showFileName(this.files[0].name, dropArea);
                validateFile(this.files[0], this);
            }
        });
    });
}

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

function highlight(dropArea) {
    dropArea.classList.add('drop-area-active');
    if (dropArea.id === 'drop-area') {
        dropArea.classList.add('border-primary-500', 'bg-primary-50');
    } else {
        dropArea.classList.add('border-green-500', 'bg-green-50');
    }
}

function unhighlight(dropArea) {
    dropArea.classList.remove('drop-area-active');
    dropArea.classList.remove('border-primary-500', 'bg-primary-50', 'border-green-500', 'bg-green-50');
}

function handleDrop(e, fileInput) {
    const dt = e.dataTransfer;
    const files = dt.files;

    if (files.length > 0) {
        fileInput.files = files;
        const dropArea = fileInput.closest('[id$="drop-area"]');
        showFileName(files[0].name, dropArea);
        validateFile(files[0], fileInput);
    }
}

function showFileName(name, dropArea) {
    let fileNameDisplay = dropArea.querySelector('#file-name');
    if (!fileNameDisplay) {
        fileNameDisplay = dropArea.querySelector('[id$="file-name"]');
    }
    
    if (fileNameDisplay) {
        fileNameDisplay.textContent = `Selected: ${name}`;
        fileNameDisplay.classList.remove('hidden');
        fileNameDisplay.classList.add('animate-fadeIn');
    }
}

function validateFile(file, input) {
    const maxSize = 16 * 1024 * 1024; // 16MB
    const allowedTypes = input.accept ? input.accept.split(',').map(t => t.trim()) : [];
    
    // Check file size
    if (file.size > maxSize) {
        showError('File size exceeds 16MB limit. Please choose a smaller file.');
        input.value = '';
        return false;
    }
    
    // Check file type
    if (allowedTypes.length > 0) {
        const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
        if (!allowedTypes.includes(fileExtension)) {
            showError(`Invalid file type. Allowed types: ${allowedTypes.join(', ')}`);
            input.value = '';
            return false;
        }
    }
    
    return true;
}

// Form validation
function initializeFormValidation() {
    const forms = document.querySelectorAll('form[enctype="multipart/form-data"]');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const fileInput = form.querySelector('input[type="file"]');
            
            if (fileInput && !fileInput.files.length) {
                e.preventDefault();
                showError('Please select a file before submitting.');
                return false;
            }
            
            // Show loading state
            showLoadingState(form);
        });
    });
}

function showLoadingState(form) {
    const submitBtn = form.querySelector('button[type="submit"]');
    if (submitBtn) {
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Processing...';
        submitBtn.disabled = true;
        
        // Store original text for potential restoration
        submitBtn.dataset.originalText = originalText;
    }
    
    // Show loading overlay
    showLoadingOverlay();
}

function showLoadingOverlay() {
    const overlay = document.createElement('div');
    overlay.className = 'loading-overlay';
    overlay.innerHTML = `
        <div class="text-center">
            <div class="loading-spinner"></div>
            <p class="mt-4 text-gray-600">Processing your request...</p>
        </div>
    `;
    document.body.appendChild(overlay);
}

// Error handling
function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'alert alert-error fixed top-4 right-4 z-50 max-w-md';
    errorDiv.innerHTML = `
        <div class="flex items-center">
            <i class="fas fa-exclamation-triangle mr-2"></i>
            <span>${message}</span>
            <button onclick="this.parentElement.parentElement.remove()" class="ml-4 text-red-800 hover:text-red-900">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;
    
    document.body.appendChild(errorDiv);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (errorDiv.parentElement) {
            errorDiv.remove();
        }
    }, 5000);
}

function showSuccess(message) {
    const successDiv = document.createElement('div');
    successDiv.className = 'alert alert-success fixed top-4 right-4 z-50 max-w-md';
    successDiv.innerHTML = `
        <div class="flex items-center">
            <i class="fas fa-check-circle mr-2"></i>
            <span>${message}</span>
            <button onclick="this.parentElement.parentElement.remove()" class="ml-4 text-green-800 hover:text-green-900">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;
    
    document.body.appendChild(successDiv);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        if (successDiv.parentElement) {
            successDiv.remove();
        }
    }, 3000);
}

// Tooltips initialization
function initializeTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    
    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', showTooltip);
        element.addEventListener('mouseleave', hideTooltip);
    });
}

function showTooltip(e) {
    const text = e.target.dataset.tooltip;
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip absolute bg-gray-800 text-white text-xs rounded px-2 py-1 z-50';
    tooltip.textContent = text;
    
    document.body.appendChild(tooltip);
    
    const rect = e.target.getBoundingClientRect();
    tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
    tooltip.style.top = rect.top - tooltip.offsetHeight - 5 + 'px';
    
    e.target.tooltipElement = tooltip;
}

function hideTooltip(e) {
    if (e.target.tooltipElement) {
        e.target.tooltipElement.remove();
        e.target.tooltipElement = null;
    }
}

// Progress bars
function initializeProgressBars() {
    const progressBars = document.querySelectorAll('.progress-bar');
    
    progressBars.forEach(bar => {
        const targetWidth = bar.dataset.progress || '0';
        bar.style.width = '0%';
        
        setTimeout(() => {
            bar.style.width = targetWidth + '%';
        }, 500);
    });
}

// Animations
function initializeAnimations() {
    // Fade in animation for cards
    const cards = document.querySelectorAll('.card-hover');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fadeIn');
            }
        });
    });
    
    cards.forEach(card => {
        observer.observe(card);
    });
    
    // Stagger animation for skill tags
    const skillTags = document.querySelectorAll('.skill-tag');
    skillTags.forEach((tag, index) => {
        tag.style.animationDelay = (index * 0.1) + 's';
    });
}

// Utility functions
function copyToClipboard(text) {
    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(() => {
            showSuccess('Copied to clipboard!');
        }).catch(() => {
            fallbackCopyToClipboard(text);
        });
    } else {
        fallbackCopyToClipboard(text);
    }
}

function fallbackCopyToClipboard(text) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    textArea.style.top = '-999999px';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
        document.execCommand('copy');
        showSuccess('Copied to clipboard!');
    } catch (err) {
        showError('Failed to copy to clipboard');
    }
    
    textArea.remove();
}

// Chart utilities
function createChart(canvasId, type, data, options = {}) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return null;
    
    const defaultOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false
            }
        }
    };
    
    const mergedOptions = { ...defaultOptions, ...options };
    
    return new Chart(ctx.getContext('2d'), {
        type: type,
        data: data,
        options: mergedOptions
    });
}

function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
}

function formatPercentage(num) {
    return Math.round(num) + '%';
}

// Export functions for global access
window.CareerInsights = {
    copyToClipboard,
    showSuccess,
    showError,
    createChart,
    formatNumber,
    formatPercentage
};

// Add custom CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .animate-fadeIn {
        animation: fadeIn 0.6s ease-out forwards;
    }
    
    @keyframes slideInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .animate-slideInUp {
        animation: slideInUp 0.8s ease-out forwards;
    }
    
    @keyframes bounce {
        0%, 20%, 53%, 80%, 100% { transform: translate3d(0,0,0); }
        40%, 43% { transform: translate3d(0,-30px,0); }
        70% { transform: translate3d(0,-15px,0); }
        90% { transform: translate3d(0,-4px,0); }
    }
    
    .animate-bounce {
        animation: bounce 1s ease infinite;
    }
`;
document.head.appendChild(style);
