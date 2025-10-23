/**
 * TradingMaven Counter Animation
 * Animates numbers counting up from 0 to target value
 */

class CounterAnimation {
  constructor(element, targetValue, duration = 2500, suffix = '') {
    this.element = element;
    this.targetValue = parseFloat(targetValue);
    this.duration = duration;
    this.suffix = suffix;
    this.startValue = 0;
    this.startTime = null;
    this.hasAnimated = false;
  }

  /**
   * Easing function for smooth animation
   */
  easeOutQuad(t) {
    return t * (2 - t);
  }

  /**
   * Start the counter animation
   */
  start() {
    if (this.hasAnimated) return;
    this.hasAnimated = true;
    this.startTime = null;
    this.animate();
  }

  /**
   * Animation loop using requestAnimationFrame
   */
  animate(currentTime) {
    if (!this.startTime) this.startTime = currentTime;
    
    const elapsed = currentTime - this.startTime;
    const progress = Math.min(elapsed / this.duration, 1);
    const easedProgress = this.easeOutQuad(progress);
    
    const currentValue = this.startValue + (this.targetValue - this.startValue) * easedProgress;
    
    // Format the number
    const displayValue = this.formatNumber(currentValue);
    this.element.textContent = displayValue + this.suffix;
    
    if (progress < 1) {
      requestAnimationFrame((time) => this.animate(time));
    }
  }

  /**
   * Format number for display
   */
  formatNumber(value) {
    // Check if target has decimal places
    const hasDecimal = this.targetValue % 1 !== 0;
    
    if (hasDecimal) {
      return value.toFixed(1);
    }
    return Math.floor(value).toString();
  }

  /**
   * Reset the counter
   */
  reset() {
    this.hasAnimated = false;
    this.element.textContent = '0' + this.suffix;
  }
}

/**
 * Counter Manager
 * Manages all counter animations on the page
 */
class CounterManager {
  constructor() {
    this.counters = [];
    this.observer = null;
  }

  /**
   * Initialize all counters on the page
   */
  init() {
    const counterElements = document.querySelectorAll('.stat-counter');
    
    counterElements.forEach(element => {
      const target = element.getAttribute('data-target');
      const suffix = element.getAttribute('data-suffix') || '';
      const duration = parseInt(element.getAttribute('data-duration')) || 2500;
      
      const counter = new CounterAnimation(element, target, duration, suffix);
      this.counters.push({ element, counter });
    });

    // Set up Intersection Observer to trigger counters
    if ('IntersectionObserver' in window) {
      this.setupObserver();
    } else {
      // Fallback: start all counters immediately
      this.startAllCounters();
    }
  }

  /**
   * Set up Intersection Observer for counters
   */
  setupObserver() {
    this.observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const counterData = this.counters.find(c => c.element === entry.target);
          if (counterData) {
            counterData.counter.start();
          }
        }
      });
    }, {
      threshold: 0.5
    });

    this.counters.forEach(({ element }) => {
      this.observer.observe(element);
    });
  }

  /**
   * Start all counters immediately (fallback)
   */
  startAllCounters() {
    this.counters.forEach(({ counter }) => {
      counter.start();
    });
  }
}

// Initialize counters when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  
  if (!prefersReducedMotion) {
    const counterManager = new CounterManager();
    counterManager.init();
  }
});

// Export for potential use in other scripts
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { CounterAnimation, CounterManager };
}
