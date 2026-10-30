// DALAN router in JavaScript: a line-for-line port of the Python package (dalan/), driven by web/model.json.
// Usage:  const router = DALAN.create(model, kb);  router.route("Asa ko makapalit og bakuna?")
(function (root) {
  function create(M, kb) {
    const STOP = new Set(M.stop), EN_GUARD = new Set(M.en_guard), EN_VOCAB = new Set(M.en_vocab);
    const LEX = M.lexicon, CONTR = M.contractions, PREF = M.prefixes, SUFF = M.suffixes;
    const phonKey = w => w.replace(/e/g, "i").replace(/o/g, "u").replace(/-/g, "");
    const LEX_BY_KEY = {};
    for (const lemma of Object.keys(LEX)) { const k = phonKey(lemma); if (!(k in LEX_BY_KEY)) LEX_BY_KEY[k] = lemma; }
    const has = (o, k) => Object.prototype.hasOwnProperty.call(o, k);

    function fold(s) {
      s = s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "");
      s = s.replace(/(\w)['’]y\b/g, "$1 ang");
      s = s.replace(/[^a-z0-9\s-]/g, " ");
      s = s.replace(/([a-z])\1{2,}/g, "$1");
      return s.replace(/\s+/g, " ").trim();
    }
    function stemEn(t) {
      if (t.length > 4 && t.endsWith("es")) return t.slice(0, -2);
      if (t.length > 3 && t.endsWith("s")) return t.slice(0, -1);
      return t;
    }
    function lookup(tok) {
      if (has(LEX, tok)) return tok;
      const k = phonKey(tok);
      return has(LEX_BY_KEY, k) ? LEX_BY_KEY[k] : null;
    }
    function lemmatize(tok) {
      let hit = lookup(tok);
      if (hit) return hit;
      if (tok.length < 4) return null;
      if (tok.includes("-")) {
        const joined = tok.replace(/-/g, "");
        hit = lookup(joined) || lemmatize(joined);
        if (hit) return hit;
        const parts = tok.split("-").filter(Boolean);
        if (parts.length && parts[parts.length - 1] === parts[0]) return lemmatize(parts[0]);
        return parts.length ? lookup(parts[parts.length - 1]) : null;
      }
      const half = Math.floor(tok.length / 2);
      if (tok.length % 2 === 0 && tok.slice(0, half) === tok.slice(half)) { hit = lookup(tok.slice(0, half)); if (hit) return hit; }
      const cands = [tok];
      for (const p of PREF) if (tok.startsWith(p) && tok.length - p.length >= 3) cands.push(tok.slice(p.length));
      const more = [];
      for (const c of cands) for (const s of SUFF) if (c.endsWith(s) && c.length - s.length >= 3) more.push(c.slice(0, -s.length));
      cands.push(...more);
      const m = tok.match(/^([bcdfghklmnprstvwy])(um|in)([a-z]{3,})$/);
      if (m) cands.push(m[1] + m[3]);
      for (const c of cands.slice()) {
        if (c.length > 4 && c.slice(0, 2) === c.slice(2, 4)) cands.push(c.slice(2));
        else if (c.length > 3 && c[0] === c[1] && "aeiou".includes(c[0])) cands.push(c.slice(1));
      }
      for (const c of cands.slice(1)) { hit = lookup(c); if (hit) return hit; }
      return null;
    }
    function normalize(query) {
      const f = fold(query);
      const words = [], stack = f.split(" ").filter(Boolean).reverse();
      while (stack.length) {
        const w = stack.pop();
        const exp = has(CONTR, w) ? CONTR[w] : null;
        if (exp === null || exp === w) words.push(w);
        else if (exp) stack.push(...exp.split(" ").reverse());
      }
      const tokens = [], tags = [], glosses = [], weights = {};
      let nLocal = 0, nEn = 0, nOov = 0, nLex = 0;
      for (const w of words) {
        if (STOP.has(w)) continue;
        let base = stemEn(w);
        const inEn = EN_VOCAB.has(w) || EN_VOCAB.has(base);
        let lemma = null;
        if (!(EN_GUARD.has(w) && inEn)) lemma = lemmatize(w);
        if (!lemma && w.includes("-")) {
          const i = w.indexOf("-"), head = w.slice(0, i), rest = w.slice(i + 1);
          if (PREF.includes(head) && rest && lookup(rest) === null) {
            base = stemEn(rest); tokens.push(base); weights[base] = 1.0; tags.push([w, "mix"]); nLocal++; continue;
          }
        }
        if (lemma) {
          const [lang, gl] = LEX[lemma];
          tokens.push(w, lemma); weights[w] = 1.0; weights[lemma] = 1.0;
          for (const g of gl) for (let x of g.split(" ")) {
            if (STOP.has(x)) continue;
            x = stemEn(x); tokens.push(x); weights[x] = Math.max(weights[x] || 0, M.gamma);
          }
          glosses.push(...gl); tags.push([w, lang]); nLocal++; nLex++;
        } else {
          tokens.push(base); weights[base] = 1.0;
          if (w.includes("-")) for (const part of w.split("-")) if (part && !STOP.has(part)) { tokens.push(stemEn(part)); weights[stemEn(part)] = 1.0; }
          if (inEn) { tags.push([w, "en"]); nEn++; } else { tags.push([w, "unk"]); nOov++; }
        }
      }
      const n = Math.max(1, nLocal + nEn + nOov);
      return { folded: f, tokens, weights, tags, charText: f + (glosses.length ? " " + glosses.join(" ") : ""),
               csi: nLocal / Math.max(1, nLocal + nEn), oov: nOov / n, lexHit: nLex / n, nTokens: nLocal + nEn + nOov };
    }

    const docs = M.lex_docs.map(d => ({ title: new Set(d.title), kw: new Set(d.kw), q: new Set(d.q), phrases: d.phrases }));
    function lexScores(nq) {
      const qt = [...new Set(nq.tokens)], qn = " " + nq.folded + " ";
      return docs.map(d => {
        let s = 0;
        for (const t of qt) {
          const w = (has(M.lex_idf, t) ? M.lex_idf[t] : M.lex_default_idf) * (has(nq.weights, t) ? nq.weights[t] : 1.0);
          if (d.kw.has(t)) s += 3 * w; else if (d.title.has(t)) s += 2 * w; else if (d.q.has(t)) s += w;
        }
        for (const p of d.phrases) if (qn.includes(" " + p + " ")) s += 4;
        return s;
      });
    }
    function charGrams(text) {
      const g = new Map();
      for (let w of text.split(" ").filter(Boolean)) {
        if (STOP.has(w)) continue;
        w = "#" + w + "#";
        for (let n = 3; n <= 5; n++) for (let i = 0; i + n <= w.length; i++) { const k = w.slice(i, i + n); g.set(k, (g.get(k) || 0) + 1); }
      }
      return g;
    }
    function charScores(nq) {
      const v = {}; let norm = 0;
      for (const [g, c] of charGrams(nq.charText)) {
        const x = (1 + Math.log(c)) * (has(M.char_idf, g) ? M.char_idf[g] : 0);
        if (x > 0) { v[g] = x; norm += x * x; }
      }
      norm = Math.sqrt(norm) || 1;
      return M.char_vecs.map(d => { let s = 0; for (const g in v) if (has(d, g)) s += (v[g] / norm) * d[g]; return s; });
    }
    const argsortDesc = a => a.map((v, i) => [v, i]).sort((x, y) => y[0] - x[0] || x[1] - y[1]).map(p => p[1]);
    function ranks(s) { const r = new Array(s.length); argsortDesc(s).forEach((i, k) => { r[i] = k; }); return r; }
    const argmax = a => a.reduce((bi, v, i) => (v > a[bi] ? i : bi), 0);
    const top2 = a => { const s = a.slice().sort((x, y) => y - x); return [s[0], s[1]]; };

    function features(lex, ch, fused, nq) {
      const [l1, l2] = top2(lex), [c1, c2] = top2(ch), [f1, f2] = top2(fused);
      const topL = argmax(lex), topC = argmax(ch);
      const sat = l1 / (l1 + 5);
      const rankLinC = ch.filter(v => v > ch[topL]).length;
      return [sat, l1 > 0 ? (l1 - l2) / (l1 + 1e-6) : 0, c1, c1 - c2, topL === topC ? 1 : 0, (f1 - f2) / (f1 + 1e-9),
              nq.csi, nq.oov, Math.log1p(nq.nTokens), nq.lexHit, nq.csi * sat, nq.oov * c1, 1 / (1 + rankLinC)];
    }
    const entries = kb.entries.filter(e => e.id !== "fallback"), fallback = kb.entries.find(e => e.id === "fallback");
    const GATES = (M.gates || []).map(g => (g ? g : null));
    const byId = Object.fromEntries(entries.map(e => [e.id, e]));

    function route(query) {
      const t0 = (typeof performance !== "undefined" ? performance : Date).now();
      const nq = normalize(query);
      let lex = lexScores(nq), ch = charScores(nq);
      if (GATES.some(g => g)) {
        const words = new Set([...nq.folded.replace(/-/g, " ").split(" ").filter(Boolean), ...nq.tokens]);
        const closed = GATES.map(g => !!g && !g.some(c => words.has(c)));
        lex = lex.map((v, i) => (closed[i] ? 0 : v)); ch = ch.map((v, i) => (closed[i] ? 0 : v));
      }
      const rl = ranks(lex), rc = ranks(ch), lmax = Math.max(...lex);
      const fused = lex.map((v, i) => 1 / (10 + 1 + rl[i]) + 1 / (10 + 1 + rc[i]) + 1e-6 * v / (1 + lmax));
      const x = features(lex, ch, fused, nq);
      let z = M.cal.b;
      x.forEach((v, i) => { z += ((v - M.cal.mu[i]) / M.cal.sd[i]) * M.cal.w[i]; });
      const p = 1 / (1 + Math.exp(-z));
      const bucket = nq.csi >= 0.2 ? "cs" : "en";
      const [tSkip, tAbs0] = M.thresholds[bucket] || M.thresholds._global;
      const tAbs = Math.min(tAbs0, tSkip);
      const TOL = 1e-9;
      const action = p >= tSkip - TOL ? "skip" : p >= tAbs - TOL ? "generate" : "abstain";
      const order = argsortDesc(fused).slice(0, M.k_ctx).map(i => M.ids[i]);
      return { action, p, bucket, csi: nq.csi, oov: nq.oov, tags: nq.tags, ranked_ids: order,
               entry: action === "abstain" ? fallback : byId[order[0]], context: order.map(id => byId[id]),
               tau: [tSkip, tAbs], ms: (typeof performance !== "undefined" ? performance : Date).now() - t0 };
    }
    return { route, normalize };
  }
  const api = { create };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.DALAN = api;
})(typeof window !== "undefined" ? window : globalThis);
