# ChineseTextClassificationGUI
程序参考GitHub开源项目：https://github.com/649453932/Chinese-Text-Classification-Pytorch

我利用原作者的项目训练好模型，将模型预测结果使用GUI进行输出。
GUI页面采用PyQt5进行编写，因此需要有PyQt5的库文件，并且需要安装tensorboardX,numpy等库。
推荐使用PyCharm打开项目，运行main.py即可。
</br>
注意：需要自行在saved_dict目录下放置各个模型的.ckpt文件，软件才可以正常运行。
<hr>
<h3>程序运行图</h3>
主页面如下图所示：
</br>
<img src="Graphs/main Window.png" alt="Main Window" width=600px height=250px>
分类结果如下图所示：
</br>
<img src="Graphs/Classify.png" alt="Classify" width=600px height=250px>
<hr>
<h3>模型性能</h3>
<h4>Batch-Size</h4>
<h5>Batch-Size Accuracy</h5>
<img src="Graphs/Batch_Size_Acc.png" alt="Batch_Size_Acc" width=470px height=340px>
<h5>Batch-Size Loss</h5>
<img src="Graphs/Batch_Size_Loss.png" alt="Batch_Size_Loss" width=470px height=340px>

<h4>Drop Out</h4>
<h5>Drop-Out Accuracy</h5>
<img src="Graphs/Drop_Out_Acc.png" alt="Batch_Size_Acc" width=470px height=340px>
<h5>Drop-Out Loss</h5>
<img src="Graphs/Drop_Out_Loss.png" alt="Batch_Size_Loss" width=470px height=340px>

<h4>Random Seed</h4>
<h5>Random-Seed Accuracy</h5>
<img src="Graphs/Random_Seed_Acc.png" alt="Batch_Size_Acc" width=470px height=340px>
<h5>Random-Seed Loss</h5>
<img src="Graphs/Random_Seed_Loss.png" alt="Batch_Size_Loss" width=470px height=340px>

<h4>项目中所使用的参数已是作者所测试的最佳值，模型表现为我所测试的最佳状态。</h4>
<hr>
上传日期：2024年11月25日 22:50
</br>
作者：Sam iLiant（参考源项目见上述链接）

