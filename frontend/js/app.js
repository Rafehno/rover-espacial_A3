// ── Estado global ─────────────────────────────────────────────────────────
let obstacles = [];
let steps = [];
let currentStep = -1;
let animTimer = null;

let roverState = { x: 0, y: 0, dir: 'N' };
let gridConfig = { width: 10, height: 10 };
let trail = [];  

// ── p5.js sketch ─────────────────────────────────────────────────────────
const sketch = (p) => {
  const CELL = 44;
  const PAD  = 2;

  p.setup = () => {
    const wrapper = document.getElementById('canvas-wrapper');
    const w = wrapper.clientWidth  || 480;
    const h = wrapper.clientHeight || 480;
    const canvas = p.createCanvas(w, h);
    canvas.parent('canvas-wrapper');
    p.noLoop();
    drawGrid(p, CELL, PAD);
  };

  p.draw = () => {
    drawGrid(p, CELL, PAD);
  };

  p.mousePressed = () => {
    const col = Math.floor((p.mouseX - PAD) / CELL);
    const row = Math.floor((p.mouseY - PAD) / CELL);
    if (col < 0 || row < 0 || col >= gridConfig.width || row >= gridConfig.height) return;

    const idx = obstacles.findIndex(o => o[0] === col && o[1] === row);
    if (idx >= 0) {
      obstacles.splice(idx, 1);
    } else {
      obstacles.push([col, row]);
    }
    p.redraw();
  };

  p.windowResized = () => {
    const wrapper = document.getElementById('canvas-wrapper');
    p.resizeCanvas(wrapper.clientWidth || 480, wrapper.clientHeight || 480);
    p.redraw();
  };

  function drawGrid(p, cell, pad) {
    p.background('#090c18');

    const cols = gridConfig.width;
    const rows = gridConfig.height;

    for (let r = 0; r < rows; r++) {
      for (let c = 0; c < cols; c++) {
        const x = pad + c * cell;
        const y = pad + r * cell;

        if (trail.some(t => t[0] === c && t[1] === r)) {
          p.fill('#1a3a5c');
        } else {
          p.fill('#0f1322');
        }

        if (obstacles.some(o => o[0] === c && o[1] === r)) {
          p.fill('#5c1a1a');
        }

        p.stroke('#1f2540');
        p.strokeWeight(1);
        p.rect(x, y, cell - 1, cell - 1, 3);
      }
    }

    obstacles.forEach(([c, r]) => {
      const x = pad + c * cell;
      const y = pad + r * cell;
      p.fill('#ef5350');
      p.noStroke();
      p.textAlign(p.CENTER, p.CENTER);
      p.textSize(cell * 0.45);
      p.text('✕', x + cell / 2, y + cell / 2);
    });

    drawRover(p, roverState.x, roverState.y, roverState.dir, cell, pad);
  }

  function drawRover(p, col, row, dir, cell, pad) {
    const x = pad + col * cell + cell / 2;
    const y = pad + row * cell + cell / 2;
    const r = cell * 0.32;

    p.push();
    p.translate(x, y);

    const angles = { N: 0, E: p.HALF_PI, S: p.PI, W: -p.HALF_PI };
    p.rotate(angles[dir] || 0);

    p.fill('#4fc3f7');
    p.noStroke();
    p.ellipse(0, 0, r * 2, r * 2);

    p.fill('#0b0e1a');
    p.triangle(0, -r * 0.85, -r * 0.45, r * 0.4, r * 0.45, r * 0.4);

    p.pop();
  }
};

const p5instance = new p5(sketch);

// Redesenha o canvas com o estado atual
function redrawCanvas() {
  p5instance.redraw();
}

// ── Funções de UI ─────────────────────────────────────────────────────────

function setStatus(text, type = 'secondary') {
  const badge = document.getElementById('status-badge');
  badge.textContent = text;
  badge.className = `badge bg-${type}`;
}

function addLog(message, cls = 'log-info') {
  const panel = document.getElementById('log-panel');
  const line = document.createElement('div');
  line.className = cls;
  line.textContent = message;
  panel.appendChild(line);
  panel.scrollTop = panel.scrollHeight;
}

function clearLog() {
  document.getElementById('log-panel').innerHTML = '';
}

function clearObstacles() {
  obstacles = [];
  redrawCanvas();
}

function resetSim() {
  clearAnimTimer();
  steps = [];
  currentStep = -1;
  trail = [];

  const sx = parseInt(document.getElementById('start-x').value) || 0;
  const sy = parseInt(document.getElementById('start-y').value) || 0;
  const sd = document.getElementById('start-dir').value || 'N';

  roverState = { x: sx, y: sy, dir: sd };
  gridConfig = {
    width:  parseInt(document.getElementById('grid-width').value)  || 10,
    height: parseInt(document.getElementById('grid-height').value) || 10,
  };

  clearLog();
  addLog('Simulação reiniciada.', 'log-info');
  setStatus('Pronto', 'secondary');
  redrawCanvas();
}

// ── API calls ─────────────────────────────────────────────────────────────

async function validateScript() {
  const script = document.getElementById('editor').value;
  setStatus('Validando…', 'warning');

  try {
    const res = await fetch('/validate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ script }),
    });
    const data = await res.json();

    clearLog();
    if (data.success) {
      addLog('✓ Sintaxe válida!', 'log-ok');
      setStatus('Válido', 'success');
    } else {
      data.errors.forEach(e => addLog(`✕ Linha ${e.line}: ${e.message}`, 'log-error'));
      setStatus('Erros encontrados', 'danger');
    }
  } catch {
    addLog('Erro de comunicação com o servidor.', 'log-error');
    setStatus('Erro', 'danger');
  }
}

async function runScript() {
  clearAnimTimer();
  const script = document.getElementById('editor').value;

  const payload = {
    script,
    width:     parseInt(document.getElementById('grid-width').value)  || 10,
    height:    parseInt(document.getElementById('grid-height').value) || 10,
    start_x:   parseInt(document.getElementById('start-x').value)    || 0,
    start_y:   parseInt(document.getElementById('start-y').value)    || 0,
    start_dir: document.getElementById('start-dir').value            || 'N',
    obstacles,
  };

  setStatus('Executando…', 'warning');
  clearLog();

  try {
    const res = await fetch('/run', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    const data = await res.json();

    if (!data.success) {
      data.errors.forEach(e => addLog(`✕ Linha ${e.line}: ${e.message}`, 'log-error'));
      setStatus('Erros encontrados', 'danger');
      return;
    }

    steps = data.steps;
    currentStep = -1;
    trail = [];

    // Reinicia posição para o início antes de animar
    roverState = {
      x:   payload.start_x,
      y:   payload.start_y,
      dir: payload.start_dir,
    };
    gridConfig = { width: payload.width, height: payload.height };
    redrawCanvas();

    setStatus('Animando…', 'primary');
    animateSteps(data.steps, data.log);

  } catch {
    addLog('Erro de comunicação com o servidor.', 'log-error');
    setStatus('Erro', 'danger');
  }
}

// ── Animação passo a passo ────────────────────────────────────────────────

// Expande MOVE/BACK em sub-passos de 1 célula para animação fluida
function buildSubSteps(apiSteps, logLines) {
  const DELTAS = { N: [0, -1], E: [1, 0], S: [0, 1], W: [-1, 0] };
  const result = [];

  for (let i = 0; i < apiSteps.length; i++) {
    const step = apiSteps[i];

    if ((step.command === 'MOVE' || step.command === 'BACK') && step.success) {
      const dir = step.before.dir;
      const [fdx, fdy] = DELTAS[dir] || [0, 0];
      const [dx, dy] = step.command === 'MOVE' ? [fdx, fdy] : [-fdx, -fdy];
      const dist = Math.abs(step.after.x - step.before.x) + Math.abs(step.after.y - step.before.y);

      let cx = step.before.x;
      let cy = step.before.y;

      for (let s = 0; s < dist; s++) {
        const nx = cx + dx;
        const ny = cy + dy;
        result.push({
          before:   { x: cx, y: cy, dir },
          after:    { x: nx, y: ny, dir },
          logLine:  s === dist - 1 ? logLines[i] : null,
          logClass: 'log-ok',
        });
        cx = nx;
        cy = ny;
      }

      // Sem células movidas (bloqueio no 1º passo) → ainda mostra o log
      if (dist === 0) {
        result.push({ before: step.before, after: step.after, logLine: logLines[i], logClass: 'log-ok' });
      }
    } else {
      result.push({
        before:   step.before,
        after:    step.after,
        logLine:  logLines[i],
        logClass: step.success ? 'log-ok' : 'log-error',
      });
    }
  }

  return result;
}

function animateSteps(apiSteps, logLines) {
  const subSteps = buildSubSteps(apiSteps, logLines);
  let i = 0;

  function next() {
    if (i >= subSteps.length) {
      setStatus('Concluído', 'success');
      return;
    }

    const sub = subSteps[i];
    trail.push([sub.before.x, sub.before.y]);
    roverState = { x: sub.after.x, y: sub.after.y, dir: sub.after.dir };
    redrawCanvas();

    if (sub.logLine) addLog(sub.logLine, sub.logClass);

    i++;
    animTimer = setTimeout(next, 280);
  }

  next();
}

function clearAnimTimer() {
  if (animTimer) { clearTimeout(animTimer); animTimer = null; }
}

// ── Init ──────────────────────────────────────────────────────────────────
window.addEventListener('load', resetSim);
