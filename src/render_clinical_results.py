"""Generate manuscript table and plot only from the frozen native receipt."""
import json
import re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
d = json.loads((ROOT/'analysis/clinical-family/receipt.json').read_text())
rows = []
covered = omitted = 0
for s in d['scenarios']:
    c = sum(x['status'] == 'covered' for x in s['slices'])
    o = sum(x['status'] == 'accepted_candidate_omission' for x in s['slices'])
    covered += c
    omitted += o
    label = s['scenario'].removeprefix('clinical_').replace('_', r'\_')
    control = s['scenario'] == 'clinical_remove_auditor'
    rows.append(f"{label} & {s['passed']}/{s['original_checks']} & " + ('-- & -- & Reject' if control else f"{c} & {o} & Pass") + r' \\')
table = r'''\begin{table}[t]
\centering\small\setlength{\tabcolsep}{3pt}
\caption{Native clinical-family results. C: covered probes; O: omitted probes. Aug.: augmented candidate satisfies original plan. Removal is a negative control.}
\label{tab:results}
\begin{tabular}{lrrrr}
\toprule Scenario & Checks & C & O & Aug.\\\midrule
''' + '\n'.join(rows) + r'''
\bottomrule\end{tabular}
\end{table}'''
figure = r'''\begin{figure}[t]
\centering
\begin{tikzpicture}
\begin{axis}[ybar,width=\columnwidth,height=4cm,ymin=0,ymax=40,
symbolic x coords={Covered,Omitted},xtick=data,ylabel={Positive probes},
nodes near coords,bar width=22pt,enlarge x limits=.7]
\addplot coordinates {''' + f'(Covered,{covered}) (Omitted,{omitted})' + r'''};
\end{axis}\end{tikzpicture}
\caption{Auditor probe coverage in ten related exception-retaining scenarios. Counts are not a benchmark-wide prevalence estimate.}
\Description{Bar chart showing six covered and thirty-four omitted positive auditor probes.}
\label{fig:counts}
\end{figure}'''
p = ROOT/'paper/main.tex'
text = p.read_text(encoding='utf-8')
for kind, body in [('TABLE', table), ('FIGURE', figure)]:
    pattern = f'% GENERATED_{kind}_BEGIN.*?% GENERATED_{kind}_END'
    assert len(re.findall(pattern, text, re.S)) == 1
    text = re.sub(pattern, lambda _: f'% GENERATED_{kind}_BEGIN\n{body}\n% GENERATED_{kind}_END', text, flags=re.S)
p.write_text(text, encoding='utf-8')
print('Generated 11 table rows and 2 plot coordinates from receipt')
