#
# this script computes and plots the classic Moody Diagram from fluid mechanics.
# The Moody diagram allows an engineer to obtain the friction factor for a conduit,
# given the flow Reynolds number and the relative roughness of the conduit.
#
# reference: http://en.wikipedia.org/wiki/Moody_diagram
#
# the range of Reynolds numbers used and the selection of relative roughness values matches the
# classical Moody charts that are widely available.  Obviously, the numbers may be modified to
# meet your personal needs.
#
# Daniel G. Hyams

import sys
try:
    import numpy
    import scipy.optimize
except ImportError:
    print ()"This example must have both numpy and scipy installed.")
    sys.exit(1)
import functools
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams['figure.figsize'] = (11.0,7.0)
matplotlib.rcParams['font.size'] = 12.0
matplotlib.rcParams['figure.subplot.left'] = 0.15
matplotlib.rcParams['figure.subplot.right'] = 0.85
matplotlib.rcParams['figure.subplot.bottom'] = 0.15
matplotlib.rcParams['figure.facecolor'] = 'white'
matplotlib.rcParams['lines.linewidth'] = 1
#matplotlib.rcParams['axes.color_cycle'] = ['blue','magenta','green','cyan']
#matplotlib.rcParams['axes.color_cycle'] = ['#0000CC']
matplotlib.rcParams['axes.color_cycle'] = ['#0000AA','#AA0000','#00AA00']
ccycle = matplotlib.rcParams['axes.color_cycle']

def colebrook(f,ks_D,Re):
    # meant to be used as part of a Newton iteration, so the equation has been rearranged such that
    # it is equal to zero.
    sf = numpy.sqrt(f)
    return -2*numpy.log10(ks_D/3.7 + 2.51/Re/sf) - 1/sf

def draw_range_arrow(x1,x2,y,label,fudge=0.005):
    # hmm, this doesn't work.  Have to transform things manually.
    #plt.arrow(6e2,0.02,2e3-6e2,0.0,transform=plt.gca().transData,length_includes_head=True,shape='full')
    # it appears that using arrow directly does not allow one to put arrow heads on both ends, nor does
    # it obey the log transformation correctly.
    xy1 = (x1,y)
    xy2 = (x2,y)
    plt.text(10**(0.5*(numpy.log10(xy1[0])+numpy.log10(xy2[0]))),xy1[1]-fudge,label,ha='center',va='top',size=10,zorder=500)
    plt.annotate('',xy1,xy2,arrowprops=dict(arrowstyle='<|-|>',fc='black'))#,xycoords='axes fraction',zorder=500)


# list of relative roughnesses to compute a curve for.
rrlist = [0.0,0.00001,0.00002,0.00003,0.00005,0.0001,0.0002,0.0004,0.0006,0.001,0.002,0.003,0.004,0.006,0.008,0.01,0.015,0.02,0.03,0.04,0.05]

# range of Reynolds numbers to use for computing the turbulent friction factors.  Will be equally
# spaced logarithmically over the range.
Remin_t = 3e3
Remax_t = 100e6

# set the limits of the chart
Remin = 6e2
Remax = Remax_t
fmin  = 0.008
fmax = 0.1

Rerange = numpy.linspace(numpy.log10(Remin_t),numpy.log10(Remax_t),200)
Rerange = 10**Rerange

# do the computation first.
f0 = 0.03
curve = {}
for ks_D in rrlist:
    ff = numpy.zeros(Rerange.shape)
    for idx,Re in enumerate(Rerange):
        func = functools.partial(colebrook,ks_D=ks_D,Re=Re)
        f = scipy.optimize.newton(func,f0)
        ff[idx] = f
        f0 = f # use the initial guess from previous solution
    curve[ks_D] = ff

# generate the data for the curve that shows the demarcation between transitional flow
# and fully rough flow.
ReT = []
fT = []
f0 = curve[rrlist[1]][-1]
for ks_D in rrlist[1:] + [0.06,0.07,0.08,0.09,0.1]:
    ReT.append(1600.0/ks_D)
    func = functools.partial(colebrook,ks_D=ks_D,Re=ReT[-1])
    fT.append(scipy.optimize.newton(func,f0))
    f0 = fT[-1]

# also compute the laminar friction factor
Rerange_l1 = numpy.linspace(numpy.log10(1e2),numpy.log10(2e3),5)
Rerange_l1 = 10**Rerange_l1
Rerange_l2 = numpy.linspace(numpy.log10(2e3),numpy.log10(3.5e3),5)
Rerange_l2 = 10**Rerange_l2
flaminar1 = 64/Rerange_l1
flaminar2 = 64/Rerange_l2

# now, do some plotting.

# plot the laminar curve
plt.loglog(Rerange_l1,flaminar1,color='#0000AA',lw=1.5)
plt.loglog(Rerange_l2,flaminar2,color='#0000AA',linestyle='dashed',dashes=[4,4],lw=1.5)

# plot the curves in the transitional/turbulent zone for each roughness
for i,ks_D in enumerate(rrlist):
   cutoff = 7
   plt.loglog( Rerange[cutoff-1:],curve[ks_D][cutoff-1:],color=ccycle[i%len(ccycle)],linewidth=1.5)
   plt.loglog( Rerange[:cutoff],curve[ks_D][:cutoff],color=ccycle[i%len(ccycle)],linewidth=1.5,dashes=[3,3])
   yfinal = curve[ks_D][-1]
   xfinal = Rerange[-1] + Rerange[-1]/10.0 # fudge a little to the right
   if yfinal > 0.008:
      plt.text(xfinal,yfinal,"%g"%ks_D,size='small',va='center')

# plot the division between transitional and fully rough flow.
plt.loglog(ReT,fT,color='orange',linestyle='dashed',linewidth=1)

ax = plt.gca()
plt.title('Moody Diagram',y=1.02)
plt.xlim(Remin,Remax)
plt.ylim(fmin,fmax)

plt.ylabel(r'Darcy friction factor, $f$')
plt.xlabel(r"Reynolds number, $Re_D$")
plt.text(1.1,0.5,r"relative roughness, $\epsilon/D$",transform=plt.gca().transAxes,rotation='vertical',va='center')
plt.text(1e6,.011,r"smooth ($\epsilon/D = 0$)",size='small',va='center',ha='center',rotation=-32)

plt.grid(True,which='both',linestyle='solid',color='gray',alpha=0.5)
yformatter = matplotlib.ticker.FormatStrFormatter("%.3f")
ax.yaxis.set_major_formatter(yformatter)
ax.yaxis.set_minor_formatter(yformatter)

# patch that shows the laminar region.
verts = [(6e2,0.008),(2e3,0.0008),(2e3,.1),(6e2,.1)]
poly = matplotlib.patches.Polygon(verts, facecolor='blue', linewidth=0,alpha=0.12)
ax.add_patch(poly)
draw_range_arrow(Remin,2e3,0.094,'laminar')

# patch that shows the transition region.
verts = [(2e3,.1),(4e3,.1),(4e3,.0008),(2e3,.0008)]
poly = matplotlib.patches.Polygon(verts, facecolor='red', linewidth=0,alpha=0.2)
ax.add_patch(poly)
draw_range_arrow(2e3,4e3,0.094,'critical')

# patch that colors the turbulent/transition zone
ix = numpy.linspace(ReT[-1],4e3,10)
iy = numpy.linspace(0.1,0.1,10)
ix2 = numpy.linspace(4e3,4e3,10)
iy2 = numpy.linspace(0.1,curve[0.0][0],10)
#verts = list(zip(ReT,fT)) + list (zip(ix,iy)) + list(zip(ix2,iy2)) + list(zip(Rerange,curve[0.0]))
verts = list(zip(ReT,fT))  + list (zip(ix,iy)) + list(zip(ix2,iy2)) + [(4e3,0.0008),(Rerange[-1],0.0008)]
poly = matplotlib.patches.Polygon(verts, facecolor='red', linewidth=0,alpha=0.05)
ax.add_patch(poly)
draw_range_arrow(4e3,1.9e4,0.094,'transitional')

# patch that colors the turbulent/fully rough zone
ix = numpy.linspace(ReT[-1], Rerange[-1], 10)
iy = numpy.linspace(0.1,0.1,10)
verts = list(zip(ReT,fT)) + list(zip(ix,iy))
poly = matplotlib.patches.Polygon(verts, facecolor='yellow', linewidth=0,alpha=0.1)
ax.add_patch(poly)
draw_range_arrow(1.8e4,Rerange[-1],0.094,'fully turbulent')

# add a table of common roughnesses
chart = [
["glass, plastic","smooth"],
["copper or brass","0.0015"],
["wrought iron, steel","0.046"],
["asphalted cast iron","0.12"],
["galvanized iron","0.15"],
["cast iron","0.26"],
["concrete","0.3 to 3.0"],
["riveted steel","0.9-9"],
["straight rubber pipe","0.025"]
]
rect = matplotlib.patches.Rectangle((0.03,0.03),0.4,0.28,fc='white',transform=plt.gca().transAxes)
ax.add_patch(rect)
tab = plt.table(cellText=chart,colLabels=["material",r"$\epsilon$ (mm)"],colColours=['white']*2,bbox=(0.03,0.03,0.4,0.28))
tab.set_fontsize(10.0)
tab.set_zorder(500)

plt.text(0.98,0.02,"Created with matplotlib %s"%matplotlib.__version__,transform=plt.gcf().transFigure,size='x-small',ha='right')


plt.show()
