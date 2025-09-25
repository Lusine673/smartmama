<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>SmartMama — диет‑ассистент</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
  <script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js" integrity="sha512-YcsIPQqR9g0oSzmKM3v94aVn2Y1v3v6mQo6Cr6a2q9oW1mYF2fKm2U4GfA2m9n/FhNw3R3n8oYYb1J9rD14f0g==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
  <style>
    :root {
      --bg: #0f172a;      /* slate-900 */
      --card: #111827;    /* gray-900 */
      --ink: #e5e7eb;     /* gray-200 */
      --muted: #9ca3af;   /* gray-400 */
      --primary: #22c55e; /* green-500 */
      --warn: #f59e0b;    /* amber-500 */
      --error: #ef4444;   /* red-500 */
      --ok: #10b981;      /* emerald-500 */
      --border: #1f2937;  /* gray-800 */
    }
    * { box-sizing: border-box; }
    body {
      margin: 0; font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
      background: radial-gradient(1200px 600px at 80% -10%, rgba(34,197,94,.15), transparent),
                  radial-gradient(1000px 500px at 10% -10%, rgba(59,130,246,.12), transparent),
                  var(--bg);
      color: var(--ink);
      line-height: 1.5;
    }
    .container {
      max-width: 960px; margin: 24px auto; padding: 16px;
    }
    .title { font-size: 28px; font-weight: 700; margin: 8px 0 6px; }
    .subtitle { color: var(--muted); margin-bottom: 24px; }
    .card {
      background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0));
      border: 1px solid var(--border); border-radius: 14px; padding: 16px 16px;
      box-shadow: 0 8px 30px rgba(0,0,0,0.25);
      backdrop-filter: blur(6px);
    }
    .grid {
      display: grid; gap: 12px;
      grid-template-columns: repeat(2, minmax(0, 1fr));
    }
    @media (max-width: 720px) { .grid { grid-template-columns: 1fr; } }
    label { display:block; font-weight:600; margin-bottom:6px; }
    input {
      width:100%; padding:10px 12px; border-radius:10px; border:1px solid var(--border);
      background:#0b1220; color:var(--ink); outline:none;
    }
    input:focus { border-color:#334155; }
    button {
      border:0; border-radius:10px; padding:10px 14px; font-weight:600; cursor:pointer;
      background: var(--primary); color:#06210f;
    }
    button.secondary { background:#1f2937; color:var(--ink); }
    button:disabled { opacity:.5; cursor:not-allowed; }
    .row { display:flex; gap:10px; align-items:center; flex-wrap:wrap; }
    .section-title { font-size:18px; font-weight:600; margin: 20px 0 8px; }
    .msg { border-radius:10px; padding:10px 12px; border:1px solid var(--border); }
    .msg.info { background:#0b1220; }
    .msg.warn { background: rgba(245,158,11,.15); border-color: rgba(245,158,11,.35); }
    .msg.error{ background: rgba(239,68,68,.15); border-color: rgba(239,68,68,.35); }
    .msg.ok   { background: rgba(16,185,129,.15); border-color: rgba(16,185,129,.35); }
    .muted { color: var(--muted); font-size: 13px; }
    table { width:100%; border-collapse: collapse; }
    th, td { padding: 8px 10px; border-bottom: 1px solid var(--border); text-align:left; }
    th { color: #cbd5e1; font-weight:600; background: #0b1220; }
    .menu-card {
      white-space: pre-wrap; background:#0b1220; border:1px dashed #334155; border-radius:12px; padding:12px;
    }
    footer { color: var(--muted); font-size: 12px; margin-top: 24px; }
  </style>
</head>
<body>
  <div class="container">
    <div class="title">🤰 SmartMama: ваш личный диет‑ассистент при беременности</div>
    <div class="subtitle">Отслеживайте прибавку веса и получайте персонализированные рекомендации по питанию</div>

    <div class="card">
      <div class="section-title">📝 Введите ваши данные</div>
      <div class="grid">
        <div>
          <label>Вес до беременности (кг)</label>
          <input id="weight_before" type="number" min="30" max="150" step="0.1" value="60.0">
        </div>
        <div>
          <label>Рост (см)</label>
          <input id="height" type="number" min="120" max="220" step="1" value="165">
        </div>
        <div>
          <label>Текущий вес (кг)</label>
          <input id="current_weight" type="number" min="30" max="200" step="0.1" value="65.0">
        </div>
        <div>
          <label>Текущий срок (нед.)</label>
          <input id="gest_weeks" type="number" min="1" max="42" step="1" value="12">
        </div>
        <div>
          <label>Предыдущий вес (кг, опционально)</label>
