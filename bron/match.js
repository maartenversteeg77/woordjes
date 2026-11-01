// Antwoordcontrole. Wordt zowel in de app als in de test gebruikt.
function strip(s) { return s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase(); }
function norm(s) {
  return strip(s).replace(/[()]/g, '').replace(/[.,;:!?'"“”‘’]/g, ' ').replace(/\s+/g, ' ').trim();
}
function splitTop(s) {
  var out = [], depth = 0, cur = '';
  for (var i = 0; i < s.length; i++) {
    var ch = s[i];
    if (ch === '(') depth++;
    if (ch === ')') depth = Math.max(0, depth - 1);
    if ((ch === '/' || ch === '|') && depth === 0) { out.push(cur); cur = ''; } else cur += ch;
  }
  out.push(cur);
  return out;
}
function expandParens(part) {
  var results = [part];
  var re = /\(([^)]*)\)/;
  for (var n = 0; n < 4; n++) {
    var next = [];
    var any = false;
    for (var r = 0; r < results.length; r++) {
      var m = re.exec(results[r]);
      if (!m) { next.push(results[r]); continue; }
      any = true;
      var alts = [''].concat(m[1].split('/').map(function (x) { return x.trim(); }));
      for (var a = 0; a < alts.length; a++) {
        next.push(results[r].slice(0, m.index) + alts[a] + results[r].slice(m.index + m[0].length));
      }
    }
    results = next.slice(0, 64);
    if (!any) break;
  }
  return results;
}
function splitSpaced(s) {
  // splitst op "|" en op " / " (met spaties) buiten haakjes
  var out = [], depth = 0, cur = '';
  for (var i = 0; i < s.length; i++) {
    var ch = s[i];
    if (ch === '(') depth++;
    if (ch === ')') depth = Math.max(0, depth - 1);
    if (depth === 0 && ch === '|') { out.push(cur); cur = ''; continue; }
    if (depth === 0 && ch === '/' && s[i - 1] === ' ' && s[i + 1] === ' ') { out.push(cur); cur = ''; continue; }
    cur += ch;
  }
  out.push(cur);
  return out;
}
function splitBare(p) {
  // "(aan) hem/haar" -> "(aan) hem", "(aan) haar"
  var pieces = splitTop(p);
  if (pieces.length < 2) return [p];
  var m = /^\s*(\([^)]*\))\s*/.exec(pieces[0]);
  var prefix = m ? m[0] : '';
  return pieces.map(function (x, i) { return i === 0 || !prefix ? x : prefix + x.trim(); });
}
function variantsOf(nl) {
  var s = nl.replace(/\(\s*\d\.\)/g, '|').replace(/\(\s*\+[^)]*\)/g, '').replace(/\.{3}|…/g, ' ');
  s = s.replace(/(^|\|)\s*hij\s*\/\s*zij\s*\/\s*het\s+/g, '$1(hij/zij/het) ');
  var parts = [];
  splitSpaced(s).forEach(function (p) { splitBare(p).forEach(function (q) { parts.push(q); }); });
  parts.push(s.replace(/\|/g, ' '));
  var set = {};
  parts.forEach(function (p) {
    expandParens(p).forEach(function (v) {
      var n = norm(v);
      if (!n) return;
      set[n] = true;
      if (/^perf /.test(n)) set['perfectum ' + n.slice(5)] = true;
    });
  });
  return Object.keys(set);
}
function lev(a, b) {
  var m = a.length, n = b.length, d = [], i, j;
  for (i = 0; i <= m; i++) { d[i] = [i]; }
  for (j = 1; j <= n; j++) d[0][j] = j;
  for (i = 1; i <= m; i++) for (j = 1; j <= n; j++) {
    var c = a[i - 1] === b[j - 1] ? 0 : 1;
    d[i][j] = Math.min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + c);
    if (i > 1 && j > 1 && a[i - 1] === b[j - 2] && a[i - 2] === b[j - 1]) d[i][j] = Math.min(d[i][j], d[i - 2][j - 2] + 1);
  }
  return d[m][n];
}
function tolerance(len) { return len <= 3 ? 0 : len <= 8 ? 1 : 2; }
// vars: varianten van dit woord; others: set van varianten die bij een ander woord horen
function judge(input, vars, others) {
  var n = norm(input);
  if (!n) return { r: 'wrong' };
  if (vars.indexOf(n) >= 0) return { r: 'exact' };
  // meerdere vertalingen achter elkaar ("hoort, luistert" / "zoeken en vragen"): goed als elk deel goed is
  var pieces = input.split(/\s*[\/,;]\s*|\s+of\s+|\s+en\s+/).map(norm).filter(Boolean);
  if (pieces.length > 1 && pieces.every(function (x) { return vars.indexOf(x) >= 0; })) return { r: 'exact' };
  if (others && others[n]) return { r: 'wrong' };
  var best = null, bd = 99;
  vars.forEach(function (v) {
    var d = lev(n, v);
    if (d < bd) { bd = d; best = v; }
  });
  if (best !== null && bd <= tolerance(best.length)) return { r: 'spelling', best: best };
  return { r: 'wrong' };
}
if (typeof module !== 'undefined') module.exports = { norm: norm, variantsOf: variantsOf, judge: judge, lev: lev };
