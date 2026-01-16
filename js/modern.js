/* ========================================
   MODERN COLLEGE WEBSITE - JAVASCRIPT
   ======================================== */

document.addEventListener('DOMContentLoaded', function () {

    // ========== STICKY NAVBAR ==========
    const navbar = document.querySelector('.navbar');

    window.addEventListener('scroll', function () {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // ========== MOBILE MENU TOGGLE ==========
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const navMenu = document.querySelector('.nav-menu');

    if (mobileMenuToggle) {
        mobileMenuToggle.addEventListener('click', function () {
            navMenu.classList.toggle('active');
        });
    }

    // ========== TAB SWITCHING ==========
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(button => {
        button.addEventListener('click', function () {
            const targetTab = this.getAttribute('data-tab');

            // Remove active class from all buttons and contents
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));

            // Add active class to clicked button and corresponding content
            this.classList.add('active');
            document.getElementById(targetTab).classList.add('active');
        });
    });

    // ========== AUTO-SCROLL TABS (Pause on Hover) ==========
    const tabContentAreas = document.querySelectorAll('.tab-content');

    tabContentAreas.forEach(content => {
        let scrollInterval;

        // Auto-scroll
        function startAutoScroll() {
            scrollInterval = setInterval(() => {
                if (content.scrollTop + content.clientHeight >= content.scrollHeight) {
                    content.scrollTop = 0; // Reset to top
                } else {
                    content.scrollTop += 1; // Scroll down
                }
            }, 50);
        }

        // Pause on hover
        content.addEventListener('mouseenter', () => {
            clearInterval(scrollInterval);
        });

        // Resume on mouse leave
        content.addEventListener('mouseleave', () => {
            startAutoScroll();
        });

        // Start scrolling if tab is active
        if (content.classList.contains('active')) {
            startAutoScroll();
        }
    });

    // ========== SMOOTH SCROLL FOR ANCHOR LINKS ==========
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href !== '#' && document.querySelector(href)) {
                e.preventDefault();
                document.querySelector(href).scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // ========== DROPDOWN MENU (Mobile) ==========
    const dropdownToggles = document.querySelectorAll('.nav-item.dropdown');

    dropdownToggles.forEach(item => {
        const link = item.querySelector('.nav-link');
        const menu = item.querySelector('.dropdown-menu');

        if (link && menu) {
            link.addEventListener('click', function (e) {
                if (window.innerWidth <= 768) {
                    e.preventDefault();
                    menu.style.display = menu.style.display === 'block' ? 'none' : 'block';
                }
            });
        }
    });

});
