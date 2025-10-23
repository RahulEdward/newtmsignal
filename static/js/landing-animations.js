/**
 * TradingMaven Landing Page Animations
 * Handles scroll-triggered animations, parallax effects, and interactive elements
 */

class ScrollAnimations {
  constructor() {
    this.observerOptions = {
      threshold: 0.1,
      rootMargin: '0px 0px -100px 0px'
    };
    this.observer = null;
  }

  /**
   * Initialize all scroll-based animations
   */
  init() {
    // Check if Intersection Observer is supported
    if ('IntersectionObserver' in window) {
      this.setupIntersectionObserver();
    } else {
      // Fallback: show all elements immediately
      this.showAllElements();
    }

    // Initialize smooth scroll for anchor links
    this.initSmoothScroll();
  }

  /**
   * Set up Intersection Observer for scroll animations
   */
  setupIntersectionObserver() {
    this.observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          // Optionally unobserve after animation
          // this.observer.unobserve(entry.target);
        }
      });
    }, this.observerOptions);

    // Observe all elements with scroll animation classes
    this.observeElements();
  }

  /**
   * Observe all elements that should animate on scroll
   */
  observeElements() {
    const animatedElements = document.querySelectorAll(
      '.scroll-fade-in, .scroll-scale-in'
    );

    animatedElements.forEach(element => {
      this.observer.observe(element);
    });
  }

  /**
   * Fallback: Show all elements immediately if Intersection Observer not supported
   */
  showAllElements() {
    const animatedElements = document.querySelectorAll(
      '.scroll-fade-in, .scroll-scale-in'
    );

    animatedElements.forEach(element => {
      element.classList.add('is-visible');
    });
  }

  /**
   * Initialize smooth scrolling for anchor links
   */
  initSmoothScroll() {
    // Add smooth scroll behavior to HTML element
    document.documentElement.style.scrollBehavior = 'smooth';

    // Handle anchor link clicks
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', (e) => {
        const href = anchor.getAttribute('href');
        
        // Skip if href is just "#"
        if (href === '#') return;

        const target = document.querySelector(href);
        if (target) {
          e.preventDefault();
          target.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
          });
        }
      });
    });
  }
}

/**
 * Navbar Scroll Effects
 * Handles navbar appearance changes on scroll
 */
class NavbarScroll {
  constructor() {
    this.navbar = document.querySelector('nav');
    this.scrollThreshold = 50;
    this.isScrolled = false;
  }

  /**
   * Initialize navbar scroll listener
   */
  init() {
    if (!this.navbar) return;

    // Throttle scroll events for better performance
    let ticking = false;

    window.addEventListener('scroll', () => {
      if (!ticking) {
        window.requestAnimationFrame(() => {
          this.updateNavbar();
          ticking = false;
        });
        ticking = true;
      }
    });

    // Initial check
    this.updateNavbar();
  }

  /**
   * Update navbar styling based on scroll position
   */
  updateNavbar() {
    const scrollPosition = window.scrollY;

    if (scrollPosition > this.scrollThreshold && !this.isScrolled) {
      this.navbar.classList.add('navbar-scrolled');
      this.isScrolled = true;
    } else if (scrollPosition <= this.scrollThreshold && this.isScrolled) {
      this.navbar.classList.remove('navbar-scrolled');
      this.isScrolled = false;
    }
  }
}

/**
 * Ripple Effect for Buttons
 * Creates a ripple animation on button click
 */
class RippleEffect {
  /**
   * Initialize ripple effect on all buttons with ripple-container class
   */
  static init() {
    const rippleButtons = document.querySelectorAll('.ripple-container');

    rippleButtons.forEach(button => {
      button.addEventListener('click', function(e) {
        RippleEffect.createRipple(e, this);
      });
    });
  }

  /**
   * Create ripple effect at click position
   */
  static createRipple(event, element) {
    const ripple = document.createElement('span');
    ripple.classList.add('ripple');

    // Get click position relative to button
    const rect = element.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = event.clientX - rect.left - size / 2;
    const y = event.clientY - rect.top - size / 2;

    ripple.style.width = ripple.style.height = size + 'px';
    ripple.style.left = x + 'px';
    ripple.style.top = y + 'px';

    element.appendChild(ripple);

    // Remove ripple after animation
    setTimeout(() => {
      ripple.remove();
    }, 600);
  }
}

/**
 * Initialize all animations when DOM is ready
 */
document.addEventListener('DOMContentLoaded', () => {
  // Check for reduced motion preference
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  if (!prefersReducedMotion) {
    // Initialize scroll animations
    const scrollAnimations = new ScrollAnimations();
    scrollAnimations.init();

    // Initialize navbar scroll effects
    const navbarScroll = new NavbarScroll();
    navbarScroll.init();

    // Initialize ripple effects
    RippleEffect.init();
  } else {
    // For users who prefer reduced motion, show all elements immediately
    const scrollAnimations = new ScrollAnimations();
    scrollAnimations.showAllElements();
  }
});

// Export for potential use in other scripts
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { ScrollAnimations, NavbarScroll, RippleEffect };
}
