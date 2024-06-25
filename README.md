## EDObounds

 [![arXiv](https://img.shields.io/badge/arXiv-2007.10722-B31B1B.svg)](...) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

*A collection of bounds on extended dark matter objects (EDOs) and code for plotting them.*

 ![All PBH bounds](plots/all_bounds.png)


### Bounds

The list of all available, tabulated bounds can be found in the [bounds/](bounds/) folder, with a dedicated sub-folder for each shape: NFW subhalos, boson stars, uniform spheres and ultra-compact minihalos (see paper for a description of their density functions).

In Section 3 of the paper we explain in detail how to use the code.

### Contributing

If you'd like to contribute to the repository with new bounds, you can either:
1. Make the changes yourself:
	* Add the new bound as a folder in the [bounds/](bounds/) folder, containing one sub-folder for each shape (you don't need to have bounds for all) and one ".txt" file with the bibitem of your paper and a small comment linking the source of the bounds. Inside each sub-folder, include one ".txt" file for each provided radius, names "rN.txt", where N is given by $R_{90}=10^N R_{\odot}$ (for negative exponentials write a hyphen, e.g., $r-1.txt" for $R_{90}=10^{-1}R_{\odot}$). Each file should have two columns, corresponding to the EDO mass in Solar masses, and the constraint on the EDO fraction.
	* Update the [bounds/README.md](https://github.com/SergioSevi/EDObounds/blob/master/bounds/README.md) file with information about the new bound.
	* Submit a pull request
2. Create an issue here on the github repository with a link to the paper/bound you believe taht is missing.  
3. Contact us directly at sergio.sevillano-munoz@durham.ac.uk or djuna.croon@durham.ac.uk and let us know which bound you think should be added.

### Plots

Some example plots for different EDO radius and shapes can be found in the [plots/](plots/) folder.

You can produce new plots with
```
python PlotEDObounds.py -listfile LIST_FILE -outfile OUT_FILE
```
where `LIST_FILE` is a text file containing a list of bounds to be plotted (see `listfiles/list_all.txt` for an example) and `OUT_FILE` is the full filename of the image to be output (e.g. `plots/PBHbounds.pdf`). You can use the short flags `-lf` and `-of` for specifying the list file and output file.


This code is an extension of Bradley Kavanagh's pbh bounds repository. Among the new additions, this code automatically generates the list of citations for all bounds appearing in the created plot in a file called "Cite.txt".
### Versions

**Version 1.0 (25/06/2024):** Release version. Created for the paper.

### Citation

Feel free to use the bounds and code, but please make sure of citing all of the individual plotted bounds (the bibitems for this is automatically generated in the "Cite.txt" file) and this repository through the paper.

