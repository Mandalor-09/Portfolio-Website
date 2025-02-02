const portfolioData = {
    education: [
      { name: "Ph.D. Data Science", institution: "Stanford University", year: "2022" },
      { name: "M.S. Computer Science", institution: "MIT", year: "2018" },
      { name: "B.S. Mathematics", institution: "Harvard University", year: "2016" },
    ],
    experience: [
      { title: "Senior Data Scientist", company: "Google", year: "2022-Present" },
      { title: "Data Scientist", company: "Amazon", year: "2020-2022" },
      { title: "Data Science Intern", company: "Facebook", year: "Summer 2019" },
    ],
    skills: ["Python", "R", "Machine Learning", "Deep Learning", "SQL", "Data Visualization", "Big Data", "Statistics"],
    projects: [
      { name: "Predictive Maintenance System", description: "ML model for equipment failure prediction" },
      { name: "Customer Churn Analysis", description: "Predictive model for customer retention" },
      { name: "NLP Sentiment Analysis", description: "Analyzing customer reviews for product improvement" },
      { name: "Stock Price Forecasting", description: "Deep learning model for stock price prediction" },
    ],
  }
  
  // Import particlesJS library.  This assumes it's available via a script tag in your HTML or a module import.
  // If using a CDN, ensure the script is included before this JavaScript file.
  // If using a module import, adjust accordingly (e.g., import particlesJS from 'particles.js';).
  
  //This is a placeholder.  You'll need to actually import particlesJS from wherever it's located.
  //For example, if it's a CDN, include it in your HTML file.  If it's a module, use an import statement.
  let particlesJS // Declare particlesJS variable
  
  // Particle.js configuration
  particlesJS("particles-js", {
    particles: {
      number: { value: 80, density: { enable: true, value_area: 800 } },
      color: { value: "#ffffff" },
      shape: {
        type: "circle",
        stroke: { width: 0, color: "#000000" },
        polygon: { nb_sides: 5 },
        image: { src: "img/github.svg", width: 100, height: 100 },
      },
      opacity: { value: 0.5, random: false, anim: { enable: false, speed: 1, opacity_min: 0.1, sync: false } },
      size: { value: 3, random: true, anim: { enable: false, speed: 40, size_min: 0.1, sync: false } },
      line_linked: { enable: true, distance: 150, color: "#ffffff", opacity: 0.4, width: 1 },
      move: {
        enable: true,
        speed: 6,
        direction: "none",
        random: false,
        straight: false,
        out_mode: "out",
        bounce: false,
        attract: { enable: false, rotateX: 600, rotateY: 1200 },
      },
    },
    interactivity: {
      detect_on: "canvas",
      events: { onhover: { enable: true, mode: "repulse" }, onclick: { enable: true, mode: "push" }, resize: true },
      modes: {
        grab: { distance: 400, line_linked: { opacity: 1 } },
        bubble: { distance: 400, size: 40, duration: 2, opacity: 8, speed: 3 },
        repulse: { distance: 200, duration: 0.4 },
        push: { particles_nb: 4 },
        remove: { particles_nb: 2 },
      },
    },
    retina_detect: true,
  })
  
  const canvas = document.getElementById("background-canvas")
  const ctx = canvas.getContext("2d")
  let particles = []
  
  function resizeCanvas() {
    canvas.width = window.innerWidth
    canvas.height = window.innerHeight
  }
  
  function createParticles() {
    particles = []
    const particleCount = 100
    for (let i = 0; i < particleCount; i++) {
      particles.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        radius: Math.random() * 2 + 1,
        color: `rgba(255, 255, 255, ${Math.random() * 0.5 + 0.5})`,
        velocity: {
          x: (Math.random() - 0.5) * 2,
          y: (Math.random() - 0.5) * 2,
        },
      })
    }
  }
  
  function drawParticles() {
    ctx.clearRect(0, 0, canvas.width, canvas.height)
    particles.forEach((particle) => {
      ctx.beginPath()
      ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2)
      ctx.fillStyle = particle.color
      ctx.fill()
  
      particle.x += particle.velocity.x
      particle.y += particle.velocity.y
  
      if (particle.x < 0 || particle.x > canvas.width) particle.velocity.x *= -1
      if (particle.y < 0 || particle.y > canvas.height) particle.velocity.y *= -1
    })
  }
  
  function animate() {
    drawParticles()
    requestAnimationFrame(animate)
  }
  
  window.addEventListener("resize", () => {
    resizeCanvas()
    createParticles()
  })
  
  resizeCanvas()
  createParticles()
  animate()
  
  // Navigation and info panel functionality
  const infoPanel = document.getElementById("info-panel")
  const buttons = document.querySelectorAll("nav button")
  
  buttons.forEach((button) => {
    button.addEventListener("click", () => {
      const section = button.dataset.section
      updateInfoPanel(section)
    })
  })
  
  function updateInfoPanel(section) {
    let content = `<h2>${section.charAt(0).toUpperCase() + section.slice(1)}</h2>`
  
    portfolioData[section].forEach((item) => {
      content += '<div class="info-item">'
      if (section === "education" || section === "experience") {
        content += `<h3>${item.name || item.title}</h3>`
        content += `<p>${item.institution || item.company} (${item.year})</p>`
      } else if (section === "skills") {
        content += `<p>${item}</p>`
      } else if (section === "projects") {
        content += `<h3>${item.name}</h3>`
        content += `<p>${item.description}</p>`
      }
      content += "</div>"
    })
  
    infoPanel.innerHTML = content
  }
  
  // Initialize with education section
  updateInfoPanel("education")
  
  // Dark mode toggle
  // Mobile menu toggle
  //These are now handled in the DOMContentLoaded event listener below.
  
  // Skill circle animation
  const skillCircles = document.querySelectorAll(".skill-circle")
  
  const animateSkillCircle = (circle) => {
    const percent = circle.getAttribute("data-percent")
    const radius = circle.querySelector(".skill-circle-inner").offsetWidth / 2
    const circumference = 2 * Math.PI * radius
    const offset = circumference - (percent / 100) * circumference
  
    circle.style.strokeDasharray = `${circumference} ${circumference}`
    circle.style.strokeDashoffset = offset
  }
  
  const observerOptions = {
    root: null,
    rootMargin: "0px",
    threshold: 0.5,
  }
  
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        animateSkillCircle(entry.target)
      }
    })
  }, observerOptions)
  
  skillCircles.forEach((circle) => {
    observer.observe(circle)
  })
  
  // Back to top button
  const backToTopBtn = document.getElementById("back-to-top")
  
  window.addEventListener("scroll", () => {
    if (window.pageYOffset > 300) {
      backToTopBtn.classList.add("show")
    } else {
      backToTopBtn.classList.remove("show")
    }
  })
  
  backToTopBtn.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" })
  })
  
  // Form submission
  const contactForm = document.getElementById("contact-form")
  
  contactForm.addEventListener("submit", (e) => {
    e.preventDefault()
    // Add your form submission logic here
    alert("Thank you for your message! I will get back to you soon.")
    contactForm.reset()
  })
  
  document.addEventListener("DOMContentLoaded", (event) => {
    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
      anchor.addEventListener("click", function (e) {
        e.preventDefault()
        document.querySelector(this.getAttribute("href")).scrollIntoView({
          behavior: "smooth",
        })
      })
    })
  
    // Animate skill bars on scroll
    const skillBars = document.querySelectorAll(".progress")
    const animateSkillBars = () => {
      skillBars.forEach((bar) => {
        const barTop = bar.getBoundingClientRect().top
        if (barTop < window.innerHeight - 50) {
          bar.style.width = bar.parentElement.getAttribute("data-progress") + "%"
        }
      })
    }
  
    window.addEventListener("scroll", animateSkillBars)
    animateSkillBars() // Initial check on page load
  
    // Add hover effect for project cards
    const projectCards = document.querySelectorAll(".project-card")
    projectCards.forEach((card) => {
      card.addEventListener("mouseenter", () => {
        card.querySelector(".project-overlay").style.opacity = "1"
      })
      card.addEventListener("mouseleave", () => {
        card.querySelector(".project-overlay").style.opacity = "0"
      })
    })
  
    // Animate on scroll
    const animateOnScroll = () => {
      const elements = document.querySelectorAll(".animate-on-scroll")
      elements.forEach((element) => {
        const elementTop = element.getBoundingClientRect().top
        const elementBottom = element.getBoundingClientRect().bottom
        if (elementTop < window.innerHeight && elementBottom > 0) {
          element.classList.add("animate")
        }
      })
    }
  
    window.addEventListener("scroll", animateOnScroll)
    animateOnScroll() // Initial check on page load
  
    // Dark mode toggle
    const darkModeToggle = document.getElementById("dark-mode-toggle")
    const body = document.body
  
    darkModeToggle.addEventListener("change", () => {
      body.classList.toggle("dark-mode")
    })
  
    // Mobile menu toggle
    const menuBtn = document.querySelector(".menu-btn")
    const navLinks = document.querySelector(".nav-links")
  
    menuBtn.addEventListener("click", () => {
      navLinks.classList.toggle("show")
      menuBtn.classList.toggle("open")
    })
  
    // Skill progress animation
    const skillCards = document.querySelectorAll(".skill-card")
  
    const animateSkillProgress = (entries, observer) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const progressBar = entry.target.querySelector(".skill-progress")
          progressBar.style.width = progressBar.dataset.progress
          observer.unobserve(entry.target)
        }
      })
    }
  
    const skillObserver = new IntersectionObserver(animateSkillProgress, {
      threshold: 0.5,
    })
  
    skillCards.forEach((card) => {
      skillObserver.observe(card)
    })
  
    // Project filtering
    const filterButtons = document.querySelectorAll(".filter-btn")
    const projectCards2 = document.querySelectorAll(".project-card") //Using a different variable name to avoid conflict
  
    filterButtons.forEach((button) => {
      button.addEventListener("click", () => {
        const filter = button.dataset.filter
  
        filterButtons.forEach((btn) => btn.classList.remove("active"))
        button.classList.add("active")
  
        projectCards2.forEach((card) => {
          //Using the different variable name here
          if (filter === "all" || card.dataset.category === filter) {
            card.style.display = "block"
            setTimeout(() => {
              card.style.opacity = "1"
              card.style.transform = "scale(1)"
            }, 10)
          } else {
            card.style.opacity = "0"
            card.style.transform = "scale(0.8)"
            setTimeout(() => {
              card.style.display = "none"
            }, 300)
          }
        })
      })
    })
  
    // Smooth scrolling for navigation links (already handled above)
  
    // Back to top button (already handled above)
  
    // Form submission (already handled above)
  })
  
  
// Download Resume

function downloadResume() {
  // Change the path below to where your resume is stored
  const resumePath = 'static/omsingh_ds_cv.pdf'; // e.g., 'files/my_resume.pdf'
  const link = document.createElement('a');
  link.href = resumePath;
  link.download = 'My_Resume.pdf'; // Name for the downloaded file
  link.click();
}