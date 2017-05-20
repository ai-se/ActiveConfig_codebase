c = ['#F6511D','#FFB400','#00A6ED','#7FB800','#0D2C54']

apache_mmre = [31.75, 18.61, 14, 8.72, 6.64]
apache_evals = [4, 8, 16, 32, 77]

bdbj_mmre = [61.45, 46.68, 9.82, 2.42, 1.96]
bdbj_evals = [4, 8, 16, 32, 64]

bdbc_mmre = [183.04, 27.17, 6.12, 1.52, 1.11]
bdbc_evals = [16, 32, 64, 128, 256]

x264_mmre = [18.12, 9.39, 7.27, 3.17, 0.96]
x264_evals = [8, 16, 32, 64, 128]

sqlite_mmre = [6, 5.7, 5.52, 5.12, 4.77]
sqlite_evals = [16, 32, 64, 128, 256]

llvm_mmre = [6.81, 4.75, 3.32, 2.3, 1.94]
llvm_evals = [8, 16, 32, 64, 128]

import matplotlib.pyplot as plt

f, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(2, 3)

ax1.plot(apache_evals,apache_mmre, color='r', marker=None, zorder=1)
ax1.scatter(apache_evals,apache_mmre, color=c, marker='s', zorder=2, s=32)

ax1.set_xticks([i*15 for i in xrange(6)])
ax1.set_title('Apache')

ax2.plot(bdbc_evals, bdbc_mmre, color='r', marker=None, zorder=1)
ax2.scatter(bdbc_evals, bdbc_mmre, color=c, marker='s', zorder=2, s=32)

ax2.set_xticks([i*100 for i in xrange(4)])
ax2.set_ylim(-5, 200)
ax2.set_title('BDBC')

ax3.plot(bdbj_evals, bdbj_mmre, color='r', marker=None, zorder=1)
ax3.scatter(bdbj_evals, bdbj_mmre, color=c, marker='s', zorder=2, s=32)

ax3.set_xticks([i*15 for i in xrange(6)])
ax3.set_ylim(-1, 70)
ax3.set_title('BDBJ')

ax4.plot(llvm_evals, llvm_mmre, color='r', marker=None, zorder=1)
ax4.scatter(llvm_evals, llvm_mmre, color=c, marker='s', zorder=2, s=32)

ax4.set_xticks([i*30 for i in xrange(6)])
ax4.set_title('LLVM')

ax5.plot(sqlite_evals, sqlite_mmre, color='r', marker=None, zorder=1)
ax5.scatter(sqlite_evals, sqlite_mmre, color=c, marker='s', zorder=2, s=32)

ax5.set_xticks([i*100 for i in xrange(4)])
ax5.set_ylim(0, 10)
ax5.set_title('SQL')

ax6.plot(x264_evals, x264_mmre, color='r', marker=None, zorder=1)
ax6.scatter(x264_evals, x264_mmre, color=c, marker='s', zorder=2, s=32)

ax6.set_xticks([i*30 for i in xrange(6)])
ax6.set_ylim(-3, 20)
ax6.set_title('x264')


from matplotlib.lines import Line2D
circ1 = Line2D([0], [0], linestyle="none", marker="s",  markersize=10, color="#F6511D")
circ2 = Line2D([0], [0], linestyle="none", marker="s", markersize=10, color="#FFB400")
circ3 = Line2D([0], [0], linestyle="none", marker="s", markersize=10, color="#00A6ED")
circ4 = Line2D([0], [0], linestyle="none", marker="s", markersize=10, color="#7FB800")
circ5 = Line2D([0], [0], linestyle="none", marker="s", markersize=10, color="#0D2C54")

r'$\alpha > \beta$'
plt.figlegend((circ1, circ2, circ3, circ4, circ5), (r'$4\cdot \sqrt{N}$', r'$2\cdot \sqrt{N}$', r'$\sqrt{N}$', r'$\frac{1}{2}\cdot \sqrt{N}$', r'$\frac{1}{4}\cdot \sqrt{N}$'), frameon=False, loc='lower center',
              bbox_to_anchor=(0.5, 0.98),fancybox=True, ncol=5, scatterpoints=1)


f.text(0.005, 0.5, 'MRE', va='center', rotation='vertical', fontsize=13)
f.text(0.40, 0.005, '# Evaluations', va='center',  fontsize=13)

f.tight_layout()
f.set_size_inches(8, 5)
plt.savefig('draw.png', bbox_inches='tight',)