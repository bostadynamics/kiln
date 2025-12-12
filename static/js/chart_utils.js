class PatternChart {
    constructor(canvasId) {
        this.ctx = document.getElementById(canvasId).getContext('2d');
        this.chart = null;
    }

    init(showCurrentTemp = false) {
        const datasets = [
            {
                label: 'Temperature Pattern',
                data: [],
                borderColor: '#3b82f6',
                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                borderWidth: 3,
                pointBackgroundColor: '#1e1e1e',
                pointBorderColor: '#60a5fa',
                pointBorderWidth: 2,
                pointRadius: 4,
                fill: true,
                tension: 0.1,
                order: 2
            }
        ];

        if (showCurrentTemp) {
            datasets.push({
                label: 'Current Temp',
                data: [],
                borderColor: '#ef4444',
                borderWidth: 2,
                pointRadius: 0,
                borderDash: [5, 5],
                fill: false,
                order: 1
            });
        }

        this.chart = new Chart(this.ctx, {
            type: 'line',
            data: {
                labels: [], // Time labels
                datasets: datasets
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                        backgroundColor: 'rgba(17, 24, 39, 0.9)',
                        titleColor: '#fff',
                        bodyColor: '#9ca3af',
                        borderColor: '#374151',
                        borderWidth: 1
                    }
                },
                scales: {
                    x: {
                        type: 'linear', // Use linear scale for proper spacing
                        grid: { color: '#374151' },
                        ticks: { color: '#9ca3af' },
                        title: { display: true, text: 'Time (minutes)', color: '#6b7280' }
                    },
                    y: {
                        grid: { color: '#374151' },
                        ticks: { color: '#9ca3af' },
                        title: { display: true, text: 'Temperature (°C)', color: '#6b7280' },
                        beginAtZero: true
                    }
                },
                animation: {
                    duration: 0 // Disable animation for better performance on updates
                }
            }
        });
    }

    updatePattern(steps) {
        if (!this.chart) return;

        const points = [];
        let currentTime = 0;
        let currentTemp = 25; // Default start

        // Initial point
        points.push({ x: currentTime, y: currentTemp });

        steps.forEach(step => {
            // Logic reused from patterns.html
            // If time > 0, we add a segment.
            // If it's step 7 and time is 0, it might be the end.
            if (step.time > 0 || (step.step === 7 && step.time === 0)) {
                currentTime += step.time;
                currentTemp = step.temp; // Step temp is target temp at end of time?
                // Delta manual implies it ramps to 'temp' over 'time'.
                points.push({ x: currentTime, y: currentTemp });
            }
        });

        this.chart.data.datasets[0].data = points;
        this.chart.update();
        return currentTime; // Return max time
    }

    updateCurrentTempLine(pv, maxTime) {
        if (!this.chart || this.chart.data.datasets.length < 2) return;

        // Horizontal line
        const maxX = Math.max(maxTime, 10); // Ensure at least some width
        this.chart.data.datasets[1].data = [
            { x: 0, y: pv },
            { x: maxX, y: pv }
        ];
        this.chart.update('none');
    }
}
