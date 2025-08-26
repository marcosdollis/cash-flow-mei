document.addEventListener('DOMContentLoaded', function() {
    // Contador para estatísticas
    const counters = document.querySelectorAll('.counter');
    counters.forEach(counter => {
        const target = parseInt(counter.textContent);
        counter.textContent = '0';
        
        const countUp = () => {
            const count = parseInt(counter.textContent);
            const increment = target / 30; // Ajuste a velocidade aqui
            
            if (count < target) {
                counter.textContent = Math.ceil(count + increment);
                setTimeout(countUp, 30);
            } else {
                counter.textContent = target;
            }
        };
        
        // Inicia animação quando o elemento está visível
        const observer = new IntersectionObserver((entries) => {
            if (entries[0].isIntersecting) {
                countUp();
                observer.disconnect();
            }
        });
        
        observer.observe(counter);
    });

    // Slider de localizações com crescimento exponencial
    const locationSlider = document.getElementById('locationSlider');
    const reachValue = document.getElementById('reachValue');
    const costPerView = document.getElementById('costPerView');
    
    if (locationSlider) {
        // Inicializar com os valores corretos
        const initialLocations = parseInt(locationSlider.value);
        const initialReach = Math.round(500 * Math.pow(1.15, initialLocations - 1));
        const initialCost = (250 / initialReach).toFixed(2);
        
        reachValue.textContent = initialReach;
        costPerView.textContent = `R$ ${initialCost}`;
        
        locationSlider.addEventListener('input', function() {
            const locations = parseInt(this.value);
            // Crescimento exponencial suave
            const reach = Math.round(500 * Math.pow(15, locations - 1));
            const cost = (250 / reach).toFixed(2);
            
            reachValue.textContent = reach;
            costPerView.textContent = `R$ ${cost}`;
        });
    }

    // Animação de pontos no mapa
    setTimeout(() => {
        const futurePoints = document.querySelectorAll('.point.future');
        futurePoints.forEach((point, index) => {
            setTimeout(() => {
                point.classList.remove('future');
                point.classList.add('active');
            }, index * 1000);
        });
    }, 2000);
});
