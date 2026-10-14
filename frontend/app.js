const results = document.getElementById('results');
const fileSelect = document.getElementById('file-select');

async function api(route, body) {
  const response = await fetch('/api/' + route, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!response.ok) throw new Error(`server replied ${response.status}`);
  return response.json();
}

function formatDate(isoString) {
  return new Date(isoString).toLocaleString();
}

async function show(task) {
  results.innerHTML = '<p class="note">Loading…</p>';
  try {
    results.innerHTML = await task();
  } catch (err) {
    results.innerHTML = `<p class="error">Something went wrong: ${err.message}</p>`;
  }
}

document.getElementById('list-btn').addEventListener('click', () => show(async () => {
  const { files } = await api('listStories', {});
  let html = '<table><tr><th>File</th><th>Words</th><th>Last modified</th></tr>';
  for (const filename of files) {
    const { word_count } = await api('countWords', { filename });
    const { modified_date } = await api('getModifiedDate', { filename });
    html += `<tr><td>${filename}</td><td>${word_count}</td><td>${formatDate(modified_date)}</td></tr>`;
  }
  return html + '</table>';
}));

document.getElementById('count-btn').addEventListener('click', () => show(async () => {
  const { filename, word_count } = await api('countWords', { filename: fileSelect.value });
  return `<p>${filename} has <b>${word_count}</b> words.</p>`;
}));

document.getElementById('modified-btn').addEventListener('click', () => show(async () => {
  const { filename, modified_date } = await api('getModifiedDate', { filename: fileSelect.value });
  return `<p>${filename} was last modified <b>${formatDate(modified_date)}</b>.</p>`;
}));

document.getElementById('search-btn').addEventListener('click', () => show(async () => {
  const word = document.getElementById('search-box').value.trim();

  const { filename, matches } = await api('wordSearch', { filename: fileSelect.value, word });
  if (matches.length === 0) return `<p class="note">nothing found</p>`;

  const lines = matches.flatMap(m => m.lines);
  return `<p>"${word}" found in ${filename} on line${lines.length > 1 ? 's' : ''} <b>${lines.join(', ')}</b>.</p>`;
}));

api('listStories', {}).then(({ files }) => {
  fileSelect.innerHTML = files.map(f => `<option>${f}</option>`).join('');
});
