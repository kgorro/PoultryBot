"""DALAN: Dual-channel Agreement with Lexicon-Augmented Normalization.

A router for retrieval-first assistants that decides, per query, whether to
  SKIP      answer directly from the verified knowledge base (no LLM call),
  GENERATE  call a small local LLM with the fused top-k entries as context, or
  ABSTAIN   decline and guide the user,
while staying reliable on code-switched, low-resource queries (Cebuano, Tagalog, English mixes).

Pipeline:  CSN (normalize.py) -> lexical + character channels (channels.py) -> RRF fusion
           -> calibrated confidence p (calibrate.py) -> language-conditioned risk-controlled thresholds.
"""
import time

import numpy as np

from .calibrate import BucketThresholds, LogisticCalibrator, features
from .channels import CharChannel, LexicalChannel, fuse
from .normalize import Normalizer, kb_vocab

SKIP, GENERATE, ABSTAIN = "skip", "generate", "abstain"
TOL = 1e-9  # thresholds sit exactly on calibration scores; absorb float round-off across implementations


def bucket_of(nq, cs_cut=0.2):
    return "cs" if nq.csi >= cs_cut else "en"


class DALANRouter:
    def __init__(self, kb, eps=0.05, delta=0.05, k_ctx=3, use_csn=True, use_char=True,
                 per_language=True, feature_mask=None, rrf_weights=(1.0, 1.0)):
        self.kb = kb
        self.entries = [e for e in kb["entries"] if e["id"] != "fallback"]
        self.fallback = next(e for e in kb["entries"] if e["id"] == "fallback")
        self.norm = Normalizer(kb_vocab(kb), use_lexicon=use_csn, use_affix=use_csn)
        core = [not e.get("scope") for e in self.entries]
        self.lex = LexicalChannel(self.entries, core)
        self.char = CharChannel(self.entries, core) if use_char else None
        self.k_ctx = k_ctx
        self.per_language = per_language
        self.feature_mask = feature_mask
        self.rrf_weights = rrf_weights
        self.cal = LogisticCalibrator()
        self.th = BucketThresholds(eps=eps, delta=delta)
        self.ids = [e["id"] for e in self.entries]
        # Scope gates: entries with a 'scope' cue list are ranked only when the query contains a cue word
        self.gates = [set(e["scope"]) if e.get("scope") else None for e in self.entries]
        self.gated = np.array([g is not None for g in self.gates])

    # ---------------------------------------------------------------- scoring
    def channel_scores(self, nq):
        """Lexical and character scores, with scope-gated entries zeroed when the query has none of their cues."""
        lex = self.lex.scores(nq)
        char = self.char.scores(nq) if self.char else np.zeros_like(lex)
        if self.gated.any():
            words = set(nq.folded.replace("-", " ").split()) | set(nq.tokens)
            closed = np.array([g is not None and not (g & words) for g in self.gates])
            lex, char = np.where(closed, 0.0, lex), np.where(closed, 0.0, char)
        return lex, char

    def _analyze(self, query):
        nq = self.norm(query)
        lex, char = self.channel_scores(nq)
        fused = fuse([lex, char], self.rrf_weights) if self.char else lex.copy()
        # Tie-break fused ranks by lexical score so strong lexical evidence wins equal RRF ranks
        fused = fused + 1e-6 * lex / (1 + lex.max())
        x = features(lex, char, fused, nq)
        if self.feature_mask is not None:
            x = x * self.feature_mask
        order = np.argsort(-fused, kind="stable")
        return nq, x, order

    # ---------------------------------------------------------------- training
    def fit(self, queries):
        """queries: list of dicts with 'q' and 'gold' (list of entry ids; ['OOD'] for out-of-domain)."""
        X, y, in_ctx, buckets = [], [], [], []
        for item in queries:
            nq, x, order = self._analyze(item["q"])
            gold = set(item["gold"])
            top_ids = [self.ids[i] for i in order[: self.k_ctx]]
            X.append(x)
            y.append(top_ids[0] in gold)
            in_ctx.append(bool(gold & set(top_ids)))
            buckets.append(bucket_of(nq) if self.per_language else "all")
        X = np.array(X)
        self.cal.fit(X, y)
        p = self.cal.predict(X)
        self.th.fit(p, y, in_ctx, buckets)
        return self

    # ---------------------------------------------------------------- inference
    def route(self, query):
        t0 = time.perf_counter()
        nq, x, order = self._analyze(query)
        p = float(self.cal.predict(x)[0])
        b = bucket_of(nq) if self.per_language else "all"
        tau_skip, tau_abs = self.th.get(b)
        if p >= tau_skip - TOL:
            action = SKIP
        elif p >= tau_abs - TOL:
            action = GENERATE
        else:
            action = ABSTAIN
        top = [self.entries[i] for i in order[: self.k_ctx]]
        return dict(action=action, p=p, bucket=b, csi=nq.csi, oov=nq.oov,
                    entry=top[0] if action != ABSTAIN else self.fallback,
                    context=top, ranked_ids=[e["id"] for e in top],
                    tau=(tau_skip, tau_abs), ms=(time.perf_counter() - t0) * 1000)
