#速度图
import cinrad

nFiles = ("D:\\test-data\\radar-netting\radar\\raw-data\\SINGLERADAR\\ARCHIVES\\PRE_QC"
          "\\安化\\Z_RADR_I_Z9737_20240701000222_O_DOR_SA_CAP_FMT.bin.bz2")
f = cinrad.io.read_auto(nFiles)
data = f.get_data(0, 230, "REF")  # 读取第一层的反射率

data
