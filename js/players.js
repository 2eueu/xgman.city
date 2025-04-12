Promise.all([
    fetch('data/xg_data.json').then(res => res.json()),
    fetch('data/full_players.json').then(res => res.json())
  ])
    .then(([xgData, playersData]) => {
      const shots = [...xgData.home_shots, ...xgData.away_shots];
  
      const brentfordContainer = document.getElementById('brentford-container');
      const manCityContainer = document.getElementById('mancity-container');
      if (!brentfordContainer || !manCityContainer) return;
  
      brentfordContainer.innerHTML = '';
      manCityContainer.innerHTML = '';
  
      const playersMap = {};
      shots.forEach(shot => {
        const name = shot.player;
        if (!playersMap[name]) {
          playersMap[name] = {
            xG: 0,
            minutes: 0,
            events: []
          };
        }
  
        playersMap[name].xG += parseFloat(shot.xG);
        playersMap[name].minutes = Math.max(playersMap[name].minutes, parseInt(shot.minute));
        playersMap[name].events.push({
          minute: shot.minute,
          xG: parseFloat(shot.xG),
          result: shot.result,
          assist: shot.player_assisted || null
        });
      });
  
      const allPlayers = [
        ...playersData["Brentford"].map(p => ({ ...p, team: "Brentford" })),
        ...playersData["Manchester City"].map(p => ({ ...p, team: "Manchester City" }))
      ];
  
      allPlayers.forEach(player => {
        const data = playersMap[player.name] || {
          xG: 0,
          minutes: player.minutes,
          events: []
        };
  
        const card = document.createElement('div');
        card.className = 'player-card';
  
        const fileName = player.name
          .toLowerCase()
          .normalize("NFD")
          .replace(/[\u0300-\u036f]/g, "")
          .replace(/ø/g, "o")
          .replace(/æ/g, "ae")
          .replace(/ß/g, "ss")
          .replace(/[^a-z0-9 ]/g, "")
          .replaceAll(" ", "-");
  
        const imgSrc = `assets/players/${fileName}.png`;
        const isGoalkeeper = player.position === "GK";
  
        const eventsHtml = data.events.length > 0
          ? data.events.map(ev => {
              let text = `${ev.result} at ${ev.minute}' (xG: ${ev.xG.toFixed(2)})`;
              if (ev.result === 'Goal' && ev.assist) {
                text += ` | Assist: ${ev.assist}`;
              }
              return `<li>⚽ ${text}</li>`;
            }).join('')
          : isGoalkeeper
            ? '<li class="info-item goalkeeper">🧤 Goalkeeper</li>'
            : '<li class="info-item no-event">📭 No shot events</li>';
  
        card.innerHTML = `
          <img 
            src="${imgSrc}" 
            alt="${player.name}" 
            onerror="this.onerror=null; this.src='assets/players/default.png'" 
            loading="lazy"
          >
          <h3>${player.name}</h3>
          <p>${player.position || "?"} | ${player.minutes || "-"}' played | xG: ${data.xG.toFixed(2)}</p>
          <ul>${eventsHtml}</ul>
        `;
  
        if (player.team === "Brentford") {
          brentfordContainer.appendChild(card);
        } else {
          manCityContainer.appendChild(card);
        }
      });
    })
    .catch(err => {
      console.error("❌ players.js error:", err);
    });
  