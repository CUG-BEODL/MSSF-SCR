# <center> High-Resolution Geochemical Data Mapping With Swin Transformer-Convolution-Based Multi-Source Geoscience Data Fusion </center>

<div align="center">

**[[Paper Page]](https://ieeexplore.ieee.org/abstract/document/10824821)**

</div>


## Quick View
![MSSF-SCR](img/model.png)

## Usage
### Perpare
- **Python environment**  
You need to install the following libraries: *pytorch, timm, gdal, numpy, pandas, sklearn, scipy, tqdm*.
```bash
conda create -n mssf_scr python=3.10

# Recommend installing according to the official PyTorch method.(Don't use the following)
conda install pytorch=2.1

conda install timm=0.9.16
```

- **Training data**  
Use the *trainData_prepare.py* file in the tool folder to automatically generate the required training files. If there is no patch shapefile, run *patch_prepare.py* first (a CSV file with coordinate information is required).

## Contact
 🙋 If you have any question or want to use the code, please contact yanjn@cug.edu.cn

 🌟 If you find this resource helpful, please consider to star this repository and cite our research.  
```
@ARTICLE{yuan2025high,
  author={Yuan, Ye and Zhou, Shuguang and Bian, Jianhua and Wang, Jinlin and Han, Wei and Yan, Jining},
  journal={IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing}, 
  title={High-Resolution Geochemical Data Mapping With Swin Transformer-Convolution-Based Multisource Geoscience Data Fusion}, 
  year={2025},
  volume={18},
  number={},
  pages={3530-3543},
  keywords={Remote sensing;Geoscience;Transformers;Feature extraction;Geology;Data models;Accuracy;Costs;Vegetation mapping;Mineral resources;Data fusion;deep learning;geochemical data;multisource geoscience data;remote sensing},
  doi={10.1109/JSTARS.2025.3525675}}
```