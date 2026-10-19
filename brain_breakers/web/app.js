const translations = {
  fr: {
    eyebrow: 'SUPPRIMER · CORRIGER · ISOLER',
    title: 'Une source retirée doit vraiment disparaître.',
    lede: 'Changez la mémoire, rejouez la recherche et vérifiez la réponse autant que ses sources. Une réponse identique peut cacher un index périmé — ou rester correcte grâce à une autre source.',
    experiment: 'Rejouer les mutations',
    explain:
      'Quatre cas synthétiques. Des fautes sont injectées dans la synchronisation du client, puis retirées. Les moteurs de base de données sont réels ; aucun bug de leur code n’est prétendu.',
    run: 'Exécuter SQLite FTS5 ici',
    published: 'Voir la preuve publiée sur 3 moteurs',
    filter: 'Cas affichés',
    all: 'Tous les cas',
    'deleted-source-resurrects': 'Source supprimée retrouvée',
    'correction-keeps-stale-index': 'Correction absente de l’index',
    'tenant-canary-leak': 'Fuite entre espaces',
    'same-answer-different-support': 'Même réponse, autres preuves',
    noNetwork:
      'Rejeu local sans modèle, clé ni téléchargement d’embeddings. Les canaris sont synthétiques.',
    results: 'Fautes et corrections comparées',
    trials: 'cas × moteurs',
    detected: 'fautes injectées détectées',
    repaired: 'intégrations corrigées valides',
    download: 'Exporter les preuves JSON',
    limits:
      'Tests d’intégration bornés, pas un classement de qualité mémoire. SQLite FTS5, Chroma et Qdrant local sont exécutés avec des faits explicites et des vecteurs déterministes. Aucun agent GBrain/Hindsight ni oubli légal complet n’est validé. Les contrôles défectueux sont créés par ce dépôt.',
    live: 'EXÉCUTION LOCALE',
    snapshot: 'PREUVE ENREGISTRÉE · 3 MOTEURS',
    fault: 'Client défectueux',
    repair: 'Client corrigé',
    unknown: 'Inconnu',
    answer: 'Réponse',
    sources: 'Sources sélectionnées',
    retrieved: 'Documents retrouvés',
    failures: 'Écarts vérifiés',
    passed: 'Conforme à l’oracle',
    baseline: 'État initial valide',
    reduction: 'Réducteur de cas',
    removed: 'Documents retirés',
    remaining: 'Documents conservés',
    same: 'Réponse inchangée, source indépendante conservée',
    stale_retrieval: 'Document supprimé ou ancienne révision encore retrouvé',
    scope_leak: 'Document d’un autre espace retrouvé',
    answer_mismatch: 'Réponse différente du registre courant',
    invalid_support: 'Sources non conformes au registre courant',
    error: 'Exécution impossible.',
    ready: 'Résultats disponibles.',
  },
  en: {
    eyebrow: 'DELETE · CORRECT · ISOLATE',
    title: 'A removed source should actually disappear.',
    lede: 'Change memory, replay retrieval and check both the answer and its sources. The same answer can hide a stale index — or remain correct through independent support.',
    experiment: 'Replay mutations',
    explain:
      'Four synthetic cases. Faults are injected into client synchronization, then removed. The database engines are real; no bug in their code is claimed.',
    run: 'Run SQLite FTS5 here',
    published: 'View published three-engine proof',
    filter: 'Displayed cases',
    all: 'All cases',
    'deleted-source-resurrects': 'Deleted source retrieved',
    'correction-keeps-stale-index': 'Correction missing from index',
    'tenant-canary-leak': 'Cross-tenant leak',
    'same-answer-different-support': 'Same answer, different support',
    noNetwork: 'Local replay without model, key or embedding downloads. Canaries are synthetic.',
    results: 'Compare faults and repairs',
    trials: 'cases × engines',
    detected: 'injected faults detected',
    repaired: 'repaired integrations valid',
    download: 'Export JSON evidence',
    limits:
      'Bounded integration trials, not a memory quality leaderboard. SQLite FTS5, Chroma and local Qdrant run with explicit facts and deterministic vectors. No GBrain/Hindsight agent or complete legal erasure is validated. Broken controls are created by this repository.',
    live: 'LOCAL EXECUTION',
    snapshot: 'RECORDED PROOF · 3 ENGINES',
    fault: 'Broken client',
    repair: 'Repaired client',
    unknown: 'Unknown',
    answer: 'Answer',
    sources: 'Selected sources',
    retrieved: 'Retrieved documents',
    failures: 'Verified failures',
    passed: 'Matches oracle',
    baseline: 'Initial state valid',
    reduction: 'Case reducer',
    removed: 'Documents removed',
    remaining: 'Documents retained',
    same: 'Answer unchanged, independent support retained',
    stale_retrieval: 'Deleted document or stale revision still retrieved',
    scope_leak: 'Another tenant’s document retrieved',
    answer_mismatch: 'Answer differs from current ledger',
    invalid_support: 'Support differs from current ledger',
    error: 'Execution failed.',
    ready: 'Results available.',
  },
  es: {
    eyebrow: 'BORRAR · CORREGIR · AISLAR',
    title: 'Una fuente retirada debe desaparecer de verdad.',
    lede: 'Cambie la memoria, repita la búsqueda y compruebe respuesta y fuentes. La misma respuesta puede ocultar un índice obsoleto o seguir siendo correcta gracias a otra fuente.',
    experiment: 'Repetir mutaciones',
    explain:
      'Cuatro casos sintéticos. Se inyectan fallos en la sincronización del cliente y luego se retiran. Los motores son reales; no se atribuye ningún fallo a su código.',
    run: 'Ejecutar SQLite FTS5 aquí',
    published: 'Ver prueba publicada en 3 motores',
    filter: 'Casos mostrados',
    all: 'Todos los casos',
    'deleted-source-resurrects': 'Fuente eliminada recuperada',
    'correction-keeps-stale-index': 'Corrección ausente del índice',
    'tenant-canary-leak': 'Fuga entre espacios',
    'same-answer-different-support': 'Misma respuesta, otras pruebas',
    noNetwork:
      'Reproducción local sin modelo, clave ni descarga de embeddings. Canarios sintéticos.',
    results: 'Comparar fallos y correcciones',
    trials: 'casos × motores',
    detected: 'fallos inyectados detectados',
    repaired: 'integraciones corregidas válidas',
    download: 'Exportar pruebas JSON',
    limits:
      'Pruebas de integración acotadas, no clasificación de calidad de memoria. SQLite FTS5, Chroma y Qdrant local usan hechos explícitos y vectores deterministas. Sin agente GBrain/Hindsight ni borrado legal completo validado. Este repositorio crea los controles defectuosos.',
    live: 'EJECUCIÓN LOCAL',
    snapshot: 'PRUEBA GUARDADA · 3 MOTORES',
    fault: 'Cliente defectuoso',
    repair: 'Cliente corregido',
    unknown: 'Desconocido',
    answer: 'Respuesta',
    sources: 'Fuentes seleccionadas',
    retrieved: 'Documentos recuperados',
    failures: 'Diferencias verificadas',
    passed: 'Conforme al oráculo',
    baseline: 'Estado inicial válido',
    reduction: 'Reductor de casos',
    removed: 'Documentos retirados',
    remaining: 'Documentos conservados',
    same: 'Respuesta idéntica, fuente independiente conservada',
    stale_retrieval: 'Documento eliminado o revisión anterior recuperado',
    scope_leak: 'Documento de otro espacio recuperado',
    answer_mismatch: 'Respuesta diferente del registro actual',
    invalid_support: 'Fuentes no conformes al registro actual',
    error: 'Ejecución fallida.',
    ready: 'Resultados disponibles.',
  },
};
const lang = new URLSearchParams(location.search).get('lang') || 'en',
  t = translations[lang] || translations.en;
document.documentElement.lang = translations[lang] ? lang : 'en';
document.querySelectorAll('[data-i18n]').forEach((e) => (e.textContent = t[e.dataset.i18n]));
const $ = (id) => document.getElementById(id);
let evidence,
  mode = 'snapshot';
function el(tag, text, cls) {
  const node = document.createElement(tag);
  node.textContent = text;
  if (cls) node.className = cls;
  return node;
}
function render() {
  $('trials').textContent = evidence.paired_trials;
  $('detected').textContent = evidence.injected_detected;
  $('repaired').textContent = evidence.repaired_passed;
  $('mode').textContent = t[mode];
  $('results').replaceChildren();
  for (const row of evidence.trials) {
    if ($('filter').value !== 'all' && $('filter').value !== row.case_id) continue;
    const card = el('section', '', 'trial');
    card.dataset.case = row.case_id;
    card.append(
      el('h3', t[row.case_id]),
      el('p', `${row.backend} · ${row.repaired.backend_version}`, 'tag'),
    );
    const pair = el('div', '', 'pair');
    for (const [key, title] of [
      ['injected', 'fault'],
      ['repaired', 'repair'],
    ]) {
      const run = row[key],
        panel = el('div', '', `evidence ${run.passed ? 'pass' : 'fail'}`),
        final = run.final;
      panel.append(
        el('h4', t[title]),
        el('p', `${t.answer}: ${final.answer.value ?? t.unknown}`),
        el('p', `${t.sources}: ${final.answer.source_ids.join(', ') || '—'}`, 'hint'),
        el('p', `${t.baseline}: ${run.initial_passed ? '✓' : '×'}`, 'hint'),
      );
      for (const failure of final.failures) panel.append(el('p', t[failure], 'trace'));
      if (run.passed) panel.append(el('p', t.passed, 'trace'));
      if (run.redundant_support_preserved) panel.append(el('p', t.same, 'trace'));
      const details = el('details', '');
      details.append(
        el('summary', t.retrieved),
        el('pre', JSON.stringify(final.retrieved, null, 2)),
      );
      panel.append(details);
      pair.append(panel);
    }
    card.append(pair);
    if (row.reduction) {
      const details = el('details', '');
      details.append(
        el('summary', t.reduction),
        el('p', `${t.removed}: ${row.reduction.removed.join(', ') || '—'}`),
        el('p', `${t.remaining}: ${row.reduction.case.documents.map((d) => d.id).join(', ')}`),
        el('pre', JSON.stringify(row.reduction.case, null, 2)),
      );
      card.append(details);
    }
    $('results').append(card);
  }
  $('status').textContent = t.ready;
}
$('filter').onchange = render;
$('run').onclick = async () => {
  try {
    $('run').disabled = true;
    const response = await fetch('/api/run', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: '{}',
    });
    if (!response.ok) throw Error();
    evidence = await response.json();
    mode = 'live';
    render();
  } catch {
    $('status').textContent = t.error;
  } finally {
    $('run').disabled = false;
  }
};
$('published').onclick = async () => {
  try {
    const response = await fetch('/api/published-evidence');
    if (!response.ok) throw Error();
    evidence = await response.json();
    mode = 'snapshot';
    render();
  } catch {
    $('status').textContent = t.error;
  }
};
$('download').onclick = () => {
  if (!evidence) return;
  const url = URL.createObjectURL(
      new Blob([JSON.stringify(evidence, null, 2)], { type: 'application/json' }),
    ),
    a = document.createElement('a');
  a.href = url;
  a.download = 'brain-breakers-evidence.json';
  a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
};
await $('published').onclick();
