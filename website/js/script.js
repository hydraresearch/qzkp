// Hydra Research Website JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for navigation links
    const navLinks = document.querySelectorAll('a[href^="#"]');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                const offsetTop = targetSection.offsetTop - 80; // Account for fixed navbar
                
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Animate statistics on scroll
    const stats = document.querySelectorAll('.stat h3');
    const animateStats = () => {
        stats.forEach(stat => {
            const rect = stat.getBoundingClientRect();
            if (rect.top < window.innerHeight && rect.bottom > 0) {
                const finalValue = stat.textContent;
                const isPercentage = finalValue.includes('%');
                const numericValue = parseInt(finalValue.replace(/[^\d]/g, ''));
                
                if (!stat.classList.contains('animated')) {
                    stat.classList.add('animated');
                    animateNumber(stat, 0, numericValue, isPercentage ? '%' : '', 2000);
                }
            }
        });
    };

    // Number animation function
    function animateNumber(element, start, end, suffix, duration) {
        const startTime = performance.now();
        
        function updateNumber(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            // Easing function for smooth animation
            const easeOutQuart = 1 - Math.pow(1 - progress, 4);
            const current = Math.floor(start + (end - start) * easeOutQuart);
            
            element.textContent = current + suffix;
            
            if (progress < 1) {
                requestAnimationFrame(updateNumber);
            } else {
                element.textContent = end + suffix;
            }
        }
        
        requestAnimationFrame(updateNumber);
    }

    // Scroll event listener for animations
    window.addEventListener('scroll', animateStats);
    
    // Initial check for stats animation
    animateStats();

    // Quantum job verification functionality
    const jobCards = document.querySelectorAll('.job-card');
    
    jobCards.forEach(card => {
        card.addEventListener('click', function() {
            const jobId = this.querySelector('code').textContent;
            const confirmVerify = confirm(`Open IBM Quantum Experience to verify job ${jobId}?`);
            
            if (confirmVerify) {
                window.open('https://quantum-computing.ibm.com/', '_blank');
            }
        });
        
        // Add hover effect
        card.style.cursor = 'pointer';
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-3px)';
            this.style.boxShadow = '0 5px 15px rgba(0,0,0,0.2)';
            this.style.transition = 'all 0.3s ease';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = 'none';
        });
    });

    // Research card interactions
    const researchCards = document.querySelectorAll('.research-card');
    
    researchCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.borderLeftColor = '#ff6b6b';
            this.style.transition = 'border-left-color 0.3s ease';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.borderLeftColor = '#667eea';
        });
    });

    // Navbar background change on scroll
    const navbar = document.querySelector('.navbar');
    
    window.addEventListener('scroll', function() {
        if (window.scrollY > 100) {
            navbar.style.background = 'rgba(30, 60, 114, 0.95)';
            navbar.style.backdropFilter = 'blur(10px)';
        } else {
            navbar.style.background = 'linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)';
            navbar.style.backdropFilter = 'none';
        }
    });

    // Copy job ID functionality
    const jobCodes = document.querySelectorAll('.job-card code');
    
    jobCodes.forEach(code => {
        code.addEventListener('click', function(e) {
            e.stopPropagation(); // Prevent card click
            
            // Copy to clipboard
            navigator.clipboard.writeText(this.textContent).then(() => {
                // Show feedback
                const originalText = this.textContent;
                this.textContent = 'Copied!';
                this.style.background = '#4ecdc4';
                
                setTimeout(() => {
                    this.textContent = originalText;
                    this.style.background = '#2c3e50';
                }, 1500);
            }).catch(() => {
                // Fallback for older browsers
                const textArea = document.createElement('textarea');
                textArea.value = this.textContent;
                document.body.appendChild(textArea);
                textArea.select();
                document.execCommand('copy');
                document.body.removeChild(textArea);
                
                const originalText = this.textContent;
                this.textContent = 'Copied!';
                this.style.background = '#4ecdc4';
                
                setTimeout(() => {
                    this.textContent = originalText;
                    this.style.background = '#2c3e50';
                }, 1500);
            });
        });
        
        // Add tooltip
        code.title = 'Click to copy job ID';
        code.style.cursor = 'pointer';
    });

    // Quantum circuit visualization (simple animation)
    const quantumPreview = document.querySelector('.quantum-circuit-preview');
    
    if (quantumPreview) {
        // Add pulsing effect to simulate quantum activity
        setInterval(() => {
            quantumPreview.style.boxShadow = '0 0 20px rgba(100, 181, 246, 0.5)';
            
            setTimeout(() => {
                quantumPreview.style.boxShadow = 'none';
            }, 1000);
        }, 3000);
    }

    // Success rate animation
    const successRates = document.querySelectorAll('.success-rate');
    
    const animateSuccessRates = () => {
        successRates.forEach(rate => {
            const rect = rate.getBoundingClientRect();
            if (rect.top < window.innerHeight && rect.bottom > 0) {
                if (!rate.classList.contains('animated')) {
                    rate.classList.add('animated');
                    rate.style.animation = 'pulse 0.6s ease-in-out';
                }
            }
        });
    };

    window.addEventListener('scroll', animateSuccessRates);
    animateSuccessRates();

    // Add CSS animation for pulse effect
    const style = document.createElement('style');
    style.textContent = `
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        
        .job-card:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3) !important;
        }
        
        .research-card:hover {
            border-left-color: #ff6b6b !important;
        }
        
        .doc-card:hover {
            border-color: #667eea !important;
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.2);
        }
    `;
    document.head.appendChild(style);

    // Email contact functionality
    const emailLinks = document.querySelectorAll('a[href^="mailto:"]');
    
    emailLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const email = this.getAttribute('href').replace('mailto:', '');
            
            // Show confirmation
            const confirmEmail = confirm(`Open email client to contact ${email}?`);
            
            if (!confirmEmail) {
                e.preventDefault();
            }
        });
    });

    // GitHub repository link tracking
    const githubLinks = document.querySelectorAll('a[href*="github.com"]');
    
    githubLinks.forEach(link => {
        link.addEventListener('click', function() {
            // Add visual feedback
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 150);
        });
    });

    // Intersection Observer for fade-in animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe sections for fade-in effect
    const sections = document.querySelectorAll('section');
    sections.forEach(section => {
        section.style.opacity = '0';
        section.style.transform = 'translateY(20px)';
        section.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(section);
    });

    // Console message for developers
    console.log(`
    🔬 Hydra Research - Quantum Zero-Knowledge Proofs
    ================================================
    
    Welcome to the future of quantum cryptography!
    
    🎯 Key Achievements:
    • 38/38 tests passed (100% success rate)
    • 14 verifiable quantum jobs on IBM Brisbane
    • First practical quantum ZKP implementation
    • Novel probabilistic entanglement encoding
    
    🔗 Verify our results:
    https://quantum-computing.ibm.com/
    
    📧 Contact: ncloutier@hydraresearch.io
    📚 Repository: https://github.com/hydraresearch/qzkp
    
    All quantum jobs are independently verifiable!
    `);
});

// Performance monitoring
window.addEventListener('load', function() {
    const loadTime = performance.now();
    console.log(`🚀 Website loaded in ${loadTime.toFixed(2)}ms`);
    
    // Track page performance
    if ('performance' in window && 'navigation' in performance) {
        const perfData = performance.getEntriesByType('navigation')[0];
        console.log(`📊 Performance metrics:
        • DOM Content Loaded: ${perfData.domContentLoadedEventEnd - perfData.domContentLoadedEventStart}ms
        • Load Complete: ${perfData.loadEventEnd - perfData.loadEventStart}ms
        • Total Page Load: ${perfData.loadEventEnd - perfData.navigationStart}ms`);
    }
});
