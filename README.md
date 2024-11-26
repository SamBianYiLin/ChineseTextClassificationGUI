# ChineseTextClassificationGUI
##程序参考GitHub开源项目：<a href=“https://github.com/649453932/Chinese-Text-Classification-Pytorch” title=“原作者链接”>原作者链接</a>

我利用原作者的项目训练好模型，将模型预测结果使用GUI进行输出。模型预测准确度相对较高。
GUI页面采用PyQt5进行编写，因此需要有PyQt5的库文件，并且需要安装tensorboardX,numpy等库。
推荐使用PyCharm打开项目，运行main.py即可。
</br>
注意：需要自行在saved_dict目录下放置各个模型的.ckpt文件，软件才可以正常运行。
——
##程序运行图
###主页面如下图所示：
</br>
<img src="Graphs/main Window.png" alt="Main Window" width=600px height=250px>
###分类结果如下图所示：
</br>
<img src="Graphs/Classify.png" alt="Classify" width=600px height=250px>
<hr>
##模型性能
###Batch-Size
####Batch-Size Accuracy
<img src="Graphs/Batch_Size_Acc.png" alt="Batch_Size_Acc" width=470px height=340px>
####Batch-Size Loss
<img src="Graphs/Batch_Size_Loss.png" alt="Batch_Size_Loss" width=470px height=340px>

###Drop Out
####Drop-Out Accuracy
<img src="Graphs/Drop_Out_Acc.png" alt="Batch_Size_Acc" width=470px height=340px>
####Drop-Out Loss
<img src="Graphs/Drop_Out_Loss.png" alt="Batch_Size_Loss" width=470px height=340px>

###Random Seed
####Random-Seed Accuracy
<img src="Graphs/Random_Seed_Acc.png" alt="Batch_Size_Acc" width=470px height=340px>
####Random-Seed Loss
<img src="Graphs/Random_Seed_Loss.png" alt="Batch_Size_Loss" width=470px height=340px>

###项目中所使用的参数已是作者所测试的最佳值，模型表现为我所测试的最佳状态。
——
##训练及运行环境
python 3.8
tensorboardX
tdqm
pytorch 1.1
PyQt5
sklearn
——
##模型训练方法
`python run.py —model TextCNN #训练TextCNN模型的方法`
`python run.py —model TextRNN #训练TextCNN模型的方法`
`python run.py —model TextRCNN #训练TextCNN模型的方法`
`python run.py —model FastText #训练TextCNN模型的方法`
`python run.py —model TextRNN_Att #训练TextCNN模型的方法`
`python run.py —model DPCNN #训练TextCNN模型的方法`
`python run.py —model Transformer #训练TextCNN模型的方法`
——
##使用说明
<ul>
<li>模型文件需要按上述步骤自行训练，也可直接导入自己预训练好的模型</li>
<li>运行需有PyQt5库，否则无法正常运行，需自行配置环境变量或使用虚拟环境</li>
<li>打开main.py，使用IDE或python命令即可运行，出现GUI界面</li>
<li>如果程序出现bug，请发issues，在看到后会及时改正</li>
</ul>
——
###上传日期：2024年11月25日 22:50
</br>
###作者：Sam iLiant（参考源项目见上述链接）
