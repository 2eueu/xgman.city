// ✅ main.js → xG 차트 전용만 유지
fetch('data/xg_data.json')
  .then(res => res.json())
  .then(data => {
    const { home_shots, away_shots } = data;
    const shots = [...home_shots, ...away_shots];

    // === Shot Map ===
    const ctxShot = document.getElementById('shotMap')?.getContext('2d');
    if (ctxShot) {
      const makeDataset = (label, shotArr, color, radius) => ({
        label,
        data: shotArr.map(s => ({
          x: parseFloat(s.X),
          y: parseFloat(s.Y),
          player: s.player,
          xG: parseFloat(s.xG)
        })),
        backgroundColor: color,
        pointRadius: radius
      });

      const homeGoals = home_shots.filter(s => s.result === "Goal");
      const homeOthers = home_shots.filter(s => s.result !== "Goal");
      const awayGoals = away_shots.filter(s => s.result === "Goal");
      const awayOthers = away_shots.filter(s => s.result !== "Goal");

      new Chart(ctxShot, {
        type: 'scatter',
        data: {
          datasets: [
            makeDataset('Brentford Shots', homeOthers, 'rgba(255, 99, 132, 0.4)', 5),
            makeDataset('Brentford Goals', homeGoals, 'rgba(255, 99, 132, 1)', 8),
            makeDataset('Man City Shots', awayOthers, 'rgba(54, 162, 235, 0.4)', 5),
            makeDataset('Man City Goals', awayGoals, 'rgba(54, 162, 235, 1)', 8),
          ]
        },
        options: {
          scales: {
            x: { min: 0, max: 1, title: { display: true, text: 'Pitch X' }},
            y: { min: 0, max: 1, title: { display: true, text: 'Pitch Y' }}
          },
          plugins: {
            tooltip: {
              callbacks: {
                label: function(context) {
                  const shot = context.raw;
                  return `${shot.player} | xG: ${shot.xG.toFixed(2)}`;
                }
              }
            },
            legend: { position: 'top' }
          }
        }
      });
    }

    // === Player xG Bar Chart ===
    const ctxBar = document.getElementById('xgBarChart')?.getContext('2d');
    if (ctxBar) {
      const playerXGMap = {};
      shots.forEach(s => {
        const name = s.player;
        const xg = parseFloat(s.xG);
        if (!playerXGMap[name]) playerXGMap[name] = 0;
        playerXGMap[name] += xg;
      });

      new Chart(ctxBar, {
        type: 'bar',
        data: {
          labels: Object.keys(playerXGMap),
          datasets: [{
            label: 'xG',
            data: Object.values(playerXGMap),
            backgroundColor: '#6cabdd'
          }]
        },
        options: {
          indexAxis: 'y',
          plugins: { legend: { display: false } },
          scales: { x: { beginAtZero: true } }
        }
      });
    }
  });
