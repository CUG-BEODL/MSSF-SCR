# <center>High-Resolution Geochemical Data Mapping With Swin Transformer-Convolution-Based Multi-Source Geoscience Data Fusion

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
Use the *trainData_prepare* file in the tool folder to automatically generate the required training files. If there is no patch shapefile, run *patch_prepare* first (a CSV file with coordinate information is required).

## Contact
If you find this resource helpful, please consider to star this repository and cite our research.  
```
@article{10824821,
  author={Yuan, Ye and Zhou, Shuguang and Bian, Jianhua and Wang, Jinlin and Han, Wei and Yan, Jining},
  journal={IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing}, 
  title={High-Resolution Geochemical Data Mapping With Swin Transformer-Convolution-Based Multi-Source Geoscience Data Fusion}, 
  year={2025},
  volume={},
  number={},
  pages={1-14},
  doi={10.1109/JSTARS.2025.3525675}}
```