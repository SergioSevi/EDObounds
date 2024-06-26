import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

import argparse
import tools

#Specify the plot style
mpl.rcParams.update({'font.size': 16,'font.family':'serif'})
mpl.rcParams['xtick.major.size'] = 7
mpl.rcParams['xtick.major.width'] = 1
mpl.rcParams['xtick.minor.size'] = 3.5
mpl.rcParams['xtick.minor.width'] = 1
mpl.rcParams['ytick.major.size'] = 7
mpl.rcParams['ytick.major.width'] = 1
mpl.rcParams['ytick.minor.size'] = 3.5
mpl.rcParams['ytick.minor.width'] = 1
mpl.rcParams['xtick.direction'] = 'in'
mpl.rcParams['ytick.direction'] = 'in'
mpl.rcParams['lines.linewidth'] = 1.5
mpl.rcParams['xtick.top'] = True
mpl.rcParams['ytick.right'] = True
mpl.rcParams['font.family'] = 'serif'
mpl.rc('text', usetex=True)

mpl.rcParams['legend.edgecolor'] = 'inherit'


#Default values, overridden if you pass in command line arguments
listfile_default = "listfiles/bounds_all.txt" 
outfile_default = "plots/EDO_bounds.pdf"

#Load in the filename with the list of bounds and the output filename
parser = argparse.ArgumentParser(description='...')
parser.add_argument('-lf','--listfile', help='File containing list of bounds to include',
                    type=str, default=listfile_default)
parser.add_argument('-of','--outfile', help='Filename (with extension) of output plot', 
                    type=str, default=outfile_default)
                    

args = parser.parse_args()
listfile = args.listfile
outfile = args.outfile

#This small routine gets all lines in the listfile starting with a #, which will be used to identify the shape, radius and constraints.
with open(listfile, 'r') as file:
    # Read the contents line by line into a list
    lines = file.readlines()

hash_line_indices = [index for index, line in enumerate(lines) if line.startswith('#')]


alpha_val = 0.03
shape=np.loadtxt(listfile,usecols=(0,),dtype=str)[0]
limits=np.loadtxt(listfile,skiprows=(hash_line_indices[1]+1), usecols=(0,1,2),dtype=str)[0]
Lensinglist=['EROS-2','OGLE-IV','Subaru-HSC']
table_row_start = hash_line_indices[2]+1

bounds = np.loadtxt(listfile,skiprows=table_row_start, usecols=(0,), dtype=str)
lines = np.loadtxt(listfile, skiprows=table_row_start,usecols=(1,), dtype=str)
xlist = np.loadtxt(listfile,skiprows=table_row_start, usecols=(2,))
ylist = np.loadtxt(listfile, skiprows=table_row_start,usecols=(3,))
anglist = np.loadtxt(listfile, skiprows=table_row_start,usecols=(4,))
labellist = np.loadtxt(listfile, skiprows=table_row_start,usecols=(5,), dtype=str)

colours=[(0.698039,0.0156863,0.), (0.937255,0.627451,0.168627),
         (0.72549,0.8,0.0705882),
         (0.317647,0.490196,0.0784314),(0.172549,0.360784,0.0705882),
         (0.360784,0.407843,0.533333),(0.227451,0.239216,0.45098),
         (0.0980392,0.0666667,0.25098),(0.560784,0.52549,0.564706),(0.921569,0.494118,0.431373)]


# if (DARKMODE):
#     for i, col in enumerate(colors):
#         if (col == "C1"):
#             colors[i] = "C5"
#         if (col == "C2"):
#             colors[i] = "C6"

def addConstraint(boundID,x = 1e-30,y=1e-4,ang=0, linestyle='-', labeltext=''):
    cc=0
    bounds_on = 0
    for radius in range(int(limits[0]),int(limits[1])+1,int(limits[2])):
        m, f = tools.load_bound(boundID,shape,radius)
        if min(f)<1:
            bounds_on = 1
        col=colours[cc]
        cc=cc+1
        plt.fill_between(m , f, 1e10, alpha=alpha_val, color=col)
        linewidth = 1.0

        if boundID == bounds[0]:

            plt.plot(m, f, color=col, lw=linewidth, linestyle=linestyle,
                     label='$10^{{{}}} R_\\odot$'.format(radius) if not radius==1 and not radius==0 else str(1+9*radius)+'$R_\\odot$')
        else:
            plt.plot(m, f, color=col, lw=linewidth, linestyle=linestyle)
    if x > 1e-20 and bounds_on == 1:
        print(boundID)
        plt.text(x, y, labeltext.replace("_", " "), rotation=ang, fontsize=12, ha='center', va='center')



#Create the citation list for the last produced plot:
def addCitation(boundID):
    filename = 'bounds/' + boundID + '/Citation.txt'
    lines=' '
    try:
        for line in open(filename):
            li=line.strip()
            if not li.startswith("#"):
                lines = lines +'\n '+li
                if li.startswith("@") :
                    frstline = str(li)
                    startcite = frstline.find('{')+1
                    endcite = frstline.find(',')
                    frstline = frstline[startcite:endcite]
    except Exception as e:
        frstline = ""
        lines = ""
    return [frstline, str(lines)]


bibdatlist = []
cits = open('Cite.txt','w')
bibitems = 'These are the bibitems to add to your mybib file:'
citelist = 'These are the items to cite in your plot:\n \\cite{'
bounds_citation = bounds
if 'Lensing' in bounds:
    for i in Lensinglist:
        bounds_citation = np.append(bounds_citation,i)
    
for i in range(len(bounds_citation)): 
    bibdat = addCitation(bounds_citation[i])
    if bibdat[0] in bibdatlist or bibdat[0] == "":
        pass
    else:
        if i == 0:
            citelist = citelist+bibdat[0]
            bibitems = bibitems + bibdat[1] + ';\n\n'
        else:    
            citelist = citelist + ',' + bibdat[0]
            bibitems = bibitems + bibdat[1] + ';\n\n'

    bibdatlist = bibdatlist + [bibdat[0]]        
citelist=citelist + '}\n\n'    
cits.write(citelist)
cits.write(bibitems)
cits.close()

 #-------------------------------------------    
    
plt.figure(figsize=(8,5))

ax = plt.gca()
ax.set_xscale('log')
ax.set_yscale('log')
ax.xaxis.tick_bottom()
ax.xaxis.set_tick_params(pad=5)
for i in range(len(bounds)):  
    addConstraint(bounds[i], x = xlist[i], y = ylist[i], ang=anglist[i], linestyle=lines[i], labeltext=labellist[i])


Msun_min = 1e-18
Msun_max = 1e7

#Plotting stuff
plt.axhspan(1, 1.5, facecolor='white', alpha=1, zorder=10)
plt.axhspan(1, 1.5, facecolor='grey', alpha=0.5, zorder=10)
    
plt.ylim(5e-6, 1.5)
plt.xlim(Msun_min, Msun_max)
    
xticks = 10**np.arange(np.floor(np.log10(Msun_min)), np.ceil(np.log10(Msun_max))+1)
ax.set_xticks(xticks, minor=True)
ax.set_xticklabels([], minor=True)
    
ax.set_xlabel(r'$M_\mathrm{EDO}$ [$M_\odot$]')
plt.ylabel(r'$f_\mathrm{DM} = \Omega_\mathrm{EDO}/\Omega_\mathrm{DM}$')

ax_top = ax.twiny()
ax_top.xaxis.tick_top()
ax_top.set_xscale('log')
ax_top.set_xlim(ax.get_xlim())
ax_top.set_xlabel(r'$M_\mathrm{EDO}$ [g]', labelpad=7)

ax.legend( loc='best',fontsize='x-small',ncol=2,fancybox=False,title=str(shape)+" $R_{90}$ size:",labelspacing=0.1,handlelength=1,title_fontsize=12,columnspacing=1)
g_to_Msun = 1/1.989e+33

g_ticks_minor =  10**np.arange(np.floor(np.log10(Msun_min/g_to_Msun)), np.ceil(np.log10(Msun_max/g_to_Msun))+1)
g_ticks = g_ticks_minor[::3]

g_tick_labels = [r"$10^{" + str(int(np.log10(x))) +"}$" for x in g_ticks]

ax_top.set_xticks(g_ticks*g_to_Msun)
ax_top.set_xticklabels(g_tick_labels)
ax_top.xaxis.set_tick_params(pad=0)

ax_top.set_xticks(g_ticks_minor*g_to_Msun,minor=True)
ax_top.set_xticklabels([],minor=True)


plt.savefig(outfile, bbox_inches='tight')
    
plt.show()


