# SVBRDF-Remapping
Code repository for the paper "Image-based remapping of spatially-varying material appearance" (JCGT)

<b>Image-based remapping of spatially-varying material appearance</b><br>
[Alejandro Sztrajman](https://asztr.github.io),
[Jaroslav Krivanek](https://cgg.mff.cuni.cz/~jaroslav/),
[Alexander Wilkie](https://cgg.mff.cuni.cz/~wilkie/Website/Home.html),
[Tim Weyrich](https://reality.cs.ucl.ac.uk/weyrich.html)<br>
<i>Journal of Computer Graphics Techniques</i> (JCGT), 8(4), pp. 1-30, 2019.

### [Project Page](http://reality.cs.ucl.ac.uk/projects/reflectance-remapping/sztrajman2019image-based.html) | [Paper](http://jcgt.org/published/0008/04/01/paper.pdf)

<video src="https://user-images.githubusercontent.com/10238412/187590012-ba23aeab-8a2d-4044-aaa0-11de2fdd925b.mp4" loop="true" style="max-height:420px;"></video>
Cross-renderer SVR remapping of hydrant from Mitsuba (Ward) to Cycles (GGX). Left: source material in Mitsuba Ward. Center: remapped in Blender-Cycles (GGX). Right: SSIM difference. Tabac plant environment map rotates from 0 to 360 degrees.


### Regression

<b>parametric_remapping.py:</b>
Reads uniform remapping data from `mitsuba-ward2mitsuba-beck.csv`, fits with parametric remapping method and output plots of data and fitting curve (`roughness_vs_roughness.jpg` and `specular_vs_specular.jpg`). Also reads `specular.exr` and `roughness.exr` textures and outputs remapped versions (`roughness_beck_remapped.exr` and `specular_beck_remapped.exr`).
```
$ python parametric_remapping.py
```

<b>svr_remapping.py:</b>
Reads uniform remapping data from `mitsuba-ward2mitsuba-beck.csv`, fits with SVR remapping method and uses fitting to remap `specular.exr` and `roughness.exr` textures. Fitted SVR models are saved in disk for subsequent runs.
```
$ python svr_remapping.py
```

### Visualization

For visualisation of the original and remapped SVBRDF assets, install the `pbr.cpp` plugin in Mitsuba and then run mitsuba on the scene files.

<b>pbr.cpp:</b>
Mitsuba PBR BRDF plugin with Schlick's Fresnel term.
For usage: copy this file into `mitsuba/src/bsdfs` and compile Mitsuba. For scons compilation add the following line to `mitsuba/src/bsdfs/SConscript`:
```
plugins += env.SharedLibrary('pbr', ['pbr.cpp'])
```

<b>ward.xml:</b>
Mitsuba scene file that uses the Ward BRDF with the original texture maps.
```
$ mitsuba ward.xml
```

<b>beck_parametric.xml:</b>
Mitsuba scene file that uses the Beckmann BRDF with the parametric remapped texture maps (make sure to run `parametric_remapping.py` before running this).
```
$ mitsuba beck_parametric.xml
```

<b>beck_svr.xml:</b>
Mitsuba scene file that uses the Beckmann BRDF with the svr remapped texture maps (make sure to run `svr_remapping.py` before running this).
```
$ mitsuba beck_svr.xml
```

### BibTeX
If you find our work useful, please cite:
```
@article{Sztrajman2019Imagebased,
    author = {Sztrajman, Alejandro and K\v{r}iv\'anek, Jaroslav and Wilkie, Alexander and Weyrich, Tim},
    title = {Image-based Remapping of Spatially-Varying Material Appearance},
    year = 2019,
    month = oct,
    day = 31,
    journal = {Journal of Computer Graphics Techniques (JCGT)},
    volume = 8,
    number = 4,
    pages = {1--30},
    url = {http://jcgt.org/published/0008/04/01/},
    issn = {2331-7418},
    authorurl = {http://reality.cs.ucl.ac.uk/projects/reflectance-remapping/sztrajman2019image-based.html},
}
```

### Contact
If you have any questions, please email Alejandro Sztrajman at a.sztrajman@ucl.ac.uk.
