# -*- coding: utf-8 -*-
"""
analysis_fig3.py

Reproduces the grid-cell statistical results of

  Tong et al., "Satellite mapping reveals complex patterns of intensively used
  croplands in the Western Sahel", Nature Food.

Written from the Methods section of the submitted manuscript. Input is
data/analysis_table.csv (117,006 grid cells of 1 x 1 km).

Requires: numpy, pandas, statsmodels, scikit-learn.
"""
import numpy as np, pandas as pd, warnings
import statsmodels.formula.api as smf
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import GroupKFold
warnings.filterwarnings('ignore')
rng = np.random.default_rng(20260101)

SPAT = 'lon_c + lat_c + I(lon_c**2) + I(lat_c**2) + I(lon_c*lat_c)'
z = lambda s: (s - s.mean()) / s.std()
hr = lambda t: print('\n' + t + '\n' + '-'*len(t))


def load(path='data/analysis_table.csv'):
    d = pd.read_csv(path)
    # Methods variable names -> columns of the analysis table
    d['cf']   = d['nci']         # cultivated fraction, 1 km sliding window, min-max normalised
    d['prod'] = d['nm1_cali']    # productivity normalised to 400 mm rainfall
    d['tree'] = d['cwc302_mea']  # tree cover of cropped fields, %
    d['soil'] = d['sqi']         # soil quality index
    d['rain'] = d['rf_mean']     # mean annual rainfall, mm (CHIRPS 1982-2020)
    d['pop']  = d['pop_sum']     # population per 1 km cell (WorldPop 2019)
    d['lon_c'] = d.lon - d.lon.mean()
    d['lat_c'] = d.lat - d.lat.mean()
    # right-skewed variables are log-transformed for the contrasts (Methods)
    d['l_prod'] = np.log(d['prod'])
    d['l_tree'] = np.log(d['tree'])
    d['l_soil'] = np.log(d['soil'])
    d['l_pop']  = np.log1p(d['pop'])   # log1p: 22 cells have zero population
    return d


def clustered(formula, data):
    """OLS with standard errors clustered on 0.5 degree blocks."""
    sub = data.dropna(subset=['block'])
    res = smf.ols(formula, data=sub).fit()
    keep = sub.index.isin(res.resid.index)
    return smf.ols(formula, data=sub).fit(
        cov_type='cluster', cov_kwds={'groups': sub.loc[keep, 'block'].values})


def main():
    d = load()
    hr('Study area and clustering')
    print(f'grid cells            {len(d):,}')
    print(d.ADMIN.value_counts().to_string())
    print(f'0.5 degree blocks     {d.block.nunique()}')

    # ---------------------------------------------------------------- deff
    hr('Design effect (clustered vs unclustered, on the cultivated fraction coefficient)')
    print(f'{"metric":22s} {"SE ratio":>9s} {"variance ratio":>15s}')
    for nm, col in [('cultivated fraction','cf'), ('productivity','l_prod'),
                    ('tree cover','l_tree'), ('soil quality','l_soil')]:
        s = d.dropna(subset=[col, 'cf'])
        m = smf.ols(f'{col} ~ cf + C(ADMIN) + {SPAT}', data=s)
        a, b = m.fit(), m.fit(cov_type='cluster', cov_kwds={'groups': s.block.values})
        r = b.bse['cf'] / a.bse['cf']
        print(f'{nm:22s} {r:9.1f} {r**2:15.1f}')

    # ------------------------------------------------- Fig 3a: controls
    hr('Fig. 3a  Controls on cultivated fraction')
    dz = d.dropna(subset=['cf','rain','soil','tree','pop','prod']).copy()
    # Methods: rainfall, soil quality index, tree cover, LOG population density,
    # productivity; response and all five controls standardised.
    for c in ['cf','rain','soil','tree','prod','l_pop']:
        dz['z_'+c] = z(dz[c])
    CTRL = 'z_rain + z_soil + z_tree + z_l_pop + z_prod'
    full = smf.ols(f'z_cf ~ {CTRL} + C(ADMIN) + {SPAT}', data=dz).fit()
    ctrl = smf.ols(f'z_cf ~ {CTRL}', data=dz).fit()
    geo  = smf.ols(f'z_cf ~ C(ADMIN) + {SPAT}', data=dz).fit()
    print(f'R2 full model          {full.rsquared:.3f}')
    print(f'R2 controls only       {ctrl.rsquared:.3f}')
    print(f'R2 geography only      {geo.rsquared:.3f}')
    print(f'full minus geography   {100*(full.rsquared-geo.rsquared):.0f} percentage points')
    fc = smf.ols(f'z_cf ~ {CTRL} + C(ADMIN) + {SPAT}', data=dz).fit(
            cov_type='cluster', cov_kwds={'groups': dz.block.values})
    print(f'\n{"control":12s} {"beta":>8s} {"95% CI":>18s} {"P":>10s} {"unique R2":>10s}')
    for v in ['z_rain','z_soil','z_tree','z_l_pop','z_prod']:
        rest = ' + '.join(x for x in CTRL.split(' + ') if x != v)
        r2d = smf.ols(f'z_cf ~ {rest} + C(ADMIN) + {SPAT}', data=dz).fit().rsquared
        lo, hi = fc.conf_int().loc[v]
        print(f'{v[2:]:12s} {fc.params[v]:+8.3f} [{lo:+.3f}, {hi:+.3f}] '
              f'{fc.pvalues[v]:10.2g} {full.rsquared-r2d:10.4f}')

    # ------------------------------------------- spatial block cross-validation
    hr('Spatial block cross-validation (whole 0.5 degree blocks held out)')
    X = pd.get_dummies(dz[['rain','soil','tree','l_pop','prod','ADMIN']],
                       columns=['ADMIN'], drop_first=True).astype(float).values
    y = dz['cf'].values; g = dz['block'].values
    for name, mk in [('linear', lambda: LinearRegression()),
                     ('gradient boosting', lambda: HistGradientBoostingRegressor(
                         max_iter=300, learning_rate=0.1, max_depth=None, random_state=0))]:
        sc = []
        for tr, te in GroupKFold(n_splits=5).split(X, y, groups=g):
            m = mk().fit(X[tr], y[tr])
            p = m.predict(X[te])
            sc.append(1 - ((y[te]-p)**2).sum() / ((y[te]-y[te].mean())**2).sum())
        print(f'{name:20s} R2 = {np.mean(sc):.2f} +/- {np.std(sc):.2f}')

    # ------------------------------------------------ cultivated fraction classes
    hr('Fig. 3e  Contrasts between cultivated fraction classes')
    dc = d.dropna(subset=['cf']).copy()
    edges = np.linspace(dc.cf.min(), dc.cf.max(), 6)
    dc['cfclass'] = pd.cut(dc.cf, edges, include_lowest=True, labels=[1,2,3,4,5])
    print('class sizes:', dc.cfclass.value_counts().sort_index().tolist())
    print(f'\n{"outcome":16s} {"class 5 vs class 1":>20s} {"95% CI":>20s} {"P":>10s}')
    for nm, col in [('productivity','l_prod'), ('tree cover','l_tree'),
                    ('soil quality','l_soil'), ('population','l_pop')]:
        s = dc.dropna(subset=[col])
        m = smf.ols(f'{col} ~ C(cfclass) + C(ADMIN) + {SPAT}', data=s).fit(
                cov_type='cluster', cov_kwds={'groups': s.block.values})
        k = 'C(cfclass)[T.5]'; b, se = m.params[k], m.bse[k]
        pct = lambda x: 100*(np.exp(x)-1)
        print(f'{nm:16s} {pct(b):+19.1f}% [{pct(b-1.96*se):+6.1f}, {pct(b+1.96*se):+6.1f}] '
              f'{m.pvalues[k]:10.2g}')

    # ----------------------------------------------------- tree interaction
    hr('Does tree cover offset the productivity cost of intensification?')
    di = d.dropna(subset=['l_prod','cf','tree','rain','pop']).copy()
    it = smf.ols(f'l_prod ~ cf * tree + rain + l_pop + C(ADMIN) + {SPAT}', data=di).fit(
            cov_type='cluster', cov_kwds={'groups': di.block.values})
    print(f'interaction coefficient {it.params["cf:tree"]:+.5f}   P = {it.pvalues["cf:tree"]:.4f}')
    sd = di.tree.std(); mn = di.tree.mean()
    for lab, tv in [('tree cover 1 SD below mean', mn-sd), ('tree cover 1 SD above mean', mn+sd)]:
        slope = it.params['cf'] + it.params['cf:tree']*tv
        print(f'  {lab:30s} productivity change per +10 pp cultivated fraction: '
              f'{100*(np.exp(slope*0.10)-1):+.1f}%')

    # --------------------------------------------- archetype shares + bootstrap
    hr('Fig. 2c  Archetype shares, with block bootstrap confidence intervals')
    da = d.dropna(subset=['arch']).copy()
    blocks = da.block.unique()
    order = sorted(da.arch.unique())
    print(f'{"country":10s} ' + ' '.join(f'{a:>14s}' for a in order))
    for ctry, g in da.groupby('ADMIN'):
        obs = g.arch.value_counts(normalize=True).reindex(order).fillna(0).values*100
        gb = g.block.unique()
        av = np.asarray(g.arch.astype(str))
        gidx = {b: np.where(np.asarray(g.block.astype(str)) == str(b))[0] for b in gb}
        oi = {a: i for i, a in enumerate(order)}
        codes = np.array([oi[a] for a in av])
        boot = np.empty((1000, len(order)))
        for k in range(1000):
            pick = rng.choice(gb, size=len(gb), replace=True)
            rows = np.concatenate([gidx[b] for b in pick])
            boot[k] = np.bincount(codes[rows], minlength=len(order)) / len(rows) * 100
        lo, hi = np.percentile(boot, [2.5, 97.5], axis=0)
        print(f'{ctry:10s} ' + ' '.join(f'{o:5.1f} [{l:4.1f},{h:4.1f}]'
              for o, l, h in zip(obs, lo, hi)))
    intens = da.arch.str.startswith('hh')
    print('\nintensive archetypes (high cultivated fraction and high productivity), % of cells:')
    print((100*intens.groupby(da.ADMIN).mean()).round(1).to_string())

    # ------------------------------------------ permutation test on composition
    hr('Does archetype composition differ between countries? (block permutation)')
    bl = da.groupby('block').ADMIN.agg(lambda s: s.mode().iat[0])
    tab = pd.crosstab(da.ADMIN, da.arch, normalize='index')
    obs = np.abs(tab.values - tab.values.mean(0)).sum()
    null = []
    for _ in range(500):
        perm = pd.Series(rng.permutation(bl.values), index=bl.index)
        lab = da.block.map(perm)
        t = pd.crosstab(lab, da.arch, normalize='index')
        null.append(np.abs(t.values - t.values.mean(0)).sum())
    p = (1 + sum(n >= obs for n in null)) / (1 + len(null))
    print(f'observed composition distance {obs:.4f}   permutation P = {p:.4f}  (500 permutations)')

    hr('Done')


if __name__ == '__main__':
    main()
