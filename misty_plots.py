from __future__ import print_function
import numpy as np
from scipy import stats

from astropy.table import Table
from astropy.io import ascii

import matplotlib as mpl
import seaborn as sns
sns.set_style("whitegrid", {'axes.grid' : False})
mpl.rcParams['font.family'] = 'stixgeneral'
mpl.rcParams['font.size'] = 16.
import matplotlib.pyplot as plt


def make_misty_plots():
    # for now, be lazy and hardcode the paths to the files
    nat = Table.read('/Users/molly/Dropbox/foggie-collab/plots_halo_008508/nref11n/natural/spectra/misty_v5_rsp.dat', format='ascii.fixed_width')
    ref = Table.read('/Users/molly/Dropbox/foggie-collab/plots_halo_008508/nref11n/nref11n_nref10f_refine200kpc/spectra/misty_v5_rsp.dat', format='ascii.fixed_width')
    hires = Table.read('/Users/molly/Dropbox/foggie-collab/plots_halo_008508/nref11n/nref11f_refine200kpc/spectra/misty_v5_rsp.dat', format='ascii.fixed_width')
    kodiaq = Table.read('/Users/molly/Dropbox/kodiaq/kodiaq_spectacle_all.dat', format='ascii.fixed_width')
    print(len(nat), len(ref), len(hires))

    ref_color = 'darkorange' ###  '#4575b4' # purple
    nat_color = '#4daf4a' # green

    nat_p = nat.to_pandas()
    ref_p = ref.to_pandas()
    hires_p = hires.to_pandas()
    kod_p = kodiaq.to_pandas()

    idn = [nat['Si_II_col'] > 12]
    idr = [ref['Si_II_col'] > 12]
    idh = [hires['Si_II_col'] > 12]
    nat_si2 = nat[idn].to_pandas()
    ref_si2 = ref[idr].to_pandas()
    hires_si2 = hires[idh].to_pandas()

    idn = [nat['O_VI_col'] > 13] ## 11.2
    idr = [ref['O_VI_col'] > 13] ## 11.2
    idh = [hires['O_VI_col'] > 13]
    nat_o6 = nat[idn].to_pandas()
    ref_o6 = ref[idr].to_pandas()
    hires_o6 = hires[idh].to_pandas()


    fig = plt.figure(figsize=(9,7))
    ax = fig.add_subplot(111)
    sns.swarmplot(x="impact", y="Si_II_Nmin", data=nat_p, color=nat_color,alpha=0.7,orient='h')
    sns.swarmplot(x="impact", y="Si_II_Nmin", data=ref_p, color=ref_color,alpha=0.7,orient='h')
    # ax.scatter(nat['impact'], nat['Si_II_Nmin'], marker='D', color=nat_color,label='natural')
    # ax.scatter(ref['impact'], ref['Si_II_Nmin'], color=ref_color, label='refined')
    #ax.plot([10,45],[10,1],color=nat_color)
    #ax.plot([12,45],[17,4],color=ref_color)
    #plt.legend(loc='upper right')
    plt.ylim(-0.5,14.5)
    plt.xlabel('impact parameter [kpc]')
    plt.ylabel('number of Si II minima')
    fig.tight_layout()
    fig.savefig('SiII_Nmin_vs_impact.png')

    fig = plt.figure(figsize=(9,7))
    ax = fig.add_subplot(111)
    ax.scatter(nat['impact'], nat['O_VI_Nmin'], marker='D', color=nat_color,label='natural')
    ax.scatter(ref['impact'], ref['O_VI_Nmin'], color=ref_color, label='refined')
    plt.legend(loc='upper right')
    plt.xlabel('impact parameter [kpc]')
    plt.ylabel('number of O VI minima')
    fig.tight_layout()
    fig.savefig('OVI_Nmin_vs_impact.png')

    # fig = plt.figure(figsize=(9,7))
    # ax = fig.add_subplot(111)
    # ax.scatter(nat['Si_IV_col'], nat['C_IV_col'], marker='D', color=nat_color,label='natural')
    # ax.scatter(ref['Si_IV_col'], ref['C_IV_col'], color=ref_color, label='refined')
    # ax.plot([10.0, 14.5], [10.0+0.47712125472, 14.5+0.47712125472],color='black', label = 'CIV/SiIV = 3')
    # ax.plot([10.0, 14.5], [10.0+2*0.47712125472, 14.5+2*0.47712125472],color='black', ls=':',label = 'CIV/SiIV = 6')
    # plt.legend(loc='lower right')
    # plt.xlabel('Si IV column')
    # plt.ylabel('C IV column')
    # fig.tight_layout()
    # fig.savefig('SiIV_vs_CIV_column.png')

    fig = plt.figure(figsize=(9,7))
    ax = fig.add_subplot(111)
    sns.swarmplot(x="Si_II_dv90", y="Si_II_Ncomp", data=nat_si2, color=nat_color,alpha=0.7,orient='h')
    sns.swarmplot(x="Si_II_dv90", y="Si_II_Ncomp", data=ref_si2, color=ref_color,alpha=0.7,orient='h')
    sns.swarmplot(x="Si_II_dv90", y="Si_II_Ncomp", data=hires_si2, color='#984ea3',alpha=0.7,orient='h')
    # sns.swarmplot(x="Si_II_dv90", y="Si_II_Ncomp", data=kod_p, color='k',alpha=0.7,orient='h')
    #ax.scatter(nat['Si_II_dv90'],nat['Si_II_Nmin'], marker='D', s=60, color=nat_color,alpha=0.5,label='natural')
    #ax.scatter(ref['Si_II_dv90'],ref['Si_II_Nmin'], color=ref_color, marker='o',s=100, alpha=0.5,label='refined')
    ax.scatter(kodiaq['Si_II_dv90'], kodiaq['Si_II_Ncomp'], color='k', marker='*', s=100, label='KODIAQ',zorder=100)
    plt.legend(loc='lower right')
    plt.xlim(xmin=0)
    plt.ylim(-0.5,14.5)
    plt.xlabel(r'Si II $\Delta v_{90}$ [km/s]')
    plt.ylabel('# of Si II 1260 components')
    fig.tight_layout()
    fig.savefig('SiII_dv90_vs_Ncomp.png')

    fig = plt.figure(figsize=(9,7))
    ax = fig.add_subplot(111)
    sns.swarmplot(x="O_VI_dv90", y="O_VI_Nmin", data=nat_o6, color=nat_color,alpha=0.7,orient='h')
    sns.swarmplot(x="O_VI_dv90", y="O_VI_Nmin", data=ref_o6, color=ref_color,alpha=0.7,orient='h')
    sns.swarmplot(x="O_VI_dv90", y="O_VI_Nmin", data=hires_o6, color='#984ea3',alpha=0.7,orient='h')
    # sns.swarmplot(x="Si_II_dv90", y="Si_II_Ncomp", data=kod_p, color='k',alpha=0.7,orient='h')
    #ax.scatter(nat['Si_II_dv90'],nat['Si_II_Nmin'], marker='D', s=60, color=nat_color,alpha=0.5,label='natural')
    #ax.scatter(ref['Si_II_dv90'],ref['Si_II_Nmin'], color=ref_color, marker='o',s=100, alpha=0.5,label='refined')
    ax.scatter(kodiaq['O_VI_dv90'], kodiaq['O_VI_Nmin'], color='k', marker='*', s=100, label='KODIAQ',zorder=100)
    plt.legend(loc='upper left')
    plt.xlim(xmin=0)
    plt.ylim(-0.5,14.5)
    plt.xlabel(r'O VI $\Delta v_{90}$ [km/s]')
    plt.ylabel('# of O VI 1032 minima')
    fig.tight_layout()
    fig.savefig('OVI_dv90_vs_Nmin.png')


    fig = plt.figure(figsize=(9,7))
    ax = fig.add_subplot(111)
    sns.swarmplot(x="Si_II_EW", y="Si_II_Ncomp", data=nat_si2, color=nat_color,alpha=0.7,orient='h')
    sns.swarmplot(x="Si_II_EW", y="Si_II_Ncomp", data=ref_si2, color=ref_color,alpha=0.7,orient='h')
    #ax.scatter(nat['Si_II_EW'],nat['Si_II_Nmin'], marker='D', s=60, color=nat_color,label='natural')
    #ax.scatter(ref['Si_II_EW'],ref['Si_II_Nmin'], color=ref_color, marker='o',s=100, label='refined')
    ax.scatter(kodiaq['Si_II_EW'], kodiaq['Si_II_Nmin'], color='k', marker='*', s=100, label='KODIAQ', zorder=200)
    plt.legend(loc='lower right')
    plt.xlim(xmin=0)
    plt.ylim(1.5,14.5)
    plt.xlabel(r'Si II EW')
    plt.ylabel('# of Si II 1260 components')
    fig.tight_layout()
    fig.savefig('SiII_EW_vs_Ncomp.png')

    fig = plt.figure(figsize=(9,7))
    ax = fig.add_subplot(111)
    ax.scatter(nat['Si_IV_col'],nat['Si_IV_dv90'], marker='D', s=30, color=nat_color,alpha=0.5, label='natural')
    ax.scatter(ref['Si_IV_col'],ref['Si_IV_dv90'], color=ref_color, marker='o',s=50, alpha=0.5, label='refined')
    ax.scatter(kodiaq['Si_IV_col'], kodiaq['Si_IV_dv90'], color='k', marker='*', s=100, label='KODIAQ')
    plt.legend(loc='upper left')
    plt.xlim(xmin=10)
    plt.ylim(ymin=0)
    plt.xlabel('Si IV column density')
    plt.ylabel(r'Si IV $\Delta v_{90}$')
    fig.tight_layout()
    fig.savefig('SiIV_col_dv90.png')

    fig = plt.figure(figsize=(9,7))
    ax = fig.add_subplot(111)
    ax.scatter(nat['O_VI_col'],nat['O_VI_dv90'], marker='D', s=30, color=nat_color,alpha=0.5, label='natural')
    ax.scatter(ref['O_VI_col'],ref['O_VI_dv90'], color=ref_color, marker='o',s=50, alpha=0.5, label='refined')
    ax.scatter(kodiaq['O_VI_col'], kodiaq['O_VI_dv90'], color='k', marker='*', s=100, label='KODIAQ')
    plt.legend(loc='upper left')
    plt.xlim(xmin=10)
    plt.ylim(ymin=0)
    plt.xlabel('O VI column density')
    plt.ylabel(r'O VI $\Delta v_{90}$ [km/s]')
    fig.tight_layout()
    fig.savefig('OVI_col_dv90.png')

    fig = plt.figure(figsize=(9,7))
    ax = fig.add_subplot(111)
    ax.scatter(nat['HI_col'],nat['HI_1216_EW'], marker='D', s=60, color=nat_color,alpha=0.5, label='natural')
    ax.scatter(ref['HI_col'],ref['HI_1216_EW'], color=ref_color, marker='o',s=100, alpha=0.5, label='refined')
    plt.legend(loc='upper left')
    #plt.xlim(xmin=0)
    plt.ylim(ymin=0)
    plt.xlabel('HI column density')
    plt.ylabel(r'HI 1216 EW')
    fig.tight_layout()
    fig.savefig('HI_col_vs_ew.png')


    fig = plt.figure(figsize=(9,7))
    ax = fig.add_subplot(111)
    ax.scatter(nat['O_VI_col'],nat['O_VI_EW'], marker='D', s=60, color=nat_color,alpha=0.5, label='natural')
    ax.scatter(ref['O_VI_col'],ref['O_VI_EW'], color=ref_color, marker='o',s=100, alpha=0.5, label='refined')
    ax.scatter(kodiaq['O_VI_col'], kodiaq['O_VI_EW'], color='k', marker='*', s=100, alpha=0.5, label='KODIAQ')
    plt.legend(loc='upper left')
    #plt.xlim(xmin=0)
    #plt.ylim(ymin=0)
    plt.xlabel('O VI column density')
    plt.ylabel(r'O VI 1032 EW')
    fig.tight_layout()
    fig.savefig('OVI_col_ew.png')

    fig = plt.figure(figsize=(9,7))
    ax = fig.add_subplot(111)
    sns.swarmplot(x="Si_IV_col", y="Si_IV_Nmin", data=nat_p, color=nat_color,alpha=0.7,orient='h')
    sns.swarmplot(x="Si_IV_col", y="Si_II_Nmin", data=ref_p, color=ref_color,alpha=0.7,orient='h')
    #ax.scatter(nat['HI_col'],nat['Si_II_Nmin'], marker='D', s=60, color=nat_color,alpha=0.5,label='natural')
    #ax.scatter(ref['HI_col'],ref['Si_II_Nmin'], color=ref_color, marker='o',s=100, alpha=0.5,label='refined')
    ax.scatter(kodiaq['Si_IV_col'], kodiaq['Si_IV_Nmin'], color='k', marker='*', s=100, alpha=0.7, label='KODIAQ',zorder=100)
    plt.legend(loc='upper left', frameon=False)
    plt.xlim(xmin=10)
    plt.ylim(0.5,14.5)
    plt.xlabel(r'log SiIV column density')
    plt.ylabel('# of Si IV 1394 minima')
    fig.tight_layout()
    fig.savefig('SiIV_col_vs_Ncomp.png')

    fig = plt.figure(figsize=(9,7))
    ax = fig.add_subplot(111)
    sns.swarmplot(x="HI_col", y="Si_II_Nmin", data=nat_p, color=nat_color,alpha=0.7,orient='h')
    sns.swarmplot(x="HI_col", y="Si_II_Nmin", data=ref_p, color=ref_color,alpha=0.7,orient='h')
    #ax.scatter(nat['HI_col'],nat['Si_II_Nmin'], marker='D', s=60, color=nat_color,alpha=0.5,label='natural')
    #ax.scatter(ref['HI_col'],ref['Si_II_Nmin'], color=ref_color, marker='o',s=100, alpha=0.5,label='refined')
    ax.scatter(kodiaq['HI_col'], kodiaq['Si_II_Nmin'], color='k', marker='*', s=100, alpha=0.7, label='KODIAQ',zorder=100)
    plt.legend(loc='upper left', frameon=False)
    plt.xlim(xmin=16)
    plt.ylim(0,14)
    plt.xlabel(r'log HI column density')
    plt.ylabel('# of Si II 1260 minima')
    fig.tight_layout()
    fig.savefig('HI_col_vs_SiII_Nmin.png')

    fig = plt.figure(figsize=(9,7))
    ax = fig.add_subplot(111)
    ax.scatter(nat['HI_col'],nat['Si_IV_Nmin'], marker='D', s=60, color=nat_color,alpha=0.5,label='natural')
    ax.scatter(ref['HI_col'],ref['Si_IV_Nmin'], color=ref_color, marker='o',s=100, alpha=0.5,label='refined')
    ax.scatter(kodiaq['HI_col'], kodiaq['Si_IV_Nmin'], color='k', marker='*', s=100, alpha=0.7, label='KODIAQ',zorder=100)
    plt.legend(loc='upper left', frameon=False)
    plt.xlim(xmin=16)
    plt.ylim(ymin=0)
    plt.xlabel(r'log HI column density')
    plt.ylabel('# of Si IV 1394 minima')
    fig.tight_layout()
    fig.savefig('HI_col_vs_SiIV_Nmin.png')

    fig = plt.figure(figsize=(9,7))
    ax = fig.add_subplot(111)
    sns.stripplot(x=nat['O_VI_Nmin'], y=nat['Si_II_Nmin']+0.1,jitter=True, color=nat_color, dodge=True,edgecolor='none',s=5, marker='D',alpha=0.5)
    sns.stripplot(x=ref['O_VI_Nmin'], y=ref['Si_II_Nmin']-0.1,jitter=True, color=ref_color, dodge=True,edgecolor='none',s=5, marker='o',alpha=0.5)
    # ax.scatter(nat['O_VI_Nmin'],nat['Si_II_Nmin'], marker='D', s=60, color=nat_color,alpha=0.5,label='natural')
#    ax.scatter(ref['O_VI_Nmin'],ref['Si_II_Nmin'], color=ref_color, marker='o',s=100, alpha=0.5,label='refined')
    ax.scatter(kodiaq['O_VI_Nmin'], kodiaq['Si_II_Nmin'], color='k', marker='*', s=100, alpha=0.7, label='KODIAQ',zorder=100)
    plt.legend(loc='upper left', frameon=False)
    plt.xlim(xmin=0)
    plt.ylim(ymin=0)
    plt.xlabel('# of O VI 1032 minima')
    plt.ylabel('# of Si II 1260 minima')
    fig.tight_layout()
    fig.savefig('OVI_Nmin_vs_SiII_Nmin.png')

    fig = plt.figure(figsize=(9,7))
    ax = fig.add_subplot(111)
    ax.scatter(nat['C_II_dv90'],nat['C_II_Ncomp'], marker='D', s=100, color=nat_color,label='natural')
    ax.scatter(ref['C_II_dv90'],ref['C_II_Ncomp'], color=ref_color, marker='*',s=100, label='refined')
    plt.legend(loc='lower right')
    plt.xlim(xmin=0)
    plt.ylim(ymin=0)
    plt.xlabel(r'C II $\Delta v_{90}$')
    plt.ylabel('# of C II 1335 components')
    fig.tight_layout()
    fig.savefig('CII_dv90_vs_Ncomp.png')


    bins = np.arange(1,20,1)
    fig = plt.figure(figsize=(9,7))
    ax = fig.add_subplot(111)
    print('min KODIAQ SiII col = ', min(kodiaq['Si_II_col']))
    idn = [nat['Si_II_col'] > 12]
    idr = [ref['Si_II_col'] > 12]
    idh = [hires['Si_II_col'] > 12]
    ax.hist(nat['Si_II_Nmin'][idn], color=nat_color, bins=bins,normed=True, alpha=0.5, label='natural')
    ax.hist(ref['Si_II_Nmin'][idr], color=ref_color, bins=bins,normed=True, alpha=0.5,  label='refined')
    ax.hist(hires['Si_II_Nmin'][idh], color='#984ea3', bins=bins,normed=True, alpha=0.5,  label='nref11f')
    ax.hist(kodiaq['Si_II_Nmin'], color='k',bins=bins,normed=True,histtype='step',lw=2,label='KODIAQ' )
    plt.legend(loc='upper right')
    plt.xlabel('# of Si II 1260 minima')
    fig.tight_layout()
    fig.savefig('Si_II_histograms.png')

    fig = plt.figure(figsize=(9,7))
    ax = fig.add_subplot(111)
    sns.swarmplot(x="Si_II_col", y="Si_II_Nmin", data=nat_p, color=nat_color,alpha=0.7,orient='h')
    sns.swarmplot(x="Si_II_col", y="Si_II_Nmin", data=ref_p, color=ref_color,alpha=0.7,orient='h')
    #ax.scatter(nat['HI_col'],nat['Si_II_Nmin'], marker='D', s=60, color=nat_color,alpha=0.5,label='natural')
    #ax.scatter(ref['HI_col'],ref['Si_II_Nmin'], color=ref_color, marker='o',s=100, alpha=0.5,label='refined')
    ax.scatter(kodiaq['Si_II_col'], kodiaq['Si_II_Nmin'], color='k', marker='*', s=100, alpha=0.7, label='KODIAQ',zorder=100)
    plt.legend(loc='upper left', frameon=False)
    plt.xlim(xmin=10)
    plt.ylim(1.5,14.5)
    plt.xlabel(r'log SiII column density')
    plt.ylabel('# of Si II 1260 minima')
    fig.tight_layout()
    fig.savefig('SiII_col_vs_Nmin.png')

    fig = plt.figure(figsize=(9,7))
    ax = fig.add_subplot(111)
    print('min KODIAQ SiIV col = ', min(kodiaq['Si_IV_col'][kodiaq['Si_IV_col'] > 0]))
    idn = [nat['Si_IV_col'] > 11.5]
    idr = [ref['Si_IV_col'] > 11.5]
    ax.hist(nat['Si_IV_Nmin'][idn], color=nat_color, bins=bins,normed=True, alpha=0.5, label='natural')
    ax.hist(ref['Si_IV_Nmin'][idr], color=ref_color, bins=bins,normed=True, alpha=0.5,  label='refined')
    ax.hist(kodiaq['Si_IV_Nmin'], color='k',bins=bins,normed=True,histtype='step',lw=2,label='KODIAQ'  )
    plt.legend(loc='upper right')
    plt.xlabel('# of Si IV 1260 minima')
    fig.tight_layout()
    fig.savefig('Si_IV_histograms.png')

    fig = plt.figure(figsize=(9,7))
    ax = fig.add_subplot(111)
    print('min KODIAQ CIV col = ', min(kodiaq['C_IV_col'][kodiaq['C_IV_col'] > 0]))
    idn = [nat['C_IV_col'] > 12]
    idr = [ref['C_IV_col'] > 12]
    ax.hist(nat['C_IV_Nmin'][idn], color=nat_color,bins=bins, normed=True, alpha=0.5, label='natural')
    ax.hist(ref['C_IV_Nmin'][idr], color=ref_color, bins=bins,normed=True, alpha=0.5,  label='refined')
    ax.hist(kodiaq['C_IV_Nmin'], color='k',bins=bins,normed=True,histtype='step',lw=2,label='KODIAQ' )
    plt.legend(loc='upper right')
    plt.xlabel('# of C IV 1548 minima')
    fig.tight_layout()
    fig.savefig('C_IV_histograms.png')

    fig = plt.figure(figsize=(9,7))
    ax = fig.add_subplot(111)
    print('min KODIAQ OVI col = ', min(kodiaq['O_VI_col'][kodiaq['O_VI_col'] > 0]))
    idn = [nat['O_VI_col'] > 13] ## 11.2
    idr = [ref['O_VI_col'] > 13]
    ax.hist(nat['O_VI_Nmin'][idn], color=nat_color, bins=bins,normed=True, alpha=0.5, label='natural')
    ax.hist(ref['O_VI_Nmin'][idr], color=ref_color, bins=bins,normed=True, alpha=0.5,  label='refined')
    ax.hist(kodiaq['O_VI_Nmin'], color='k',bins=bins,normed=True,histtype='step',lw=2,label='KODIAQ')
    plt.legend(loc='upper right')
    plt.xlabel('# of O VI 1032 minima')
    fig.tight_layout()
    fig.savefig('O_VI_histograms.png')

    ## KS-test
    for key in ['Si_II_Nmin','Si_IV_Nmin', 'C_IV_Nmin', 'O_VI_Nmin']:
        print(key, 'nat vs. KODIAQ:', stats.ks_2samp(np.array(nat[key][key > 0])[0], np.array(kodiaq[key][key > 0])[0]))
        print(key, 'ref vs. KODIAQ:', stats.ks_2samp(np.array(ref[key][key > 0])[0], np.array(kodiaq[key][key > 0])[0]))


if __name__ == "__main__":
    make_misty_plots()
