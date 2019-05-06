# svr-remap
Application of Support Vector Regression and parametric methods for the translation between different BRDF models.

## USAGE

svr_remapping.py:
        $ python3 svr_remapping.py

        Reads uniform remapping data from mitsuba-ward2mitsuba-as.csv, fits with SVR remapping method and uses fitting to remap specular.exr and roughness.exr textures. Fitted SVR models are saved in disk for subsequent runs.

parametric_remapping.py:
        $ python3 svr_remapping.py

        Reads uniform remapping data from mitsuba-ward2mitsuba-as.csv, fits with parametric remapping method and output plots of data and fitting curve (roughness_vs_roughness.jpg and specular_vs_specular.jpg). Also reads specular.exr and roughness.exr textures and outputs remapped versions (roughness_as_remapped.exr and specular_as_remapped.exr).

