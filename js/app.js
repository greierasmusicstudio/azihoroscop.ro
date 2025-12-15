/* =========================================
   1. CANVAS BACKGROUND (STELE ANIMATE)
   ========================================= */
const canvas = document.getElementById('star-canvas');

// Rulăm animația doar dacă avem elementul canvas în pagină
if (canvas) {
    const ctx = canvas.getContext('2d');
    let width, height, stars = [];

    function initCanvas() {
        width = window.innerWidth;
        height = window.innerHeight;
        canvas.width = width;
        canvas.height = height;
        createStars();
    }

    function createStars() {
        stars = [];
        // Mai puține stele pe mobil (50) vs desktop (150) pentru performanță
        const count = width > 768 ? 150 : 50; 
        for (let i = 0; i < count; i++) {
            stars.push({
                x: Math.random() * width,
                y: Math.random() * height,
                radius: Math.random() * 1.5,
                speed: Math.random() * 0.3,
                alpha: Math.random()
            });
        }
    }

    function animateStars() {
        ctx.clearRect(0, 0, width, height);
        
        stars.forEach(star => {
            ctx.fillStyle = `rgba(255, 255, 255, ${star.alpha})`;
            ctx.beginPath();
            ctx.arc(star.x, star.y, star.radius, 0, Math.PI * 2);
            ctx.fill();
            
            // Mișcare în sus
            star.y -= star.speed;
            // Resetare când iese din ecran
            if (star.y < 0) {
                star.y = height;
                star.x = Math.random() * width;
            }
            
            // Efect de sclipire
            star.alpha += (Math.random() - 0.5) * 0.02;
            if (star.alpha < 0.1) star.alpha = 0.1;
            if (star.alpha > 0.8) star.alpha = 0.8;
        });
        
        requestAnimationFrame(animateStars);
    }

    window.addEventListener('resize', initCanvas);
    initCanvas();
    animateStars();
}

/* =========================================
   2. ZODIAC DATA LOADER
   ========================================= */

async function loadZodiacData(zodiaKey) {
    // Definim elementele din HTML unde vom pune textul
    const els = {
        date: document.getElementById('date-display'),
        general: document.getElementById('txt-general'),
        love: document.getElementById('txt-love'),
        money: document.getElementById('txt-money'),
        number: document.getElementById('val-number'),
        color: document.getElementById('val-color'),
        mood: document.getElementById('val-mood')
    };

    try {
        // Încărcăm fișierul JSON. 
        // Fiind în folderul 'content', calea este directă 'daily_data.json'
        const response = await fetch('daily_data.json');
        
        if (!response.ok) throw new Error("Eroare rețea");
        
        const data = await response.json();
        
        // Verificăm dacă avem date pentru zodia cerută
        const zodiacData = data[zodiaKey];

        if (zodiacData) {
            // Actualizăm data valabilității
            if (els.date && data.meta) els.date.innerText = data.meta.data_valabilitate;

            // Funcție mică pentru efect de fade-in la text
            const setText = (el, text) => {
                if(el) {
                    el.style.opacity = 0;
                    el.innerText = text;
                    setTimeout(() => el.style.opacity = 1, 300);
                }
            };

            setText(els.general, zodiacData.general);
            setText(els.love, zodiacData.dragoste);
            setText(els.money, zodiacData.bani);
            
            if(els.number) els.number.innerText = zodiacData.noroc_nr;
            if(els.color) els.color.innerText = zodiacData.noroc_culoare;
            if(els.mood) els.mood.innerText = zodiacData.stare;
        } else {
            if(els.general) els.general.innerText = "Datele se actualizează...";
        }

    } catch (err) {
        console.error("Eroare la încărcare:", err);
        if(els.general) els.general.innerText = "Conexiunea cu astrele este instabilă. Reîncercați.";
    }
}