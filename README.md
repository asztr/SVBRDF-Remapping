# Remapping of Spatially-Varying BRDFs
Application of Support Vector Regression (SVR) and parametric methods for the translation between different BRDF models.

<p align="center">
<img src="https://user-images.githubusercontent.com/10238412/127756365-f270df52-f34f-4319-8153-ee4c425ba993.gif" width="35%"/>
</p>

## USAGE

SVR Remapping:
        ```$ python3 svr_remapping.py```

> Reads uniform remapping data from mitsuba-ward2mitsuba-as.csv, fits with SVR remapping method and uses fitting to remap specular.exr and roughness.exr textures. Fitted SVR models are saved in disk for subsequent runs.

Parametric Remapping:
        ```$ python3 parametric_remapping.py```

> Reads uniform remapping data from mitsuba-ward2mitsuba-as.csv, fits with parametric remapping method and output plots of data and fitting curve (roughness_vs_roughness.jpg and specular_vs_specular.jpg). Also reads specular.exr and roughness.exr textures and outputs remapped versions (roughness_as_remapped.exr and specular_as_remapped.exr).
